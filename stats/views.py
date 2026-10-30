from django.shortcuts import render
from django.core.cache import cache
from django.utils import timezone
from mailings.models import Mailing, SendingAttempt
from clients.models import Recipient
from django.db.models import Count, Q

def dashboard(request):
    cache_key = 'dashboard_stats'
    stats = cache.get(cache_key)

    if stats is None:
        now = timezone.now()
        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(start_time__lte=now, end_time__gte=now).count()
        unique_recipients = Recipient.objects.count()

        attempts_stats = SendingAttempt.objects.aggregate(
            success_count=Count('id', filter=Q(status='success')),
            failed_count=Count('id', filter=Q(status='failed')),
        )

        stats = {
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_recipients': unique_recipients,
            'success_count': attempts_stats['success_count'],
            'failed_count': attempts_stats['failed_count'],
        }
        cache.set(cache_key, stats, 60)  # кэш на 60 секунд

    return render(request, 'stats/dashboard.html', stats)

