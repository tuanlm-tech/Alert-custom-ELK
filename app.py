from pathlib import Path

html = Path(
    "templates/email_template.html"
).read_text(encoding="utf-8")

html = html.replace("{{RULE_NAME}}", "SSH Failed Login")
html = html.replace("{{SEVERITY}}", "HIGH")
html = html.replace("{{SOURCE_IP}}", "10.10.10.5")
html = html.replace("{{USERNAME}}", "root")
html = html.replace("{{COUNT}}", "25")
html = html.replace("{{TIME}}", "2026-06-19 14:30:00")
html = html.replace(
    "{{DESCRIPTION}}",
    "Multiple failed SSH login attempts detected."
)
html = html.replace(
    "{{KIBANA_URL}}",
    "https://kibana.company.local"
)

msg = MIMEText(html, "html", "utf-8")