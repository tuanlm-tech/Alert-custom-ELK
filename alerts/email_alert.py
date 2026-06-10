import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp-relay.gmail.com"
SMTP_PORT = 25
SMTP_DOMAIN = "mk.com.vn"

FROM_EMAIL = "elk-notification@mk.com.vn"
TO_EMAIL = "tuanlm@mksmart.com.vn"

SUBJECT = "[SIEM AUDIT] TEST LOGIN FAILED"

BODY = """
Canh bao SIEM

Command : ssh
Action  : failed_login

Co nhieu lan dang nhap that bai.
"""

try:
    # Ket noi SMTP
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    # Tuong duong domain => "mk.com.vn"
    server.ehlo(SMTP_DOMAIN)

    # Tao email
    msg = MIMEText(BODY)

    msg["Subject"] = SUBJECT
    msg["From"] = f"elk-notification <{FROM_EMAIL}>"
    msg["To"] = TO_EMAIL

    # Gui mail
    server.sendmail(FROM_EMAIL, [TO_EMAIL], msg.as_string())

    print("Gui email thanh cong")

except Exception as e:
    print("Loi gui email:", e)

finally:
    server.quit()