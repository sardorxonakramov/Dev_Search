from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, CreateView, DetailView
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import Project, Tag, Message
from .forms import ProjectForm, MessageForm

# Create your views here.
User = get_user_model()


class DevelopersView(ListView):
    template_name = "MAIN/developers.html"
    paginator_class = Paginator
    paginate_by =2
    def get_queryset(self):
        return User.objects.exclude(
            Q(bio=None)
            | Q(location=None)
            | Q(occupation=None)
            | Q(bio=None)
            | Q(location=None)
            | Q(occupation=None)
        ).exclude(id=self.request.user.id)
    
    context_object_name = "developers"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        page_obj = context['page_obj']
        left_index = page_obj.number - 1
        right_index = page_obj.number + 1

        if left_index < 1:
            left_index = 1
        
        if right_index > page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages

        custom_range = range(left_index, right_index + 1)
        context['custom_range'] = custom_range
        return context
    
class ProjectViews(ListView):
    queryset = Project.objects.all()
    template_name = 'MAIN/projects.html'
    context_object_name ='projects'

    paginator_class = Paginator
    paginate_by =2

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        page_obj = context['page_obj']
        left_index = page_obj.number - 1
        right_index = page_obj.number + 1

        if left_index < 1:
            left_index = 1
        
        if right_index > page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages

        custom_range = range(left_index, right_index + 1)
        context['custom_range'] = custom_range
        return context





    
class CreateprojectView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")
    model = Project
    template_name = "MAIN/project_form.html"
    form_class = ProjectForm
    extra_context = {"btn_text": "Create project"}

    def get_success_url(self):
        return reverse("account", kwargs={"user_id": self.request.user.id})

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            tags = self.request.POST.get("tags", "").split(",")
            project_form = ProjectForm(self.request.POST)

            if project_form.is_valid():
                project = project_form.save(commit=False)
                project.owner = self.request.user
                project.save()

                # Process and add tags
                for tag_name in tags:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name.strip().lower()
                    )
                    project.tags.add(tag)

                project.save()  # Final save with tags
                return redirect("account", user_id=self.request.user.id)

            # If form is invalid, render the form with errors
            return redirect("project_create", kwargs={"user_id": self.request.user.id})

        return super().dispatch(request, *args, **kwargs)


class ProjectDetailView(DetailView):
    model = Project
    template_name = "MAIN/project.html"
    pk_url_kwarg = "project_id"


class ProfileView(DetailView):
    model = User
    pk_url_kwarg = "user_id"
    template_name = "MAIN/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dev_skill"] = self.get_object().skill_set.exclude(discription="")
        context["other_skill"] = self.get_object().skill_set.filter(discription="")
        return context


def handle_message_submission(request, receiver_id):
    form = MessageForm(request.POST or None)

    if request.user.is_authenticated:
        form.fields.pop("fullname")
        form.fields.pop("email")
    if request.method == "POST":
        if form.is_valid():
            print(form.errors)
            message = form.save(commit=False)
            if request.user.is_authenticated:
                message.sender = request.user
                message.fullname = request.user.fullname
                message.email = request.user.email
            message.receiver = User.objects.get(id=receiver_id)
            message.save()
            return redirect("profile", user_id=receiver_id)

    context = {"form": form, "btn_text": "Sent Message"}
    return render(request=request, template_name="form.html", context=context)


class InboxView(ListView):
    queryset = Message.objects.all().order_by('is_read','-created')

    template_name = 'MAIN/inbox.html'
    get_user_model = 'messages'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['unread_messages_count'] = Message.objects.filter(is_read=False).count()
        return context

class MessageView(DetailView):
    model = Message

    template_name = 'MAIN/message.html'
    context_object_name ='message'
    pk_url_kwarg ='message_id'

    def dispatch(self, request, *args, **kwargs):
        message = self.get_object()
        message.is_read =True
        message.save()
        return super().dispatch(request, *args, **kwargs)