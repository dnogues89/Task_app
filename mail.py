from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

msg = MIMEMultipart()
msg["From"] = "espasadocu@espasa.com.ar"
msg["To"] = "damiannogues@gmail.com"
body_text = "HOLA MUNDO :)"
body_part = MIMEText(body_text, 'plain')
msg.attach(body_part)
with smtplib.SMTP_SSL('mail.backoffice.com.ar', '587') as smtp:

        smtp.login('espasadocu@espasa.com.ar', 'Ed2210')

        subject = "Message from python"
        msg = "Hello from python"

        smtp.sendmail('espasadocu@espasa.com.ar', 'damiannogues@gmail.com', msg)

print("¡Datos enviados con éxito!")

