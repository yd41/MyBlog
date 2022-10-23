from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app01.models import Articles
from app01.utils.random_code import random_code


def index(request):
    return render(request, 'index.html', {'request': request})


def article(request, nid):
    article_query = Articles.objects.filter(nid=nid)
    if not article_query:
        return redirect('/')
    article = article_query.first()
    return render(request, 'article.html', locals())


def news(request):
    return render(request, 'news.html')


def login(request):
    return render(request, 'login.html')


# 获取随机验证码
def get_random_code(request):
    data, valid_code = random_code()
    request.session['valid_code'] = valid_code
    return HttpResponse(data)


def sign(request):
    return render(request, 'sign.html')


def logout(request):
    auth.logout(request)
    return redirect('/')




def backend(request):
    if not request.user.username:
    #     没有登录
        return redirect('/')
    return render(request,'backend/backend.html',locals())

def edit_avatar(request):
    return render(request,'backend/edit_avatar.html')

def add_article(request):
    return render(request,'backend/add_article.html',locals())

def edit_article(request):
    return render(request,'backend/edit_article.html',locals())


def reset_password(request):
    return render(request,'backend/reset_password.html',locals())