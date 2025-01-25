import random


def generate_otp() -> str:
    """
    Generate a random 4 digit OTP
    """
    return str(random.randint(1000, 9999))
