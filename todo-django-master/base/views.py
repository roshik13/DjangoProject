from email.mime import base
from django.contrib.auth.models import User

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
from django.http import HttpResponseRedirect
from django.urls import reverse


context2={}
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
        task=Task.objects.all()
        pair=Pair.objects.all()
        pair=pair.filter(user=self.request.user)
        complete={}
        for tasks in task:
            complete[tasks]=False
        for pairs in pair:
            if pairs.complete==1:
                complete[pairs.task]=True

        context = super().get_context_data(**kwargs)
        context['count'] = context['tasks'].count()
        context['completed']=complete
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
    fields = ['title','description']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

class TaskSubmit(LoginRequiredMixin,ListView):
    template_name='base/task_submission.html'
    model=Pair
    fields=['user','complete','task','image']
    context_object_name = 'pairs'
    def get_context_data(self, **kwargs):
        context1 = super().get_context_data(**kwargs)
        return context1

class UserSubmit(LoginRequiredMixin,CreateView):
    template_name='base/user_submit.html'
    model=Pair
    fields=['task', 'image']
    success_url=reverse_lazy('tasks')
    
    def form_valid(self, form):
        # pair_object = form.save(commit=False)
        task_id = dict(form.data)['task'][0]

        task=Task.objects.get(pk=task_id)
        user=User.objects.get(username=self.request.user)
        uploaded_image = dict(self.request.FILES)['image'][0]

        user_image_obj = Pair.objects.filter(task=task, user=user)

        if not list(user_image_obj):
            user_image_obj=Pair.objects.create(task=task, image=uploaded_image, user=user)
            user_image_obj.save()
        else:
            for item in user_image_obj:
                item.image = uploaded_image
                item.save()

        # pair_object.save()
        return HttpResponseRedirect(reverse('user-submit'))
    

class TaskVerify(LoginRequiredMixin,ListView):
    template_name='base/task_submission.html'
    model=Pair
    fields=['user','complete','task']
    context_object_name = 'pairs'
    def get_context_data(self, **kwargs):
        context1 = super().get_context_data(**kwargs)
        return context1

    def YOUR_VIEW_DEF(request, pk):
        pair=Pair.objects.get(pk=pk)
        if pair.complete<1:
            pair.user.profile.rewards+=pair.task.rewards
            pair.complete=1
            pair.save()
            pair.user.profile.save()
        #return render(request,'base/task_submission.html')
        return redirect('task-submissions')

    def YOUR_VIEW_DEF1(request, pk):
        pair=Pair.objects.get(pk=pk)
        if not pair.complete:
            pair.complete=-1
            pair.save()
            pair.user.profile.save()
        #return render(request,'base/task_submission.html')
        return redirect('task-submissions')

def certificate_request(request):
    
        return render(request, 'base/certificate.html')  
    
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)