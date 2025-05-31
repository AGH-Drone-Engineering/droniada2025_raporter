# UWAGA: W katalogu projektu muszą znajdować się pliki DejaVuSans.ttf oraz DejaVuSans-Bold.ttf
from fpdf import FPDF

DARK_BG = (30, 30, 30)
WHITE = (255, 255, 255)
GREEN = (60, 120, 40)


def rgb_to_fpdf(rgb):
    return tuple(int(x) for x in rgb)


def generate_pdf(team_info, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)
    # Dodaj czcionki
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf', uni=True)

    # Tło strony
    pdf.set_fill_color(*rgb_to_fpdf(DARK_BG))
    pdf.rect(0, 0, pdf.w, pdf.h, 'F')

    # Spis treści
    pdf.set_xy(10, 10)
    pdf.set_text_color(*WHITE)
    pdf.set_font('DejaVu', 'B', 13)
    pdf.cell(0, 10, 'WZÓR RAPORTU Z KONKURENCJI "INSPEKCJA"', ln=True, align='C')
    pdf.ln(2)
    pdf.set_font('DejaVu', '', 11)
    pdf.set_text_color(*WHITE)
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
        pdf.set_text_color(180, 255, 180) if i <= 2 else pdf.set_text_color(*WHITE)
        pdf.cell(0, 6, f'{i}. {t}', ln=True)
    pdf.set_text_color(*WHITE)
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
    rows = [
        ('NAZWA / EMAIL', f"{team_info['name']} / {team_info['email']}"),
        ('NAZWISKO PILOTA / NR KOMÓRKI', team_info.get('pilot', '')),
        ('DATA I GODZINA ROZPOCZĘCIA MISJI', team_info.get('mission_start', '')),
        ('NR MISJI', team_info.get('mission_number', '')),
        ('CZAS TRWANIA LOTU', team_info.get('flight_time', '')),
        ('STAN BATERII PRZED WYKONANIEM LOTU', team_info.get('battery_before', '')),
    ]
    pdf.set_font('DejaVu', '', 9)
    for row in rows:
        pdf.set_text_color(*WHITE)
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
    rows2 = [
        ('INDEX KP', team_info.get('kp_index', '')),
        ('STAN BATERII PO ZAKOŃCZENIU LOTU', team_info.get('battery_after', '')),
    ]
    for row in rows2:
        pdf.set_text_color(*WHITE)
        pdf.cell(col_widths[0], 8, row[0], 1, 0, 'L', 0)
        pdf.cell(col_widths[1], 8, row[1], 1, 1, 'L', 0)
    pdf.output(output_path) 