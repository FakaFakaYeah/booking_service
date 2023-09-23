import smtplib

from pydantic import EmailStr

from app.core import settings
from app.models import Bookings
from app.tasks.email_templates import create_booking_confirmation_template


def send_booking_confirmation_email(
        booking: Bookings,
        email_to: EmailStr,
):
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
