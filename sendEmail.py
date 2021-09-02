import smtplib, ssl
from dotenv import dotenv_values
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

config = dotenv_values(".env")
smtp_server = "smtp.gmail.com"
port = 587  # For starttls

sender_email = config['EMAIL_SENDER']
password = config['EMAIL_PASSWORD']
receiver_email = config['EMAIL_RECEIVE']

message = MIMEMultipart("alternative")
message["Subject"] = "Alterações"
message["From"] = sender_email
message["To"] = receiver_email

def send(listFollowers, listFollowins, newFollowers, newFollowins, user):
    html  = """
    <html>
    <body>
        <p>Olá<br>
        Há novas atualizações de """ + user + """:<br>
        Começou a seguir:""" + str(listFollowins) + """ <br>
        Começou a ser seguido por:""" + str(listFollowers) + """ </p>
    </body>
    </html>
    """
  
    part2 = MIMEText(html, "html")
    message.attach(part2)

    if (newFollowers or newFollowins):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.kinghost.net", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )