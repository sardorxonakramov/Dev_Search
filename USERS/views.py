from django.shortcuts import render,redirect
from django.views.generic import CreateView,DetailView,UpdateView,DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from .models import Skill
from .forms import UserRegisterForm, SkillForm,UpdateAccountForm



User =get_user_model()

# class SignInView(LoginView):
#     model = User
#     template_name = 'USERS/login.html'

class SignUpView(CreateView):
    model = User
    template_name = 'USERS/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')

class AccountView(LoginRequiredMixin,DetailView):
    model = User
    context_object_name ='account'
    template_name = 'USERS/account.html'
    pk_url_kwarg = 'user_id'
    login_url=reverse_lazy('login')


class CreateSkillView(CreateView):
    template_name = 'form.html'
    model = Skill
    form_class = SkillForm

    def form_valid(self, form):
        skill = form.save(commit=False)
        skill.owner= self.request.user
        skill.save()
        return redirect('account',user_id=self.request.user.id)
     
    def get_context_data(self, *args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['btn_text']=_("Create Skill")
        return context

    def get_success_url(self):
        return reverse('account',user_id=self.user.id)
    


class UpdateSkillView(UpdateView):
    template_name = 'form.html'
    model = Skill
    form_class = SkillForm
    pk_url_kwarg= 'skill_id'

    def form_valid(self, form):
        skill = form.save(commit=False)
        skill.owner= self.request.user
        skill.save()
        return redirect('account',user_id=self.request.user.id)
     
    def get_context_data(self, *args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['btn_text']=_("Update Skill")
        return context

    def get_success_url(self):
        return reverse('account',user_id=self.user.id)
    


class DeleteSkillView(DeleteView):
    model  = Skill
    template_name = 'delete.html'
    pk_url_kwarg ='skill_id'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['confirmation_text']= f'Are your sure you want to delete this "{ self.get_object().name }"?'
        return context
    

    def get_success_url(self):
        return  reverse('account',kwargs={'user_id':self.request.user.id })

class UpdateAccount(UpdateView):
    template_name ='form.html'
    model = User
    form_class = UpdateAccountForm
    pk_url_kwarg = 'user_id'
    
    def get_success_url(self):
        return reverse('account',kwargs={'user_id':self.request.user.id})
    
    def get_context_data(self, *args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['btn_text']=_("Update Account")
        return context