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
smtp = config['SMTP']
port = config['PORT']

message = MIMEMultipart("alternative")
message["Subject"] = "Alterações"
message["From"] = sender_email
message["To"] = receiver_email

def send(listFollowers, listFollowins, newFollowers, newFollowins, user):
    followins = """ """
    followers = """ """
    html  = """
    <html>
    <body>
        <p>Olá<br>
        Há novas atualizações de """ + user + """:<br>"""
    if newFollowins > 0:
       followins = """Começou a seguir:""" + str(listFollowins) + """ <br>"""
    elif newFollowins < 0:
       followins = """Deixou de seguir:""" + str(listFollowins) + """ <br>"""
    
    if newFollowins > 0:
       followers = """Começou a ser seguido por:""" + str(listFollowers) + """ </p>"""
    elif newFollowins < 0:
       followers = """Diexou de ser seguido por:""" + str(listFollowers) + """ </p>"""

    fim = """</body>
    </html>
    """
    completeHtml = html + followins + followers + fim
    part2 = MIMEText(completeHtml, "html")
    message.attach(part2)
   
    if (newFollowers != 0 or newFollowins != 0):      
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
            print("enviou")