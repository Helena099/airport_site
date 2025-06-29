from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_booking_confirmation(passenger):
    """Send booking confirmation email to passenger."""
    subject = "Confirmation de réservation"
    html_msg = render_to_string(
        "airport/emails/booking_confirmation.html",
        {"p": passenger}
    )
    send_mail(
        subject=subject,
        message="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[f"{passenger.passport_number}@example.com"],  # FIXME: replace with real email
        html_message=html_msg,
        fail_silently=False,
    )
