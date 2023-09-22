import smtplib
import requests

from pydantic import EmailStr


from app.core import settings
from app.tasks.celery import celery
from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def send_booking_confirmation_email(
        booking_id: int,
        email_to: EmailStr
):
    booking = requests.get(f'http://127.0.0.1:8000/bookings/{booking_id}')
    msg_content = create_booking_confirmation_template(booking.json(), email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
