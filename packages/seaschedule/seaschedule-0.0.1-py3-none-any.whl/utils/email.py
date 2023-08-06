import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path


def send_mail(host: str, port: int, from_addr: str, to_addrs: str, cc_addrs: str,
              subject: str, body: str, files: list) -> None:
    msg = MIMEMultipart()
    msg["from"] = from_addr
    msg["to"] = to_addrs
    if cc_addrs: msg["cc"] = cc_addrs
    msg["subject"] = subject
    msg.attach(MIMEText(body, "html"))
    for file in files:
        with open(file, "rb") as f:
            attachment = MIMEApplication(f.read())
            attachment.add_header("Content-Disposition", "attachment", filename=Path(file).name)
            msg.attach(attachment)

    with smtplib.SMTP(host=host, port=port) as smtp:
        smtp.send_message(msg)
