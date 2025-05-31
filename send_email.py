import smtplib
from email.message import EmailMessage
import mimetypes

def send_email_with_attachment(subject, body, to, attachments, from_addr, from_pass):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to
    msg.set_content(body)

    # Obsługa wielu załączników
    for attachment_path in attachments:
        ctype, encoding = mimetypes.guess_type(attachment_path)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = attachment_path.split('/')[-1]
        msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)

    # Wysyłka przez Interia SMTP
    with smtplib.SMTP('mail.m160.mikr.dev', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(from_addr, from_pass)
        smtp.send_message(msg)