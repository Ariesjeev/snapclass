import hashlib
import secrets
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from urllib.parse import urlencode

import streamlit as st

from src.database.db import (
    create_recovery_token,
    get_teacher_by_email,
    get_valid_recovery_token,
    update_teacher_password,
    use_recovery_token,
)


def _setting(name, default=None):
    value = st.secrets.get(name, default)
    return value.strip() if isinstance(value, str) else value


def _token_hash(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _recovery_url(token_type, token):
    base_url = _setting("APP_URL", "http://localhost:8501").rstrip("/")
    query = urlencode({"recovery": token_type, "token": token})
    return f"{base_url}/?{query}"


def _send_email(recipient, subject, body):
    smtp_host = _setting("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(_setting("SMTP_PORT", 587))
    smtp_username = _setting("SMTP_USERNAME")
    smtp_password = _setting("SMTP_PASSWORD")
    sender = _setting("SMTP_FROM", smtp_username)

    if not smtp_username or not smtp_password:
        raise RuntimeError("SMTP_USERNAME and SMTP_PASSWORD are not configured")

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient
    message.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)


def send_username_recovery(email):
    teacher = get_teacher_by_email(email.strip().lower())
    if not teacher:
        return False

    raw_token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    create_recovery_token(teacher["teacher_id"], _token_hash(raw_token), "username", expires_at.isoformat())
    link = _recovery_url("username", raw_token)
    _send_email(
        email,
        "Your SnapClass username",
        f"Your SnapClass username is: {teacher['username']}\n\nView it securely here: {link}\nThis link expires in 30 minutes.",
    )
    return True


def send_password_recovery(email):
    teacher = get_teacher_by_email(email.strip().lower())
    if not teacher:
        return False

    raw_token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    create_recovery_token(teacher["teacher_id"], _token_hash(raw_token), "password", expires_at.isoformat())
    link = _recovery_url("password", raw_token)
    _send_email(
        email,
        "Reset your SnapClass password",
        f"Reset your password using this secure link:\n{link}\n\nThis link expires in 30 minutes and can only be used once.",
    )
    return True


def get_recovery_request(token_type, raw_token):
    if token_type not in {"username", "password"} or not raw_token:
        return None
    return get_valid_recovery_token(_token_hash(raw_token), token_type)


def reset_password(token_id, teacher_id, password):
    if not update_teacher_password(teacher_id, password):
        return False
    return use_recovery_token(token_id)
