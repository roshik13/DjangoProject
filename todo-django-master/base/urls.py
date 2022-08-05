from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns =[
    path('login/', CustomLoginView.as_view(), name ='login'),
    path('logout/', LogoutView.as_view(next_page= 'login'), name ='logout'),
    path('register/', RegisterPage.as_view(), name ='register' ),
    path('', TaskList.as_view(), name='tasks' ),
    path('task/<int:pk>/', TaskDetail.as_view(), name = 'task'),
    path('task-create/', CreateTask.as_view(), name= "task-create"),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name= 'task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name= 'task-delete'),
    path('task-submissions/', TaskSubmit.as_view(), name= 'task-submissions'),
    path('user-submit/', UserSubmit.as_view(), name= 'user-submit'),
    path('some/<int:pk>/',TaskVerify.YOUR_VIEW_DEF,name='YOUR_VIEW'),
    path('some1/<int:pk>/',TaskVerify.YOUR_VIEW_DEF1,name='YOUR_VIEW1'),
    path('certificate/',views.certificate_request,name='certificate')

]