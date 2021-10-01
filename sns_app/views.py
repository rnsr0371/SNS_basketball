from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import TweetModel, GoodModel
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

#紹介された人かどうかを調べるログイン画面。部屋名とパスはしばらく公開するのでハードコーディングしてOK
def login_room_view(request):
    if request.method=="POST":
        roomname_data=request.POST["roomname_data"]
        password_data=request.POST["password_data"]

        if roomname_data=="BLeague_SNS" and password_data=="20210930":
            return redirect("login")
        else:
            return redirect("login_room")

    return render(request, "login_room.html")


#ユーザーの新規作成画面。
def signupview(request):
    if request.method=="POST":
        username_data=request.POST["username_data"]
        password_data=request.POST["password_data"]
        try:
            User.objects.create_user(username_data,"",password_data)
        except IntegrityError:
            return render(request,"signup.html",{"error":"このユーザーはすでに登録されています。"})
    else:
        return render(request,"signup.html",{})

    return redirect("login")


#ユーザのログイン画面。
def loginview(request):
    if request.method=="POST":
        username_data=request.POST["username_data"]
        password_data=request.POST["password_data"]
        user=authenticate(request, username=username_data, password=password_data)

        if user is not None:
            login(request, user)
            return redirect("list")
        else:
            return redirect("login")
    
    return render(request,"login.html")


#タイムラインの画面
@login_required(login_url="/login")
def listview(request):
    object_list=TweetModel.objects.all().order_by("id").reverse()#order_by以降で投稿が新しいものから順に上に表示
    return render(request, "list.html", {"object_list":object_list})


#新規投稿の画面
class CreateClass(CreateView):
    template_name="create.html"
    model=TweetModel
    fields=("content","author","good")
    success_url=reverse_lazy("list")


#ログアウト画面
def logoutview(request):
    logout(request)
    return redirect("login")

#いいね機能
#本当はいいねに成功した時や失敗した時（すでにいいねを押したことがある時）はフラッシュメッセージが表示されるようにしたかった。
def good(request, content_id):
    #いいねするツイートの取得
    good_content=TweetModel.objects.get(id=content_id)
    #自分がいいねした数を調べる
    num_good=GoodModel.objects.filter(good_by=request.user).filter(content_id=good_content).count()

    if num_good>0:
        #messages.success(request,"既にそのツイートにはいいねを押したことがあります。")
        return redirect("list")

    #メッセージのいいねを一つ増やす
    good_content.good+=1
    good_content.save()

    #Goodモデルを作成し保存
    good=GoodModel()
    good.good_by=request.user
    good.content_id=good_content
    good.save()

    #messages.success(request, "ツイートにいいねしました！")
    return redirect("list")


