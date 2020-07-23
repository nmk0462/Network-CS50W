
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post",views.post,name="post"),
    path("postcreate",views.postcreate,name="postcreate"),
    path("profilepage/<str:nam>",views.profilepage,name="profilepage"),
    path("follow/<str:nam1>",views.follow,name="follow"),
    path("unfollow/<str:nam2>",views.unfollow,name="unfollow"),
    path("folposts",views.folpost,name="folpost"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("likedby/<int:pp>/<str:mnk>",views.likedby,name="likedby"),
    path("unlike/<int:pp1>/<str:mnk1>",views.unlike,name="unlike")
]
