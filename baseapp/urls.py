from django.urls import path
from . import views
#from views import create_task_api,task_detail_api,task_update_api,task_delete_api


urlpatterns = [
    path('', views.home, name ="home"),
    path('login/', views.login_user, name ='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    
    path('create_task/', views.create_task, name='create_task'),
    path('task_list/', views.task_detail, name='task_list'),
    path('task_update/<int:pk>/',views.task_update,name='task_update'),
    path('task_delete/<int:pk>/',views.task_delete,name='task_delete'),

    # path('api/task/create/', views.create_task_api, name='create_task_api'),
    # path('api/task/detail/', views.task_detail_api, name='task_detail_api'),
    # path('api/task/update/<int:pk>/', views.task_update_api, name='task_update_api'),
    # path('api/task/delete/<int:pk>/', views.task_delete_api, name='task_delete_api'),
 
]

