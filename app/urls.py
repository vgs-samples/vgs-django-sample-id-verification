from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    # ex: /app/5/
    path('<int:data_id>/', views.detail, name='detail'),
]
