from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserAPIView.as_view(), name='user-list-create'),
    path('<str:email>/', views.UserAPIView.as_view(), name='user-detail-update-delete'),
]
