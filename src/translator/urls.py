from django.contrib.auth import (
    views as auth_views,
)  # Імпортуємо вбудовані представлення
from django.urls import path

from .forms import UserLoginForm
from .views import (
    delete_record_view,
    download_file_view,
    history_view,
    register_view,
    result_detail_view,
    translate_view,
)

app_name = "translator"

urlpatterns = [
    path("", translate_view, name="translate"),
    path("history/", history_view, name="history"),
    path("result/<uuid:record_id>/", result_detail_view, name="result_detail"),
    path("delete/<uuid:record_id>/", delete_record_view, name="delete_record"),
    path(
        "download/<uuid:record_id>/<str:file_type>/",
        download_file_view,
        name="download_file",
    ),
    path("register/", register_view, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="translator/login.html", authentication_form=UserLoginForm),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
