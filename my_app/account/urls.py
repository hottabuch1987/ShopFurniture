from django.urls import path

from .views import CreateReviewView

urlpatterns = [
    path('create_review/', CreateReviewView.as_view(), name='create_review'),

]