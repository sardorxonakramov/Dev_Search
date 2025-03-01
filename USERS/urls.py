from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("account/<int:user_id>/", views.AccountView.as_view(), name="account"),
    path("update-account/<int:user_id>/", views.UpdateAccount.as_view(), name="update_account"),

    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signin/", LoginView.as_view(template_name="USERS/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("create-skill/", views.CreateSkillView.as_view(),name='create_skill'),
    path("update-skill/<int:skill_id>/", views.UpdateSkillView.as_view(),name='update_skill'),
    path("delete-skill/<int:skill_id>/", views.DeleteSkillView.as_view(),name='delete_skill'),
]
