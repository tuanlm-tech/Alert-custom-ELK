import os
import smtplib

from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 25))
SMTP_DOMAIN = os.getenv("SMTP_DOMAIN")
FROM_EMAIL = os.getenv("FROM_EMAIL")


def send_email(
    subject: str,
    body: str,
    to_email: str,
    is_html: bool = False
) -> bool:

    server = None

    try:
        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        )

        server.ehlo(SMTP_DOMAIN)

        msg = MIMEText(
            body,
            "html" if is_html else "plain",
            "utf-8"
        )

        msg["Subject"] = subject
        msg["From"] = f"elk-notification <{FROM_EMAIL}>"
        msg["To"] = to_email

        server.sendmail(
            FROM_EMAIL,
            [to_email],
            msg.as_string()
        )

        return True

    except Exception as e:
        print(f"Send email error: {e}")
        return False

    finally:
        if server:
            server.quit()