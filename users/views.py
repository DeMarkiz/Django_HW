from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.core.mail import send_mail
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from .models import CustomUser


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('catalog:product_list')  # Перенаправление после успешной регистрации

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)

        # Отправка приветственного письма
        send_mail(
            'Добро пожаловать!',
            'Спасибо за регистрацию на нашем сайте.',
            'noreply@example.com',
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)
