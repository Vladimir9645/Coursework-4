from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import MessageTemplate

class MessageTemplateListView(ListView):
    model = MessageTemplate
    template_name = 'mail_templates/template_list.html'
    context_object_name = 'templates'

class MessageTemplateDetailView(DetailView):
    model = MessageTemplate
    template_name = 'mail_templates/template_detail.html'
    context_object_name = 'template'

class MessageTemplateCreateView(CreateView):
    model = MessageTemplate
    fields = ['subject', 'body']
    template_name = 'mail_templates/template_form.html'
    success_url = reverse_lazy('template-list')

class MessageTemplateUpdateView(UpdateView):
    model = MessageTemplate
    fields = ['subject', 'body']
    template_name = 'mail_templates/template_form.html'
    success_url = reverse_lazy('template-list')

class MessageTemplateDeleteView(DeleteView):
    model = MessageTemplate
    template_name = 'mail_templates/template_confirm_delete.html'
    success_url = reverse_lazy('template-list')
