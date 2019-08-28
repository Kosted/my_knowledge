from django.urls import path

from knowledge import views

app_name = "knowledge"

urlpatterns = [
    path("", views.index, name="index"),
    path("create_memory/", views.create_memory, name="create_memory"),
    path("show_memory/<str:order_by>", views.show_memory,name="show_memory"),
    path("signup/", views.signup, name='signup'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("createUser/", views.createUser, name="createUser"),
    path("logger/", views.logger, name="logger"),
    path("search/", views.search, name="search"),
    path("convert_text_to_tags/", views.convert_text_to_tags, name="convert_text_to_tags"),
    path("get_single_tag_counter/<str:tag_text>", views.get_single_tag_counter, name="get_single_tag_counter"),


    path("temp/", views.temp, name="temp")
]
