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


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'account/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')

        # send_registration_email.delay(username, email)
        return redirect('activate')


class ActivateProfile(FormView):
    form_class = ActivateProfileForm
    template_name = 'account/registration.html'


    def form_valid(self, form):
        auth_code = ''.join(random.choices(string.digits, k=6))

        send_registration_email.delay(auth_code)
        return redirect('profile')
    
    
    
    



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
        user = User.objects.get(id=request.user.id)
        return render(request, self.template_name, {'user': user})


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



