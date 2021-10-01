from django.contrib import admin
from django.urls import path
from .views import login_room_view, signupview, loginview, listview, CreateClass, logoutview, good

urlpatterns=[
    path("", login_room_view, name="login_room"),#紹介された人かどうかを調べるログイン画面
    path("admin/", admin.site.urls),
    path("signup/", signupview, name="signup"),#ユーザー登録画面
    path("login/", loginview, name="login"),#ユーザとしてログインする画面
    path("list/", listview, name="list"),#タイムラインの画面
    path("create/", CreateClass.as_view(), name="create"),#新規投稿の画面
    path("logout/", logoutview, name="logout"),#ログアウト画面
    path("good/<int:content_id>", good, name="good"),#いいね機能
]