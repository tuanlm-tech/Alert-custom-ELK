import re
import time

from pathlib import Path
from datetime import datetime

from connections.elasticsearch_connection import es
from utils.email_service import send_email


# =========================
# CONFIG
# =========================

TO_EMAILS = [
    "tuanlm@mksmart.com.vn",
    "admin@mksmart.com.vn",
    # "soc@mksmart.com.vn",
]

EMAIL_SUPPRESS_SECONDS = 180
EMAIL_BATCH_SECONDS = 60

last_timestamp = None

# alert_key -> last_sent_time
message_cache = {}

# danh sách alert chờ gửi
pending_alerts = []

last_email_time = time.time()

BASE_DIR = Path(__file__).resolve().parent.parent

html_template = (
    BASE_DIR
    / "templates"
    / "email_template.html"
).read_text(encoding="utf-8")


# =========================
# HELPER
# =========================

def get_index_name():
    return (
        "kiosk-log-ssh_login-"
        + datetime.now().strftime("%Y.%m.%d")
    )


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

    # fallback
    return re.sub(
        r"port\s+\d+",
        "port:*",
        message
    )


def send_batch_email(alerts):
    if not alerts:
        return

    description = "<br><br>".join(alerts)

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
        description
    )

    html = html.replace(
        "{{KIBANA_URL}}",
        "http://10.30.137.11"
    )

    success_count = 0

    for email in TO_EMAILS:

        success = send_email(
            subject=f"[SIEM AUDIT] SSH LOGIN ({len(alerts)} Events)",
            body=html,
            to_email=email,
            is_html=True
        )

        if success:
            success_count += 1

    print(
        f"Batch email sent "
        f"({len(alerts)} alerts, "
        f"{success_count}/{len(TO_EMAILS)} recipients)"
    )


# =========================
# MAIN LOOP
# =========================

while True:

    try:

        INDEX_NAME = get_index_name()

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
                {
                    "@timestamp": "asc"
                }
            ],
            query=query
        )

        hits = response["hits"]["hits"]

        current_time = time.time()

        # =========================
        # Xóa cache hết hạn
        # =========================

        expired_keys = [
            key
            for key, ts in message_cache.items()
            if current_time - ts > EMAIL_SUPPRESS_SECONDS
        ]

        for key in expired_keys:
            del message_cache[key]

        # =========================
        # Xử lý log mới
        # =========================

        for hit in hits:

            source = hit["_source"]

            message = source.get(
                "message",
                ""
            )

            timestamp = source.get(
                "@timestamp"
            )

            last_timestamp = timestamp

            alert_key = build_alert_key(
                message
            )

            # chống gửi trùng
            if alert_key in message_cache:
                continue

            print(
                f"[NEW ALERT] {alert_key}"
            )

            pending_alerts.append(
                f"{timestamp}<br>{message}"
            )

            message_cache[
                alert_key
            ] = current_time

        # =========================
        # Gửi email theo batch
        # =========================

        if (
            pending_alerts
            and current_time - last_email_time
            >= EMAIL_BATCH_SECONDS
        ):

            send_batch_email(
                pending_alerts
            )

            pending_alerts.clear()

            last_email_time = current_time

        time.sleep(0.2)

    except Exception as e:

        print(
            f"Error: {e}"
        )

        time.sleep(1)