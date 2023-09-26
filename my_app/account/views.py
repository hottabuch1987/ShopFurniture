from django.shortcuts import redirect, render
from django.views import View
from .forms import  ReviewsForm
from django.contrib import messages

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



