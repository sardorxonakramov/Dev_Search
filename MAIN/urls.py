from django.urls import path
from . import views


urlpatterns = [
    path("", views.DevelopersView.as_view(), name="developers"),
    path("projects/", views.ProjectViews.as_view(), name="projects"),
    path("profile/<int:user_id>/", views.ProfileView.as_view(), name="profile"),

    path("project-create/", views.CreateprojectView.as_view(), name="project_create"),
    path("project/<int:project_id>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("sent-message/<int:reciever_id>",views.handle_message_submission,name='sent_message'),

    path('inbox/',views.InboxView.as_view(),name='inbox'),
    path('message/<int:message_id>',views.MessageView.as_view(),name='message'),
]
