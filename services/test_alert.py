import re
import time

from pathlib import Path
from datetime import datetime

from connections.elasticsearch_connection import es
from utils.email_service import send_email

INDEX_NAME = "kiosk-log-ssh_login-2026.06.19"

TO_EMAIL = "tuanlm@mksmart.com.vn"

# Chống gửi email trùng trong 3 phút
EMAIL_SUPPRESS_SECONDS = 180

last_timestamp = None

# alert_key -> last_sent_time
message_cache = {}

BASE_DIR = Path(__file__).resolve().parent.parent

html_template = (
    BASE_DIR
    / "templates"
    / "email_template.html"
).read_text(encoding="utf-8")


def build_alert_key(message: str) -> str:
    """
    Ví dụ:

    Jun 19 15:39:23 kiosk-api-02 sshd[228629]:
    Accepted password for tuanlm from 10.30.102.44 port 61815 ssh2

    =>
    kiosk-api-02|tuanlm|10.30.102.44
    """

    pattern = (
        r"^\w+\s+\d+\s+\d+:\d+:\d+\s+"
        r"(\S+)\s+"
        r".*for\s+(\S+)\s+"
        r"from\s+(\d+\.\d+\.\d+\.\d+)"
    )

    match = re.search(pattern, message)

    if match:
        hostname = match.group(1)
        username = match.group(2)
        src_ip = match.group(3)

        return f"{hostname}|{username}|{src_ip}"

    # fallback nếu parse lỗi
    return re.sub(
        r"port\s+\d+",
        "port:*",
        message
    )


while True:
    try:

        query = {"match_all": {}}

        if last_timestamp:
            query = {
                "range": {
                    "@timestamp": {
                        "gt": last_timestamp
                    }
                }
            }

        response = es.search(
            index=INDEX_NAME,
            size=1000,
            sort=[
                {"@timestamp": "asc"}
            ],
            query=query
        )

        hits = response["hits"]["hits"]

        current_time = time.time()

        # Xóa cache quá hạn
        expired_keys = [
            key
            for key, ts in message_cache.items()
            if current_time - ts > EMAIL_SUPPRESS_SECONDS
        ]

        for key in expired_keys:
            del message_cache[key]

        for hit in hits:

            source = hit["_source"]

            message = source.get("message", "")
            timestamp = source.get("@timestamp")

            last_timestamp = timestamp

            alert_key = build_alert_key(message)

            # Đã gửi email trong vòng 3 phút
            if alert_key in message_cache:
                continue

            print(message)
            print(f"ALERT_KEY: {alert_key}")

            html = html_template

            html = html.replace(
                "{{COMMAND}}",
                "ssh"
            )

            html = html.replace(
                "{{ACTION}}",
                "login"
            )

            html = html.replace(
                "{{TIME}}",
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            html = html.replace(
                "{{SEVERITY}}",
                "HIGH"
            )

            html = html.replace(
                "{{DESCRIPTION}}",
                message
            )

            html = html.replace(
                "{{KIBANA_URL}}",
                "https://kibana.mk.com.vn"
            )

            success = send_email(
                subject="[SIEM AUDIT] SSH LOGIN",
                body=html,
                to_email=TO_EMAIL,
                is_html=True
            )

            if success:

                print(
                    f"Email sent ({alert_key})"
                )

                message_cache[alert_key] = current_time

        time.sleep(0.2)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)