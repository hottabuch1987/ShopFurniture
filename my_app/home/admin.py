from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Category, Feedback

admin.site.site_title = 'Администрация'
admin.site.site_header = 'Администрация'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name',  'slug']
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name', 'date_added', 'slug']
    search_fields = ('name', 'price', 'date_added')
    prepopulated_fields = {'slug':('name',)}



admin.site.register(Feedback)


