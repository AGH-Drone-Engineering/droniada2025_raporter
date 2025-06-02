import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json
import os
from datetime import datetime
import argparse
from typing import List, Dict, Tuple, Optional
import sys
import math

class LocalMapProcessor:
    def __init__(self, config_path: Optional[str] = None):
        """
        Inicjalizacja procesora mapy
        :param config_path: Ścieżka do pliku konfiguracyjnego JSON
        """
        self.default_config = {
            'marker_size': 20,
            'font_size': 20,
            'colors': {
                'infrastructure': (0, 255, 0),  # Zielony
                'emergency': (255, 0, 0),      # Czerwony
                'worker': (0, 0, 255),         # Niebieski
                'text': (0, 0, 0)              # Czarny
            }
        }
        
        self.config = self.load_config(config_path) if config_path else self.default_config
        # Zahardcodowane współrzędne dla Gliwic
        self.map_bounds = {
            'upper_left': (50.2728434, 18.6705653),
            'lower_right': (50.2725078, 18.6716368)
        }
        self.image = None

    def load_config(self, config_path: str) -> dict:
        """Ładuje konfigurację z pliku JSON"""
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        # Konwertuj listy kolorów na krotki
        if 'colors' in config:
            config['colors'] = {
                k: tuple(v) for k, v in config['colors'].items()
            }
            
        return {**self.default_config, **config}

    def load_map_image(self, image_path: str):
        """Ładuje obraz mapy"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Nie znaleziono pliku: {image_path}")
        
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"Nie udało się załadować obrazu: {image_path}")

    def convert_gps_to_pixel(self, gps_coords: Tuple[float, float]) -> Tuple[int, int]:
        """Konwertuje współrzędne GPS na piksele na obrazie"""
        if self.image is None:
            raise ValueError("Najpierw załaduj obraz")
        
        lat, lon = gps_coords
        height, width = self.image.shape[:2]
        
        # Obliczanie współczynników skalowania
        lat_scale = height / (self.map_bounds['upper_left'][0] - self.map_bounds['lower_right'][0])
        lon_scale = width / (self.map_bounds['lower_right'][1] - self.map_bounds['upper_left'][1])
        
        # Konwersja współrzędnych
        x = int((lon - self.map_bounds['upper_left'][1]) * lon_scale)
        y = int((self.map_bounds['upper_left'][0] - lat) * lat_scale)
        
        return (x, y)

    def add_point_offset(self, lat: float, lon: float, d_north_m: float, d_east_m: float) -> Tuple[float, float]:
        """Zwraca nowe współrzędne GPS oddalone o d_north_m na północ i d_east_m na wschód od podanego punktu."""
        # Stałe
        R = 6378137  # promień Ziemi w metrach
        dLat = d_north_m / R
        dLon = d_east_m / (R * math.cos(math.pi * lat / 180))
        new_lat = lat + dLat * 180 / math.pi
        new_lon = lon + dLon * 180 / math.pi
        return new_lat, new_lon

    def draw_marker(self, draw: ImageDraw.ImageDraw, coords: Tuple[int, int], 
                   marker_type: str, description: str, font: ImageFont.FreeTypeFont, gps_coords: Tuple[float, float], img_pil: Image.Image):
        """Wstawia ikonę z folderu icons na mapę oraz dodaje opis i współrzędne GPS"""
        size = self.config['marker_size']
        icon_path = os.path.join('icons', f'{marker_type}.png')
        if not os.path.exists(icon_path):
            # Jeśli nie ma ikony dla typu, nie rysuj markera
            return
        # Ikona powinna być większa niż marker_size
        icon_scale = 1.3  # 30% większa
        icon_size = int(size * icon_scale)
        icon = Image.open(icon_path).convert('RGBA').resize((icon_size, icon_size), Image.LANCZOS)
        img_pil.paste(icon, (coords[0]-icon_size//2, coords[1]-icon_size//2), icon)
        # Przygotuj tekst główny
        text = f"{marker_type}: {description}"
        text_pos = (coords[0]+size//2+5, coords[1]-size//2)
        text_bbox = draw.textbbox(text_pos, text, font=font)
        draw.rectangle(text_bbox, fill=(255,255,255))
        draw.text(
            text_pos,
            text,
            fill=self.config['colors']['text'],
            font=font
        )
        # Przygotuj tekst współrzędnych GPS (mniejsza czcionka)
        lat, lon = gps_coords
        coords_text = f"{lat:.6f}, {lon:.6f}"
        try:
            small_font = ImageFont.truetype("DejaVuSans.ttf", max(1, font.size-1))
        except:
            small_font = ImageFont.load_default()
        coords_text_pos = (text_pos[0], text_bbox[3]+2)
        coords_text_bbox = draw.textbbox(coords_text_pos, coords_text, font=small_font)
        draw.rectangle(coords_text_bbox, fill=(255,255,255))
        draw.text(
            coords_text_pos,
            coords_text,
            fill=self.config['colors']['text'],
            font=small_font
        )

    def process_map(self, 
                   image_path: str,
                   changes: List[Dict],
                   output_path: Optional[str] = None) -> str:
        """
        Przetwarza mapę i nanosi na nią zmiany
        :param image_path: Ścieżka do obrazu mapy
        :param changes: Lista zmian do naniesienia
        :param output_path: Ścieżka do zapisu wynikowego obrazu
        :return: Ścieżka do wygenerowanego obrazu
        """
        # Załaduj dane
        self.load_map_image(image_path)
        
        # Dodaj punkt 2m na północ od pierwszego infrastructure
        infra = next((c for c in changes if c['type'] == 'infrastructure'), None)
        if infra:
            lat, lon = infra['gps_coords']
            new_lat, new_lon = self.add_point_offset(lat, lon, 2, 0)  # 2m na północ
            changes.append({
                'type': 'other',
                'description': '2m na północ od infrastructure',
                'gps_coords': [new_lat, new_lon]
            })
        
        # Konwertuj na format PIL
        img_pil = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        
        # Załaduj czcionkę
        font_path = "DejaVuSans.ttf"  # lub "arial.ttf" jeśli masz tę czcionkę
        if not os.path.exists(font_path):
            print("Brak pliku czcionki DejaVuSans.ttf! Pobierz ją np. z https://dejavu-fonts.github.io/")
            sys.exit(1)
        font_size = max(1, self.config['font_size'] - 2)
        font = ImageFont.truetype(font_path, font_size)

        # Nanieś zmiany
        for change in changes:
            coords = self.convert_gps_to_pixel(change['gps_coords'])
            self.draw_marker(draw, coords, change['type'], change['description'] if 'description' in change else '', font, change['gps_coords'], img_pil)

        # Zapisz wynik
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"map_with_changes_{timestamp}.png"
        
        img_pil.save(output_path)
        return output_path

def main():
    parser = argparse.ArgumentParser(description='Przetwarzanie lokalnej mapy')
    parser.add_argument('--image', required=True, help='Ścieżka do obrazu mapy')
    parser.add_argument('--config', help='Ścieżka do pliku konfiguracyjnego JSON')
    parser.add_argument('--changes', required=True, help='Ścieżka do pliku JSON ze zmianami')
    parser.add_argument('--output', help='Ścieżka do zapisu wynikowego obrazu')
    
    args = parser.parse_args()
    
    try:
        # Załaduj zmiany
        with open(args.changes, 'r', encoding='utf-8') as f:
            changes = json.load(f)
        
        # Przetwórz mapę
        processor = LocalMapProcessor(args.config)
        output_path = processor.process_map(
            args.image,
            changes,
            args.output
        )
        
        print(f"Wygenerowano mapę: {output_path}")
        
    except Exception as e:
        print(f"Błąd: {str(e)}")

if __name__ == "__main__":
    main() 