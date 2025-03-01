from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("social-auth/", include("social_django.urls", namespace="social")),
    # password reset
    path(
        "password-reset",
        PasswordResetView.as_view(template_name="USERS/password-reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="USERS/password-reset-done.html"),
        name="password_reset_done",
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name="USERS/password-reset-confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("MAIN.urls")),
    path("user/", include("USERS.urls")),
)

if settings.DEBUG:
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
