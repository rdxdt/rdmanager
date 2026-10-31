import hashlib
import hmac
import time

from flask import render_template, url_for
from flask_mail import Message

from rdmanager import app, mail

RESET_CODE_MINUTES = 15


def reset_code(user, window=None):
    if window is None:
        window = int(time.time() // (RESET_CODE_MINUTES * 60))
    # Including the password hash invalidates the code once the password changes
    message = f"{user.id}:{user.password_hash}:{window}".encode()
    key = app.config["SECRET_KEY"].encode()
    digest = hmac.new(key, message, hashlib.sha256).digest()
    return f"{int.from_bytes(digest[:4], 'big') % 1_000_000:06d}"


def verify_reset_code(user, code):
    window = int(time.time() // (RESET_CODE_MINUTES * 60))
    # The previous window is accepted so a code sent near the end of one stays valid
    return any(
        hmac.compare_digest(reset_code(user, w), code) for w in (window, window - 1)
    )


def send_reset_email(user):
    code = reset_code(user)
    link = url_for("main.reset_verify", email=user.email, code=code, _external=True)
    msg = Message("RD Manager password recovery", recipients=[user.email])
    msg.body = render_template(
        "main/email/reset_password.txt",
        user=user,
        code=code,
        link=link,
        minutes=RESET_CODE_MINUTES,
    )
    mail.send(msg)
