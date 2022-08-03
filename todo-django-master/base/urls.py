from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns =[
    path('login/', CustomLoginView.as_view(), name ='login'),
    path('logout/', LogoutView.as_view(next_page= 'login'), name ='logout'),
    path('register/', RegisterPage.as_view(), name ='register' ),
    path('', TaskList.as_view(), name='tasks' ),
    path('task/<int:pk>/', TaskDetail.as_view(), name = 'task'),
    path('task-create/', CreateTask.as_view(), name= "task-create"),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name= 'task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name= 'task-delete'),
    path('task-submissions/<int:pk>/', TaskSubmit.as_view(), name= 'task-submissions'),
    path('user-submit/<int:pk>/', UserSubmit.as_view(), name= 'user-submit'),

]