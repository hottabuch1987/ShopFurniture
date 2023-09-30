from django.urls import path

from .views import *

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('activate/', ActivateProfile.as_view(), name='activate'),
    path('profile/', Profile.as_view(), name='profile'),
    path('logout/', logout_user, name='logout'),
    path('delete/<int:pk>/', DeleteProfile.as_view(), name='delete'),
    path('edit/<int:pk>/', EditProfile.as_view(), name='edit'),
    path('profile/cart/', Profile.as_view(), name='profile'),
    path('create_review/', CreateReviewView.as_view(), name='create_review'),

]