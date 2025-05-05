# utils/email.py

from django.core.mail import send_mail
from django.conf import settings
from django.core.signing import TimestampSigner


def send_email(subject, message, from_email, to_email):
    to_email = to_email if isinstance(to_email, list) else [to_email]
    send_mail(subject, message, from_email, to_email)


def send_verification_email(request, user):
    signer = TimestampSigner()
    signed_code = signer.sign(user.email)

    verify_url = request.build_absolute_uri(f"/users/verify-email/?code={signed_code}")
    subject = "[MyApp] 이메일 인증"
    message = f"{user.name}님, 안녕하세요!\n\n이메일 인증을 위해 아래 링크를 클릭해주세요:\n\n{verify_url}"

    send_email(subject, message, settings.EMAIL_HOST_USER, user.email)
