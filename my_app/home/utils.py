from django.db.models import Count
from django.core.cache import cache
from .models import Category

menu = [{'title': 'Мы', 'url_name': 'about'},
        {'title': 'Каталог', 'url_name': 'catalog'},
        {'title': 'Отзывы', 'url_name': 'reviews'},
        {'title': 'Контакты', 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 6

    def get_user_context(self, **kwargs):
        context = kwargs
        # category = cache.get('category')
        # if not category:
            # category = Category.objects.annotate(Count('products'))
            # cache.set('category', category, 60)

        context['menu'] = menu
        # context['category'] = category
        return context
