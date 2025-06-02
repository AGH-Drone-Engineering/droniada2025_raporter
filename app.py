import firebase_admin
from firebase_admin import credentials, db
import time
import json
from local_map_processor import LocalMapProcessor
from send_email import send_email_with_attachment
import datetime
from fpdf import FPDF
from pdf_generator import generate_pdf
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import io
import os

KEY_PASSWORD = b'testowehaslo'
SALT = b'firebase_salt_1234'
backend = default_backend()

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    return kdf.derive(password)

def decrypt_file_to_bytes(input_path, password, salt):
    key = derive_key(password, salt)
    with open(input_path, 'rb') as f:
        iv = f.read(16)
        ct = f.read()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

# Odszyfruj klucz do pamięci
firebase_key_bytes = decrypt_file_to_bytes('firebase_key.json.enc', KEY_PASSWORD, SALT)
firebase_key_dict = json.loads(firebase_key_bytes.decode("utf-8"))
cred = credentials.Certificate(firebase_key_dict)
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

            team = data.get('team', {})
            team_info = {
                "name": team.get('name', "AGH Drone Engineering"),
                "email": team.get('email', "agh_droniada@m160.mikr.dev"),
                "pilot": team.get('pilot', "[Imię Nazwisko, nr komórki]"),
                "mission_start": team.get('mission_start', "[DD/MM/RRRR, GG:MM:SS]"),
                "mission_number": team.get('mission_number', "-1"),
                "flight_time": flight_time_str,
                "battery_before": team.get('battery_before', "98% / 18.2V"),
                "kp_index": team.get('kp_index', "1.2"),
                "battery_after": team.get('battery_after', "53% / 12.6V"),
                "points": data.get('points', [])
            }
            # Możesz przekazać team_info do generatora PDF
            processor = LocalMapProcessor('map_config.json')
            processor.process_map(
                'mapa_gliwice.png',
                points,
                'wynik.png'
            )
            print("Mapa wygenerowana jako wynik.png")
            print("Generowanie PDF...")
            generate_pdf(team_info, 'raport.pdf')
            print("PDF wygenerowany jako raport.pdf")
            print("Wysyłanie emaila...")  
            send_email_with_attachment(
              subject="AGH Drone Engineering - raport z misji",
              body="W załączniku znajduje się najnowszy raport PDF oraz mapa.",
              to="skrzynka.wrzutka@gmail.com",
              attachments=["raport.pdf", "wynik.png"],
              from_addr="agh_droniada@m160.mikr.dev",
              from_pass="!!zaq1@WSX!!"
            )
            print("Email wysłany")
            ref.update({'generate': False})
        time.sleep(3)  # sprawdzaj co 2 sekundy

if __name__ == '__main__':
    main()

    #9W5J-SJZH-O37R-0AFI