from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('users/', views.get_users),
    path('users/<int:id>/',views.single_user)
]