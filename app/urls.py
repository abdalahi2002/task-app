from django.urls import path
from . import views

urlpatterns = [
    path("projet/",views.ProjectListCreateView.as_view(),name='list_create_url'),
    path('projet/<str:pk>',views.ProjectRetrieveUpdateDestroyView.as_view(), name='retrieve_update_destroy_url'),
    path('tashe/', views.TashListCreateView.as_view(), name='task_list_create_url'),
    path('tashe/<str:pk>/', views.TashRetrieveUpdateDestroyView.as_view(), name='task_retrieve_update_destroy_url')
    
]
