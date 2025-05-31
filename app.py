import firebase_admin
from firebase_admin import credentials, db
import time
import json
from local_map_processor import LocalMapProcessor
from send_email import send_email_with_attachment
import datetime
from fpdf import FPDF
from pdf_generator import generate_pdf

# Ścieżka do klucza serwisowego Firebase
cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://droniada-2025-default-rtdb.europe-west1.firebasedatabase.app'
})

def main():
    ref = db.reference('/')
    print("Czekam na generate:true w Firebase...")

    while True:
        data = ref.get()
        if data and data.get('generate'):
            print("Generuję mapę na podstawie punktów z Firebase...")
            points = data.get('points', [])
            if isinstance(points, dict) and 'points' in points:
                points = points['points']

            # Hardkodowane dane zespołu
            team_name = "AGH Drone Engineering"
            team_email = "agh_droniada@m160.mikr.dev"

            # Czas startu misji (jeśli jest w bazie, w formacie ISO lub "YYYY-MM-DDTHH:MM:SS")
            mission_start = data.get('team', {}).get('mission_start', None)
            if mission_start:
                try:
                    start_dt = datetime.datetime.fromisoformat(mission_start)
                except Exception:
                    start_dt = datetime.datetime.now()
            else:
                start_dt = datetime.datetime.now()

            # Czas generowania raportu
            end_dt = datetime.datetime.now()
            # Czas trwania = end - start - 1 minuta
            flight_time = end_dt - start_dt - datetime.timedelta(minutes=1)
            flight_time_str = f"{flight_time.seconds//60:02d}:{flight_time.seconds%60:02d}"

            team_info = {
                "name": team_name,
                "email": team_email,
                "flight_time": flight_time_str,
                "mission_start": start_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "mission_end": end_dt.strftime("%Y-%m-%d %H:%M:%S")
            }
            print(f"Dane zespołu: {team_info}")
            # Możesz przekazać team_info do generatora PDF
            processor = LocalMapProcessor('map_config.json')
            processor.process_map(
                'mapa_gliwice.png',
                points,
                'wynik.png'
            )
            print("Mapa wygenerowana jako wynik.png")
            print("Generowanie PDF...")
            # Dodaj dane o baterii jeśli są w bazie
            team_info['battery_before'] = data.get('team', {}).get('battery_before', '---')
            team_info['battery_after'] = data.get('team', {}).get('battery_after', '---')
            generate_pdf(team_info, 'raport.pdf')
            print("PDF wygenerowany jako raport.pdf")
            print("Wysyłanie emaila...")  
            send_email_with_attachment(
              subject="AGH Drone Engineering - raport z misji",
              body="W załączniku znajduje się najnowszy raport PDF.",
              to="skrzynka.wrzutka@gmail.com",
              attachment_path="raport.pdf",
              from_addr="agh_droniada@m160.mikr.dev",
              from_pass="!!zaq1@WSX!!"
            )
            print("Email wysłany")
            ref.update({'generate': False})
        time.sleep(2)  # sprawdzaj co 2 sekundy

if __name__ == '__main__':
    main()

    #9W5J-SJZH-O37R-0AFI