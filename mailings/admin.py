from django.contrib import admin
from .models import Mailing, SendingAttempt

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'status', 'owner')
    list_filter = ('status', 'owner')

@admin.register(SendingAttempt)
class SendingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'recipient', 'attempt_time', 'status')
    list_filter = ('status',)
    readonly_fields = ('attempt_time',)
