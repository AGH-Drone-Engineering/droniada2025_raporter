# UWAGA: W katalogu projektu muszą znajdować się pliki DejaVuSans.ttf oraz DejaVuSans-Bold.ttf
from fpdf import FPDF
from datetime import datetime

DARK_BG = (255, 255, 255)  # Białe tło
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (60, 120, 40)


def rgb_to_fpdf(rgb):
    return tuple(int(x) for x in rgb)


def generate_pdf(team_info, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)
    # Dodaj czcionki
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf', uni=True)

    # Spis treści
    pdf.set_xy(10, 10)
    pdf.set_text_color(*BLACK)
    pdf.set_font('DejaVu', 'B', 13)
    pdf.cell(0, 10, 'Raport z lotu AGH - INSPEKCJA', ln=True, align='C')
    pdf.ln(2)
    pdf.set_font('DejaVu', '', 11)
    pdf.set_text_color(*BLACK)
    pdf.cell(0, 8, 'Spis treści', ln=True)
    pdf.set_font('DejaVu', '', 9)
    pdf.ln(1)
    toc = [
        'Podstawowe informacje o wykonanej misji',
        'Dodatkowe informacje o wykonanej misji',
        'Lista pracowników znajdujących się na terenie',
        'Zmiany w infrastrukturze',
        'Sytuacje nadzwyczajne',
        'Kody ArUcoS',
        'Mapa infrastruktury',
        'Informacje końcowe'
    ]
    for i, t in enumerate(toc, 1):
        pdf.set_text_color(60, 120, 40) if i <= 2 else pdf.set_text_color(*BLACK)
        pdf.cell(0, 6, f'{i}. {t}', ln=True)
    pdf.set_text_color(*BLACK)
    pdf.ln(2)

    # Sekcja 1 - Tabela
    pdf.set_font('DejaVu', 'B', 9)
    pdf.cell(0, 7, '1. PODSTAWOWE INFORMACJE O WYKONANEJ MISJI', ln=True)
    pdf.ln(1)
    col_widths = [70, 110]
    # Nagłówki
    pdf.set_fill_color(*GREEN)
    pdf.set_text_color(*WHITE)
    pdf.set_font('DejaVu', 'B', 9)
    pdf.cell(col_widths[0], 8, '', 1, 0, 'C', 1)
    pdf.cell(col_widths[1], 8, 'zespół', 1, 1, 'C', 1)
    # Wiersze
    pdf.set_font('DejaVu', '', 9)
    for row in [
        ('NAZWA / EMAIL', f"{team_info['name']} / {team_info['email']}"),
        ('NAZWISKO PILOTA / NR KOMÓRKI', team_info.get('pilot', '')),
        ('DATA I GODZINA ROZPOCZĘCIA MISJI', team_info.get('mission_start', '')),
        ('NR MISJI', team_info.get('mission_number', '')),
        ('CZAS TRWANIA LOTU', team_info.get('flight_time', '')),
        ('STAN BATERII PRZED WYKONANIEM LOTU', team_info.get('battery_before', '')),
    ]:
        pdf.set_text_color(*BLACK)
        pdf.cell(col_widths[0], 8, row[0], 1, 0, 'L', 0)
        pdf.cell(col_widths[1], 8, row[1], 1, 1, 'L', 0)
    pdf.ln(2)

    # Sekcja 2 - Tabela
    pdf.set_font('DejaVu', 'B', 9)
    pdf.cell(0, 7, '2. DODATKOWE INFORMACJE O WYKONANEJ MISJI', ln=True)
    pdf.ln(1)
    pdf.set_fill_color(*GREEN)
    pdf.set_text_color(*WHITE)
    pdf.set_font('DejaVu', 'B', 9)
    pdf.cell(col_widths[0], 8, '', 1, 0, 'C', 1)
    pdf.cell(col_widths[1], 8, 'zespół', 1, 1, 'C', 1)
    pdf.set_font('DejaVu', '', 9)
    for row in [
        ('INDEX KP', team_info.get('kp_index', '')),
        ('STAN BATERII PO ZAKOŃCZENIU LOTU', team_info.get('battery_after', '')),
    ]:
        pdf.set_text_color(*BLACK)
        pdf.cell(col_widths[0], 8, row[0], 1, 0, 'L', 0)
        pdf.cell(col_widths[1], 8, row[1], 1, 1, 'L', 0)

    # Sekcja 3 - Pracownicy
    workers = [p for p in team_info.get('points', []) if p.get('type') == 'worker']
    if not workers and 'workers' in team_info:
        workers = team_info['workers']
    print(f"[PDF] Liczba pracowników: {len(workers)}")
    pdf.add_page()
    if workers:
        pdf.ln(4)
        pdf.set_font('DejaVu', 'B', 10)
        pdf.set_text_color(*BLACK)
        pdf.cell(0, 8, '3. LISTA PRACOWNIKÓW ZNAJDUJĄCYCH SIĘ NA TERENIE ZAKŁADU', ln=True)
        pdf.ln(1)
        # Kolory
        BLUE = (40, 80, 160)
        table_width = pdf.w - 2 * pdf.l_margin
        col_widths = [table_width * 0.08, table_width * 0.18, table_width * 0.44, table_width * 0.30]  # proporcje: 8%, 18%, 44%, 30%
        # Nagłówki
        pdf.set_fill_color(*GREEN)
        pdf.cell(sum(col_widths), 8, 'zespół', 1, 1, 'C', 1)
        pdf.set_fill_color(100, 160, 255)  # jasnoniebieski
        pdf.set_text_color(*BLACK)
        pdf.set_font('DejaVu', 'B', 9)
        pdf.cell(col_widths[0], 8, '#', 1, 0, 'C', 1)
        pdf.cell(col_widths[1], 8, 'BHP', 1, 0, 'C', 1)
        pdf.cell(col_widths[2], 8, 'LOKALIZACJA', 1, 0, 'C', 1)
        pdf.cell(col_widths[3], 8, 'ZDJĘCIE', 1, 1, 'C', 1)
        # Wiersze
        pdf.set_font('DejaVu', '', 9)
        for idx, worker in enumerate(workers[:6], 1):
            pdf.set_text_color(*BLACK)
            pdf.cell(col_widths[0], 24, str(idx), 1, 0, 'C', 0)
            pdf.cell(col_widths[1], 24, worker.get('bhp', ''), 1, 0, 'C', 0)
            gps = worker.get('gps_coords', [None, None])
            loc_str = f"Lat {gps[0]:.5f}, Long {gps[1]:.5f}" if gps[0] is not None and gps[1] is not None else ''
            pdf.cell(col_widths[2], 24, loc_str, 1, 0, 'C', 0)
            import base64
            from io import BytesIO
            from PIL import Image
            photo_b64 = worker.get('photo_b64', '')
            if photo_b64:
                try:
                    img_data = base64.b64decode(photo_b64)
                    img = Image.open(BytesIO(img_data))
                    img.thumbnail((20, 20))  # proporcje 1:1
                    temp_path = f"temp_worker_{idx}.png"
                    img.save(temp_path)
                    x = pdf.get_x()
                    y = pdf.get_y()
                    pdf.cell(col_widths[3], 24, '', 1, 0, 'C', 0)
                    # Wyśrodkuj obrazek w komórce
                    img_x = x + (col_widths[3] - 20) / 2
                    img_y = y + 2
                    pdf.image(temp_path, img_x, img_y, 20, 20)
                except Exception:
                    x = pdf.get_x()
                    y = pdf.get_y()
                    pdf.cell(col_widths[3], 24, '', 1, 0, 'C', 0)
                    try:
                        img_x = x + (col_widths[3] - 20) / 2
                        img_y = y + 2
                        pdf.image('worker_default.png', img_x, img_y, 20, 20)
                    except Exception:
                        pass
            else:
                x = pdf.get_x()
                y = pdf.get_y()
                pdf.cell(col_widths[3], 24, '', 1, 0, 'C', 0)
                try:
                    img_x = x + (col_widths[3] - 20) / 2
                    img_y = y + 2
                    pdf.image('worker_default.png', img_x, img_y, 20, 20)
                except Exception:
                    pass
            pdf.ln()
    else:
        pdf.ln(4)
        pdf.set_font('DejaVu', 'B', 10)
        pdf.set_text_color(*BLACK)
        pdf.cell(0, 8, '3. LISTA PRACOWNIKÓW ZNAJDUJĄCYCH SIĘ NA TERENIE ZAKŁADU (Brak pracowników)', ln=True)

    # Sekcja 4 - Zmiany w infrastrukturze
    ICON_CATEGORY_MAP = {
        'tower': ('Słup energetyczny', 'icons/tower.png'),
        'broken-tower': ('Słup energetyczny', 'icons/broken-tower.png'),
        'rusty-pipe': ('Rurociąg', 'icons/rusty-pipe.png'),
        'fixed-pipe': ('Rurociąg', 'icons/fixed-pipe.png'),
        'barrel': ('Beczka', 'icons/barrel.png'),
        'europallet': ('Paleta', 'icons/europallet.png'),
        'removed-europallet': ('Paleta', 'icons/removed-europallet.png'),
        'car': ('Samochód', 'icons/car.png'),
        'removed-car': ('Samochód', 'icons/removed-car.png'),
        'fence': ('Płot', 'icons/fence.png'),
        'broken-fence': ('Płot', 'icons/broken-fence.png'),
        'pipe': ('Rurociąg', 'icons/pipe.png'),
        'broken-pipe': ('Rurociąg', 'icons/broken-pipe.png'),
        'powerline': ('Linia energetyczna', 'icons/powerline.png'),
        'broken-powerline': ('Linia energetyczna', 'icons/broken-powerline.png'),
        'powerpole': ('Słup energetyczny', 'icons/powerpole.png'),
        'broken-powerpole': ('Słup energetyczny', 'icons/broken-powerpole.png'),
        'car': ('Samochód', 'icons/car.png'),
        'pipeline': ('Rurociąg', 'icons/infrastructure.png'),
        
        # ... inne mapowania ...
    }
    infra_types = list(ICON_CATEGORY_MAP.keys())
    print(infra_types)
    print([p['type'] for p in team_info.get('points', [])])
    infra_points = [p for p in team_info.get('points', []) if p.get('type') in infra_types]
    if infra_points:
        pdf.add_page()
        pdf.ln(4)
        pdf.set_font('DejaVu', 'B', 10)
        pdf.set_text_color(*BLACK)
        pdf.multi_cell(0, 8, '4. ZMIANY W INFRASTRUKTURZE W STOSUNKU DO LOTU "ZERO"', align='L')
        pdf.ln(1)
        table_width = pdf.w - 2 * pdf.l_margin
        col_widths = [table_width * 0.06, table_width * 0.22, table_width * 0.18, table_width * 0.28, table_width * 0.26]
        row_height = 36  # wyższy wiersz dla większego zdjęcia
        padding_y = 6
        pdf.set_fill_color(*GREEN)
        pdf.cell(sum(col_widths), 8, 'zespół', 1, 1, 'C', 1)
        pdf.set_fill_color(100, 160, 255)
        pdf.set_text_color(*BLACK)
        pdf.set_font('DejaVu', 'B', 9)
        pdf.cell(col_widths[0], 8, '#', 1, 0, 'C', 1)
        pdf.cell(col_widths[1], 8, 'KATEGORIA', 1, 0, 'C', 1)
        pdf.cell(col_widths[2], 8, 'CZAS WYKRYCIA', 1, 0, 'C', 1)
        pdf.cell(col_widths[3], 8, 'LOKALIZACJA', 1, 0, 'C', 1)
        pdf.cell(col_widths[4], 8, 'ZDJĘCIE', 1, 1, 'C', 1)
        pdf.set_font('DejaVu', '', 9)
        for idx, infra in enumerate(infra_points, 1):
            pdf.set_text_color(*BLACK)
            x_start = pdf.get_x()
            y_start = pdf.get_y()
            # Przygotuj teksty do łamania
            typ = infra.get('type', '')
            desc, icon_path = ICON_CATEGORY_MAP.get(typ, ('Inne', 'icons/bag.png'))
            desc_lines = desc.split('\n')
            detection_time = infra.get('detection_time', '[DD/MM/RRRR, GG:MM:SS]')
            if ',' in detection_time:
                date_part, time_part = detection_time.split(',', 1)
                time_lines = [date_part.strip(), time_part.strip()]
            else:
                time_lines = [detection_time]
            gps = infra.get('gps_coords', [None, None])
            if gps[0] is not None and gps[1] is not None:
                loc_lines = [f"Lat {gps[0]:.5f}", f"Long {gps[1]:.5f}"]
            else:
                loc_lines = ['']
            max_lines = max(len(desc_lines), len(time_lines), len(loc_lines))
            line_height = (row_height - 2*padding_y) / max_lines
            # #
            pdf.cell(col_widths[0], row_height, str(idx), 1, 0, 'C', 0)
            # Kategoria
            y_cell = pdf.get_y()
            for i in range(max_lines):
                txt = desc_lines[i] if i < len(desc_lines) else ''
                y_line = y_cell + padding_y + i*line_height
                pdf.set_xy(x_start + col_widths[0], y_line)
                pdf.cell(col_widths[1], line_height, txt, 0, 0, 'C', 0)
            pdf.set_xy(x_start + col_widths[0], y_cell)
            pdf.cell(col_widths[1], row_height, '', 1, 0, '', 0)
            # Czas
            for i in range(max_lines):
                txt = time_lines[i] if i < len(time_lines) else ''
                y_line = y_cell + padding_y + i*line_height
                pdf.set_xy(x_start + col_widths[0] + col_widths[1], y_line)
                pdf.cell(col_widths[2], line_height, txt, 0, 0, 'C', 0)
            pdf.set_xy(x_start + col_widths[0] + col_widths[1], y_cell)
            pdf.cell(col_widths[2], row_height, '', 1, 0, '', 0)
            # Lokalizacja
            for i in range(max_lines):
                txt = loc_lines[i] if i < len(loc_lines) else ''
                y_line = y_cell + padding_y + i*line_height
                pdf.set_xy(x_start + col_widths[0] + col_widths[1] + col_widths[2], y_line)
                pdf.cell(col_widths[3], line_height, txt, 0, 0, 'C', 0)
            pdf.set_xy(x_start + col_widths[0] + col_widths[1] + col_widths[2], y_cell)
            pdf.cell(col_widths[3], row_height, '', 1, 0, '', 0)
            # Zdjęcie
            import base64
            from io import BytesIO
            from PIL import Image
            image_b64 = infra.get('image', '')
            x_img = x_start + col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3]
            y_img = y_cell + padding_y
            pdf.set_xy(x_img, y_cell)
            pdf.cell(col_widths[4], row_height, '', 1, 0, 'C', 0)
            try:
                if image_b64:
                    img_data = base64.b64decode(image_b64)
                    img = Image.open(BytesIO(img_data))
                    img.thumbnail((row_height - 2*padding_y, row_height - 2*padding_y))
                    temp_path = f"temp_infra_{idx}.png"
                    img.save(temp_path)
                    img_x = x_img + (col_widths[4] - (row_height - 2*padding_y)) / 2
                    img_y = y_img
                    pdf.image(temp_path, img_x, img_y, row_height - 2*padding_y, row_height - 2*padding_y)
                else:
                    raise Exception('Brak zdjęcia')
            except Exception:
                try:
                    img_x = x_img + (col_widths[4] - (row_height - 2*padding_y)) / 2
                    img_y = y_img
                    pdf.image('infrastructure_default.png', img_x, img_y, row_height - 2*padding_y, row_height - 2*padding_y)
                except Exception:
                    pass
            pdf.set_xy(x_start, y_start + row_height)
            pdf.ln()

    # Sekcja 5 - Sytuacje nadzwyczajne
    event_types = ['intruder', 'fire', 'emergency']
    event_points = [p for p in team_info.get('points', []) if p.get('type') in event_types]
    if event_points:
        pdf.add_page()
        pdf.ln(4)
        pdf.set_font('DejaVu', 'B', 10)
        pdf.set_text_color(*BLACK)
        pdf.multi_cell(0, 8, '5. SYTUACJE NADZWYCZAJNE', align='L')
        pdf.ln(1)
        table_width = pdf.w - 2 * pdf.l_margin
        col_widths = [table_width * 0.06, table_width * 0.18, table_width * 0.18, table_width * 0.22, table_width * 0.18, table_width * 0.18]
        row_height = 24
        padding_y = 6
        pdf.set_fill_color(100, 160, 255)
        pdf.set_text_color(*BLACK)
        pdf.set_font('DejaVu', 'B', 9)
        pdf.cell(col_widths[0], 8, '#', 1, 0, 'C', 1)
        pdf.cell(col_widths[1], 8, 'ZDARZENIE', 1, 0, 'C', 1)
        pdf.cell(col_widths[2], 8, 'CZAS', 1, 0, 'C', 1)
        pdf.cell(col_widths[3], 8, 'LOKALIZACJA', 1, 0, 'C', 1)
        pdf.cell(col_widths[4], 8, 'ZDJĘCIE', 1, 0, 'C', 1)
        pdf.cell(col_widths[5], 8, 'POWIADOMIENIE', 1, 1, 'C', 1)
        pdf.set_font('DejaVu', '', 9)
        for idx, event in enumerate(event_points, 1):
            pdf.set_text_color(*BLACK)
            x_start = pdf.get_x()
            y_start = pdf.get_y()
            # Przygotuj teksty do łamania
            event_map = {'intruder': 'Intruz', 'fire': 'Ogień', 'emergency': 'Sytuacja\nnadzwyczajna'}
            event_name = event_map.get(event.get('type', ''), event.get('type', ''))
            event_lines = event_name.split('\n')
            detection_time = event.get('detection_time', '[DD/MM/RRRR, GG:MM:SS]')
            if ',' in detection_time:
                date_part, time_part = detection_time.split(',', 1)
                time_lines = [date_part.strip(), time_part.strip()]
            else:
                time_lines = [detection_time]
            gps = event.get('gps_coords', [None, None])
            if gps[0] is not None and gps[1] is not None:
                loc_lines = [f"Lat {gps[0]:.5f}", f"Long {gps[1]:.5f}"]
            else:
                loc_lines = ['']
            # Wyznacz max liczbę linii
            max_lines = max(len(event_lines), len(time_lines), len(loc_lines))
            line_height = (row_height - 2*padding_y) / max_lines
            # #
            pdf.cell(col_widths[0], row_height, str(idx), 1, 0, 'C', 0)
            # Zdarzenie
            y_cell = pdf.get_y()
            pdf.set_xy(pdf.get_x(), y_cell)
            for i in range(max_lines):
                txt = event_lines[i] if i < len(event_lines) else ''
                y_line = y_cell + padding_y + i*line_height
                pdf.set_xy(x_start + col_widths[0], y_line)
                pdf.cell(col_widths[1], line_height, txt, 0, 0, 'C', 0)
            pdf.set_xy(x_start + col_widths[0], y_cell)
            pdf.cell(col_widths[1], row_height, '', 1, 0, '', 0)
            # Czas
            for i in range(max_lines):
                txt = time_lines[i] if i < len(time_lines) else ''
                y_line = y_cell + padding_y + i*line_height
                pdf.set_xy(x_start + col_widths[0] + col_widths[1], y_line)
                pdf.cell(col_widths[2], line_height, txt, 0, 0, 'C', 0)
            pdf.set_xy(x_start + col_widths[0] + col_widths[1], y_cell)
            pdf.cell(col_widths[2], row_height, '', 1, 0, '', 0)
            # Lokalizacja
            for i in range(max_lines):
                txt = loc_lines[i] if i < len(loc_lines) else ''
                y_line = y_cell + padding_y + i*line_height
                pdf.set_xy(x_start + col_widths[0] + col_widths[1] + col_widths[2], y_line)
                pdf.cell(col_widths[3], line_height, txt, 0, 0, 'C', 0)
            pdf.set_xy(x_start + col_widths[0] + col_widths[1] + col_widths[2], y_cell)
            pdf.cell(col_widths[3], row_height, '', 1, 0, '', 0)
            # Zdjęcie
            import base64
            from io import BytesIO
            from PIL import Image
            image_b64 = event.get('image', '')
            x_img = x_start + col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3]
            y_img = y_cell + padding_y
            pdf.set_xy(x_img, y_cell)
            pdf.cell(col_widths[4], row_height, '', 1, 0, 'C', 0)
            try:
                if image_b64:
                    img_data = base64.b64decode(image_b64)
                    img = Image.open(BytesIO(img_data))
                    img.thumbnail((row_height - 2*padding_y, row_height - 2*padding_y))
                    temp_path = f"temp_event_{idx}.png"
                    img.save(temp_path)
                    img_x = x_img + (col_widths[4] - (row_height - 2*padding_y)) / 2
                    img_y = y_img
                    pdf.image(temp_path, img_x, img_y, row_height - 2*padding_y, row_height - 2*padding_y)
                else:
                    raise Exception('Brak zdjęcia')
            except Exception:
                try:
                    img_x = x_img + (col_widths[4] - (row_height - 2*padding_y)) / 2
                    img_y = y_img
                    if event.get('type') == 'emergency':
                        pdf.image('emergency_default.png', img_x, img_y, row_height - 2*padding_y, row_height - 2*padding_y)
                    else:
                        pdf.image('icons/emergency.png', img_x, img_y, row_height - 2*padding_y, row_height - 2*padding_y)
                except Exception:
                    pass
            # Powiadomienie
            pdf.set_xy(x_start + col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3] + col_widths[4], y_cell)
            pdf.cell(col_widths[5], row_height, event.get('notification', 'Tak'), 1, 0, 'C', 0)
            pdf.set_xy(x_start, y_start + row_height)
            pdf.ln()

    # Sekcja 6 - Kody ArUco
    aruco_points = [p for p in team_info.get('points', []) if p.get('type') == 'aruco']
    if aruco_points:
        pdf.add_page()
        pdf.ln(4)
        pdf.set_font('DejaVu', 'B', 10)
        pdf.set_text_color(*BLACK)
        pdf.multi_cell(0, 8, '6. KODY ARUCO', align='L')
        pdf.ln(1)
        table_width = pdf.w - 2 * pdf.l_margin
        col_widths = [table_width * 0.08, table_width * 0.38, table_width * 0.32, table_width * 0.22]
        row_height = 24
        padding_y = 6
        pdf.set_fill_color(100, 160, 255)
        pdf.set_text_color(*BLACK)
        pdf.set_font('DejaVu', 'B', 9)
        pdf.cell(col_widths[0], 8, '#', 1, 0, 'C', 1)
        pdf.cell(col_widths[1], 8, 'ZAWARTOŚĆ', 1, 0, 'C', 1)
        pdf.cell(col_widths[2], 8, 'LOKALIZACJA', 1, 0, 'C', 1)
        pdf.cell(col_widths[3], 8, 'ZDJĘCIE', 1, 1, 'C', 1)
        pdf.set_font('DejaVu', '', 9)
        for idx, aruco in enumerate(aruco_points, 1):
            pdf.set_text_color(*BLACK)
            x_start = pdf.get_x()
            y_start = pdf.get_y()
            value_lines = [str(aruco.get('value', ''))]
            gps = aruco.get('gps_coords', [None, None])
            if gps[0] is not None and gps[1] is not None:
                loc_lines = [f"Lat {gps[0]:.5f}", f"Long {gps[1]:.5f}"]
            else:
                loc_lines = ['']
            max_lines = max(len(value_lines), len(loc_lines))
            line_height = (row_height - 2*padding_y) / max_lines
            # #
            pdf.cell(col_widths[0], row_height, str(idx), 1, 0, 'C', 0)
            # Zawartość
            y_cell = pdf.get_y()
            for i in range(max_lines):
                txt = value_lines[i] if i < len(value_lines) else ''
                y_line = y_cell + padding_y + i*line_height
                pdf.set_xy(x_start + col_widths[0], y_line)
                pdf.cell(col_widths[1], line_height, txt, 0, 0, 'C', 0)
            pdf.set_xy(x_start + col_widths[0], y_cell)
            pdf.cell(col_widths[1], row_height, '', 1, 0, '', 0)
            # Lokalizacja
            for i in range(max_lines):
                txt = loc_lines[i] if i < len(loc_lines) else ''
                y_line = y_cell + padding_y + i*line_height
                pdf.set_xy(x_start + col_widths[0] + col_widths[1], y_line)
                pdf.cell(col_widths[2], line_height, txt, 0, 0, 'C', 0)
            pdf.set_xy(x_start + col_widths[0] + col_widths[1], y_cell)
            pdf.cell(col_widths[2], row_height, '', 1, 0, '', 0)
            # Zdjęcie
            import base64
            from io import BytesIO
            from PIL import Image
            image_b64 = aruco.get('image', '')
            x_img = x_start + col_widths[0] + col_widths[1] + col_widths[2]
            y_img = y_cell + padding_y
            pdf.set_xy(x_img, y_cell)
            pdf.cell(col_widths[3], row_height, '', 1, 0, 'C', 0)
            try:
                if image_b64:
                    img_data = base64.b64decode(image_b64)
                    img = Image.open(BytesIO(img_data))
                    img.thumbnail((row_height - 2*padding_y, row_height - 2*padding_y))
                    temp_path = f"temp_aruco_{idx}.png"
                    img.save(temp_path)
                    img_x = x_img + (col_widths[3] - (row_height - 2*padding_y)) / 2
                    img_y = y_img
                    pdf.image(temp_path, img_x, img_y, row_height - 2*padding_y, row_height - 2*padding_y)
                else:
                    raise Exception('Brak zdjęcia')
            except Exception:
                try:
                    img_x = x_img + (col_widths[3] - (row_height - 2*padding_y)) / 2
                    img_y = y_img
                    pdf.image('icons/qrcode.png', img_x, img_y, row_height - 2*padding_y, row_height - 2*padding_y)
                except Exception:
                    pass
            pdf.set_xy(x_start, y_start + row_height)
            pdf.ln()

    # Sekcja 7 - Mapa wykrycia
    pdf.add_page()
    pdf.ln(4)
    pdf.set_font('DejaVu', 'B', 10)
    pdf.set_text_color(*BLACK)
    pdf.multi_cell(0, 8, '7. MAPA WYKRYCIA', align='L')
    pdf.ln(2)
    try:
        # Domyślnie detection_map.png, można zmienić nazwę jeśli inna
        pdf.image('wynik.png', x=pdf.l_margin, y=pdf.get_y(), w=pdf.w - 2*pdf.l_margin)
    except Exception:
        pdf.set_font('DejaVu', '', 9)
        pdf.set_text_color(200, 0, 0)
        pdf.cell(0, 10, 'Brak mapy wykrycia (detection_map.png)', ln=True, align='C')

    pdf.output(output_path) 