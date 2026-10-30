from django.core.mail import send_mail
from django.conf import settings
from .models import SendingAttempt

def send_mailing(mailing_id):
    from .models import Mailing, Recipient
    mailing = Mailing.objects.get(pk=mailing_id)

    if not mailing.can_send_now():
        raise PermissionError("Отправка вне разрешённого временного окна.")

    for recipient in mailing.recipients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
            )
            status = 'success'
            response = "OK"
        except Exception as e:
            status = 'failed'
            response = str(e)

        SendingAttempt.objects.create(
            mailing=mailing,
            recipient=recipient,
            status=status,
            server_response=response,
        )
