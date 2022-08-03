from email.mime import base
from urllib import request
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView,FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 

from django.urls import reverse_lazy
from base.models import *


class CustomLoginView(LoginView):
    template_name= "base/login.html"
    fields = "__all__"
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name ='base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self,form):
        user =form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    
    #def get(self,*args, **kwargs):
        #if self.request.user.is_authenticated == True:
            #return redirect('tasks')
        
        #return super(RegisterPage, self.get(*args, **kwargs) )

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = context['tasks'].count()

        search_input = self.request.GET.get('area-busca') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(
                title__istartswith=search_input
            )
        
        
        return context



class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class CreateTask(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description', 'rewards']
    success_url = reverse_lazy('tasks')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):  
    model = Task
    fields = ['title','description', 'complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

class TaskSubmit(LoginRequiredMixin,ListView):
    template_name='base/task_submission.html'
    model=Pair
    fields=['user','complete']
    context_object_name = 'pairs'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class UserSubmit(LoginRequiredMixin,CreateView):
    template_name='base/user_submit.html'
    model=Pair
    fields=['complete']
    success_url=reverse_lazy('tasks')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserSubmit, self).form_valid(form)