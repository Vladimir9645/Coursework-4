from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Recipient

class RecipientListView(ListView):
    model = Recipient
    template_name = 'clients/recipient_list.html'
    context_object_name = 'recipients'

class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'clients/recipient_detail.html'
    context_object_name = 'recipient'

class RecipientCreateView(CreateView):
    model = Recipient
    fields = ['email', 'full_name', 'comment']
    template_name = 'clients/recipient_form.html'
    success_url = reverse_lazy('recipient-list')

class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ['email', 'full_name', 'comment']
    template_name = 'clients/recipient_form.html'
    success_url = reverse_lazy('recipient-list')

class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'clients/recipient_confirm_delete.html'
    success_url = reverse_lazy('recipient-list')
