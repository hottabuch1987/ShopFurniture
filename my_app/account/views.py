from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.views import View
from .forms import  ReviewsForm
from django.contrib import messages
from .forms import RegisterUserForm, LoginUserForm, EditForm, ActivateProfileForm
from django.urls import reverse_lazy
from home.utils import DataMixin
from django.views.generic import CreateView, UpdateView, FormView
from account.models import User
from .tasks import send_registration_email
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView
import random
import string

from django.core.mail import send_mail
class RegisterUser(FormView):
    form_class = RegisterUserForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        auth_code = ''.join(random.choices(string.digits, k=6))
        user = form.save(commit=False)
        user.auth_code = auth_code
        user.save()
        
        send_mail(
            'Активация профиля',
            f'Ваш код активации: {auth_code}',
            'varvar1987a@mail.ru',
            [email],
            fail_silently=False,
        )
        return redirect('activate')



class ActivateProfile(FormView):
    form_class = ActivateProfileForm
    template_name = 'account/registration.html'

        
    def form_valid(self, form):
        auth_code = form.cleaned_data['auth_code']
        
        try:
            user = User.objects.get(auth_code=auth_code)
            user.auth_code == auth_code

        except User.DoesNotExist:
            return redirect('register')

        user.is_active = True
        user.save()
        return redirect('login')


    
    



class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'account/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Войти")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('profile')


def logout_user(request):
    logout(request)
    return redirect('login')


class Profile(DataMixin, View):
    template_name = 'account/profile.html'

    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            return render(request, self.template_name, {'user': user})
        else:
            return redirect('login')


class EditProfile(UpdateView):
    model = User
    form_class = EditForm
    template_name_suffix = '-edit'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        avatar = form.cleaned_data.get('avatar')
        user = self.request.user
        user.avatar = avatar
        user.save()
        return super().form_valid(form)


class DeleteProfile(DeleteView):
    model = User
    template_name_suffix = '-delete'
    success_url = reverse_lazy('login')


class CreateReviewView(View):
    def get(self, request):
        form = ReviewsForm()
        return render(request, 'account/create_review.html', {'form': form})

    def post(self, request):
        cart = request.session.get('cart', {})
        form = ReviewsForm(request.POST, initial={'product': cart})

        if form.is_valid():
            review = form.save(commit=False)
            review.product = cart
            review.save()
            # Очистка сессии
            request.session.flush()
            # Вывод флэш-сообщения
            messages.success(request, 'Заказ успешно отправлен.')

            return redirect('products')

        return render(request, 'account/create_review.html', {'form': form})



