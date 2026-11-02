import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Mailing
from .services import send_mailing


class OwnerOrManagerMixin(LoginRequiredMixin):
    """
    Разрешает доступ, если пользователь — владелец рассылки или менеджер.
    Предполагается, что у пользователя есть атрибут role: 'manager' или иное.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Если пользователь не авторизован, LoginRequiredMixin уже редиректит
        if user.role == "manager":
            return queryset
        return queryset.filter(owner=user)


class MailingListView(OwnerOrManagerMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'


class MailingDetailView(OwnerOrManagerMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    # owner убираем из fields — он будет установлен автоматически
    fields = ['start_time', 'end_time', 'message', 'recipients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailing-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(OwnerOrManagerMixin, UpdateView):
    model = Mailing
    # owner не включаем в редактируемые поля
    fields = ['start_time', 'end_time', 'message', 'recipients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailing-list')


class MailingDeleteView(OwnerOrManagerMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing-list')


@login_required
def send_mailing_view(request, pk):
    # Сначала фильтруем через логику OwnerOrManager, чтобы нельзя было отправить чужую рассылку
    queryset = Mailing.objects.all()
    user = request.user

    if user.role != "manager":
        queryset = queryset.filter(owner=user)

    mailing = get_object_or_404(queryset, pk=pk)

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

