from django.urls import path
from api import views

urlpatterns = [
    path('create/', views.Create.as_view()),
    path('delete/', views.Delete.as_view()),
    path('auth/', views.Auth.as_view()),
    path('callback/', views.Callback.as_view(), name='googleauth_callback'),
]