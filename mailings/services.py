from django.conf import settings
from django.core.mail import send_mail

from .models import Mailing, SendingAttempt


def send_mailing(mailing_id: int) -> None:
    mailing = (
        Mailing.objects.select_related("message")
        .prefetch_related("recipients")
        .get(pk=mailing_id)
    )

    if not mailing.can_send_now():
        raise PermissionError("Отправка вне разрешённого временного окна.")

    attempts = []
    for recipient in mailing.recipients.all():
        try:
            sent_count = send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            status = "success" if sent_count else "failed"
            response = "OK" if sent_count else "Письмо не отправлено"
        except Exception as error:
            status = "failed"
            response = str(error)

        attempts.append(
            SendingAttempt(
                mailing=mailing,
                recipient=recipient,
                status=status,
                server_response=response,
            )
        )

    SendingAttempt.objects.bulk_create(attempts)