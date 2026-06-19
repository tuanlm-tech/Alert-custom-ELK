from pathlib import Path
from datetime import datetime

from utils.email_service import send_email

BASE_DIR = Path(__file__).resolve().parent.parent

css = (
    BASE_DIR
    / "templates"
    / "css"
    / "email_style.css"
).read_text(encoding="utf-8")

html = (
    BASE_DIR
    / "templates"
    / "email_template.html"
).read_text(encoding="utf-8")

html = html.replace("{{CSS}}", css)

html = html.replace("{{COMMAND}}", "ssh")
html = html.replace("{{ACTION}}", "failed_login")
html = html.replace("{{TIME}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
html = html.replace("{{SEVERITY}}", "HIGH")
html = html.replace(
    "{{DESCRIPTION}}",
    "Multiple SSH login failures detected."
)
html = html.replace(
    "{{KIBANA_URL}}",
    "https://kibana.mk.com.vn"
)

send_email(
    subject="[SIEM AUDIT] SSH LOGIN FAILED",
    body=html,
    to_email="tuanlm@mksmart.com.vn",
    is_html=True
)