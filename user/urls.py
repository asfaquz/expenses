from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.get_all_users, name='get_all_users'),
    path('user/<int:user_id>/', views.get_user, name='get_user'),
    path('user/create/', views.create_user, name='create_user'),
    path('user/update/<int:user_id>/', views.update_user, name='update_user'),
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user/account/create/', views.create_user_account, name='create_user_account'),


    

]