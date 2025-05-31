import smtplib
from email.message import EmailMessage

def send_email_with_attachment(subject, body, to, attachment_path, from_addr, from_pass):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to
    msg.set_content(body)

    # Załącznik
    with open(attachment_path, 'rb') as f:
        file_data = f.read()
        file_name = attachment_path.split('/')[-1]
    msg.add_attachment(file_data, maintype='image', subtype='png', filename=file_name)

    # Wysyłka przez Interia SMTP
    with smtplib.SMTP('mail.m160.mikr.dev', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(from_addr, from_pass)
        smtp.send_message(msg)