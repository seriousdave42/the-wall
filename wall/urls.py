from django.urls import path
from . import views

urlpatterns = [
    path('', views.wall),
    path('new_post', views.new_post),
    path('new_comment', views.new_comment),
    path('delete_post', views.delete_post),
    path('delete_comment', views.delete_comment)
]