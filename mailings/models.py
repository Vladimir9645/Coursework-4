import datetime
from django.db import models
from django.utils import timezone
from accounts.models import User
from mail_templates.models import MessageTemplate
from clients.models import Recipient

class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(MessageTemplate, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient, related_name='mailings')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='own_mailings')

    def update_status(self):
        now = timezone.now()
        if now < self.start_time:
            new_status = 'created'
        elif now <= self.end_time:
            new_status = 'running'
        else:
            new_status = 'completed'

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=['status'])

    def can_send_now(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def __str__(self):
        return f"Mailing #{self.id} — {self.message.subject}"


class SendingAttempt(models.Model):
    ATTEMPT_STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='attempts')
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ATTEMPT_STATUS_CHOICES)
    server_response = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-attempt_time']

