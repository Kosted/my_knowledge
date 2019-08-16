from django.urls import path

from knowledge import views

app_name = "knowledge"

urlpatterns = [
    path("", views.index, name="index"),
    path("create_memory/", views.create_memory, name="create_memory"),
    path("show_memory/", views.show_memory,name="show_memory"),
    path("signup/", views.signup, name='signup'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("createUser/", views.createUser, name="createUser"),
    path("logger/", views.logger, name="logger"),
    path("search/", views.search, name="search")
]
