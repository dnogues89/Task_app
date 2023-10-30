import smtplib, ssl
from api.key_espasa_api import mail_password

port = 587  # For starttls
smtp_server = "mail.backoffice.com.ar"
sender_email = "espasadocu@espasa.com.ar"
receiver_email = "dnogues@espasa.com.ar"
password = mail_password
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)