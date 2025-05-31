# Aplikacja do Raportowania Konkursu Dronów

## Wymagania

- Python 3.8+
- Firebase konto
- Konto email do wysyłania raportów

## Instalacja

1. Zainstaluj wymagane pakiety:

```bash
pip install -r requirements.txt
```

2. Skonfiguruj Firebase:

   - Utwórz projekt w Firebase Console
   - Pobierz plik credentials i zapisz jako `firebase-credentials.json` w głównym katalogu projektu

3. Skonfiguruj zmienne środowiskowe:
   Utwórz plik `.env` z następującymi zmiennymi:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL=twoj.email@gmail.com
   EMAIL_PASSWORD=twoje_haslo_aplikacji
   ```

## Użycie

Aplikacja obsługuje następujące funkcje:

1. Raportowanie misji:

   - Lot ZERO (Misja 1)
   - Wykrywanie zmian (Misja 2 i 3)
   - Misje specjalne (Misja 4)

2. Automatyczne generowanie raportów PDF

3. Wysyłanie raportów na email

4. Obsługa sytuacji nadzwyczajnych

## Przykład użycia

```python
from app import DroneCompetitionApp

app = DroneCompetitionApp()

# Przykładowe dane misji
mission_data = {
    'mission_type': 'Lot ZERO',
    'timestamp': datetime.now().isoformat(),
    'detected_changes': [],
    'workers_present': 0,
    'safety_compliance': True
}

# Zapisanie danych i wysłanie raportu
app.save_mission_data(1, mission_data)
pdf_path = app.create_mission_report(1, mission_data)
app.send_report(pdf_path, 'janstojowski@gmail.com')
```

## Struktura raportu

Raport zawiera:

- Informacje o misji
- Wykryte zmiany w infrastrukturze
- Informacje o pracownikach
- Status BHP
- Sytuacje nadzwyczajne (jeśli wystąpiły)

## Bezpieczeństwo

- Wszystkie dane są przechowywane w Firebase
- Raporty są wysyłane przez bezpieczne połączenie SMTP
- Dane wrażliwe są przechowywane w zmiennych środowiskowych
