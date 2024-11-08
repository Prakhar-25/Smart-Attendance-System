from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name = "index"),
    path("about", views.about, name = "about"),
    path("register", views.register, name = "register"),
    # path("faculty", views.faculty, name = "faculty"),
    path("dashboard", views.dashboard, name = "dashboard"),
    path("registered_students", views.registered_students, name = "registered_students"),
    path("login", views.login_view, name = "login_view"),
    path("logout", views.logout_view, name = "logout_view"),
    path("attendance", views.attendance, name = "attendance")
]
