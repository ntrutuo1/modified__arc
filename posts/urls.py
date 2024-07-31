from django.urls import path
from . import views

app_name='posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
]
