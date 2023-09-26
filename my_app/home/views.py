from django.conf import settings
from django.views import View
from home.models import Product, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from account.forms import ReviewsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from .models import Product, Category, Feedback

from .forms import ContactForm
from .utils import DataMixin
from django.db.models import Q
from unidecode import unidecode



class HomePage(ListView):
    """Главная"""
    model = Category
    template_name = 'my_app/fitnes/index.html'
    context_object_name = 'category'
    extra_context = {'title': 'Главная'}


class About(ListView):
    """О нас"""
    model = Product
    template_name = 'my_app/fitnes/about.html'
    context_object_name = 'products'
    extra_context = {'title': 'О нас'}


class Products(DataMixin, ListView):
    """Все продукты"""
    model = Product
    template_name = 'my_app/fitnes/product.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Navien')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class Contact(DataMixin, CreateView):
    """Контакты"""
    form_class = ContactForm
    template_name = 'my_app/fitnes/contact.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Консультация')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class ShowProduct(DataMixin, DetailView):
    """Продукт"""
    model = Product
    template_name = 'my_app/fitnes/detail.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'products'
    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['products'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class ShowCategory(DataMixin, ListView):
    """Категория"""
    model = Product
    template_name = 'my_app/fitnes/category.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория | ' + str(context['products'][0].category))
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'], )


class Search(ListView):
    """Поиск"""
    model = Product
    template_name = 'my_app/fitnes/search.html'

    def get_queryset(self):
        search_term = self.request.GET.get("q")

        # Преобразование русских символов в транслитерацию
        search_term_translit = unidecode(search_term)

        # Поиск с учетом транслитерации и русских слов
        queryset = Product.objects.filter(Q(name__icontains=search_term) | Q(name__icontains=search_term_translit) | Q(name__icontains=search_term))
        return queryset








class AddToCartView(View):
    """Добавление в корзину"""
    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)

        # Получаем или создаем пустую корзину для пользователя
        cart = request.session.get('cart', {})
        cart.setdefault(product_slug, {'quantity': 0, 'price': float(product.price)})

        # Увеличиваем количество товара в корзине
        cart[product_slug]['quantity'] += 1
        request.session['cart'] = cart

        return redirect('cart')


class RemoveFromCartView(View):
    """Удаление с корзины"""
    def get(self, request, product_slug):
        # Получаем корзину пользователя
        cart = request.session.get('cart', {})

        # Уменьшаем количество товара в корзине
        if product_slug in cart:
            cart[product_slug]['quantity'] -= 1
            if cart[product_slug]['quantity'] <= 0:
                del cart[product_slug]
            request.session['cart'] = cart

        return redirect('cart')


# 



class CartView(View):
    """Инициализация корзины"""
    def get(self, request):
        # Получаем корзину пользователя
        cart = request.session.get('cart', {})

        # Создаем переменные для подсчета количества и общей цены
        total_quantity = 0
        total_price = 0

        # Обходим все товары в корзине и увеличиваем значения количества и цены
        for item in cart.values():
            total_quantity += item['quantity']
            total_price += item['quantity'] * item['price']

        return render(request, 'my_app/fitnes/cart.html', {'cart': cart, 'total_quantity': total_quantity, 'total_price': total_price, 'products': Product.objects.all()})

    def post(self, request):
        cart = request.session.get('cart', {})
        cart_items = {}
        for product_id, item in cart.items():
            cart_items[product_id] = item['quantity']

        form = ReviewsForm(request.POST, initial={'cart': cart_items})

        if form.is_valid():
            review = form.save(commit=False)
            review.product = Product.objects.get(pk=form.cleaned_data['product'])
            review.save()

            # Удаление ключа 'cart' из сессии
            del request.session['cart']

            # Вывод флэш-сообщения
            messages.success(request, 'Заказ успешно отправлен.')

            return redirect('products')

        return render(request, 'account/create_review.html', {'form': form})


# 
