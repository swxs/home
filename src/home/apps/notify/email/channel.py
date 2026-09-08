# -*- coding: utf-8 -*-

import smtplib
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import home.core as core


@dataclass
class SmtpConfig:
    host: str
    port: int
    user: str
    password: str
    from_addr: str
    from_name: str
    use_tls: bool


def load_smtp_config() -> SmtpConfig:
    return SmtpConfig(
        host=core.config.MAIL_SERVER_IP,
        port=core.config.MAIL_SERVER_PORT,
        user=core.config.MAIL_SERVER_USER,
        password=core.config.MAIL_SERVER_PASSWORD,
        from_addr=core.config.MAIL_SERVER_USER_MAIL,
        from_name=core.config.MAIL_SENDER_NAME,
        use_tls=core.config.MAIL_USE_TLS,
    )


def send_email(to: str, subject: str, html_body: str, text_body: str) -> None:
    cfg = load_smtp_config()
    if not cfg.host or not cfg.from_addr:
        raise RuntimeError("邮件服务未配置")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{cfg.from_name} <{cfg.from_addr}>"
    msg["To"] = to
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP(cfg.host, cfg.port, timeout=30) as server:
        if cfg.use_tls:
            server.starttls()
        if cfg.user and cfg.password:
            server.login(cfg.user, cfg.password)
        server.sendmail(cfg.from_addr, [to], msg.as_string())
