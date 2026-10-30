from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Mailing
from .services import send_mailing

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'

class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'

class MailingCreateView(CreateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'message', 'recipients', 'owner']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailing-list')

class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'message', 'recipients', 'owner']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailing-list')

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing-list')

def send_mailing_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    if request.method == 'POST':
        try:
            send_mailing(pk)  # из services.py
            messages.success(request, f'Рассылка #{pk} успешно запущена.')
        except PermissionError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'Ошибка при отправке: ' + str(e))

        return redirect('mailing-detail', pk=mailing.pk)

    return render(request, 'mailings/mailing_send_confirm.html', {'mailing': mailing})
