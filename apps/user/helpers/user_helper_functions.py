import threading
from datetime import timedelta

from decouple import config
from django.core.mail import send_mail

from utils.common_utils import generate_otp
from utils.datetime_utils import get_current_utc_datetime


def set_user_otp(instance):
    instance.otp = generate_otp()
    instance.otp_expiry = get_current_utc_datetime() + timedelta(minutes=int(config("OTP_VALIDITY")))
    return instance


def send_otp_via_thread(instance):
    thread = threading.Thread(target=send_otp_verification_email, args=(instance,), name="SendOTPThread")
    thread.start()


def send_otp_verification_email(instance):
    try:
        if not int(config("MOCK_SEND_EMAIL")):
            recipient_list = [instance.email]
            if int(config("IS_DIVERT_EMAIL")):
                recipient_list = [str(config("DEFAULT_TO_EMAIL"))]
            send_mail(
                subject="OTP Verification",
                message=f"Your OTP is {instance.otp} and will expire in {str(config('OTP_VALIDITY'))} minutes.",
                from_email=str(config("EMAIL_HOST_USER")),
                recipient_list=recipient_list,
                fail_silently=False,
            )
    except Exception as e:
        print(f"Failed to send OTP email: {e}")
