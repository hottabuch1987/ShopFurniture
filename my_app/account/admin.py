from django.contrib import admin
from .models import User, Reviews


admin.site.register(User)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'tel', 'product']
    prepopulated_fields = {'name': ('tel',)}
    list_filter = ['name', 'tel']
    search_fields = ('name', 'tel', 'product')
  
