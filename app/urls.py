from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    # ex: /app/5/
    path('<int:data_id>/', views.detail, name='detail'),
    path('api/data/<int:data_id>/', views.get_data, name='api.data'),
    path('api/checkr/<int:data_id>/', views.check, name='api.checker'),

]
