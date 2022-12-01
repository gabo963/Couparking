from django.urls import path, include
from coupark import views

# Template URLs
app_name = 'coupark'

urlpatterns = [
    path('register/', views.register, name='register' ),
    path('user_login/', views.user_login, name='user_login'),
]
