from django.contrib import auth
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app01.models import Articles, Tags, Cover
from app01.utils.pagination import Pagination
from app01.utils.random_code import random_code
from app01.utils.sub_comment import sub_comment_list


def index(request):
    article_list = Articles.objects.filter(status=1).order_by('-change_date')
    fronted_list = article_list.filter(category=1)[:6]  # 前端
    backend_list = article_list.filter(category=2)[:6]  # 后端
    query_params = request.GET.copy()
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=3,
        page_page_count=7
    )

    article_list = article_list[pager.start:pager.end]

    return render(request, 'index.html', locals())


def search(request):
    search_key = request.GET.get('key', '')
    order = request.GET.get('order', '')
    tag = request.GET.get('tag', '')
    word = request.GET.getlist('word')

    article_list = Articles.objects.filter(title__contains=search_key)
    query_params = request.GET.copy()
    if len(word) == 2:
        article_list = article_list.filter(word__range=word)
    if tag:
        article_list = article_list.filter(tag__title=tag)
    if order:
        try:
            article_list = article_list.order_by(order)
        except Exception:
            pass
    # 分页器
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=5,
        page_page_count=7
    )
    article_list = article_list[pager.start:pager.end]

    return render(request, 'search.html', locals())


def article(request, nid):
    article_query = Articles.objects.filter(nid=nid)

    article_query.update(look_count=F('look_count') + 1)

    if not article_query:
        return redirect('/')
    article = article_query.first()
    comment_list = sub_comment_list(nid)

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
    return render(request, 'backend/backend.html', locals())


def edit_avatar(request):
    return render(request, 'backend/edit_avatar.html')


def add_article(request):
    # 拿到所有的分类，标签
    tag_list = Tags.objects.all()
    # 拿到所有的文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            'url': cover.url.url,
            'nid': cover.nid
        })
    category_list = Articles.category_choice
    return render(request, 'backend/add_article.html', locals())


def edit_article(request, nid):
    article_obj = Articles.objects.get(nid=nid)
    tags = [str(tag.nid) for tag in article_obj.tag.all()]
    # 拿到所有的分类，标签
    tag_list = Tags.objects.all()
    # 拿到所有的文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            'url': cover.url.url,
            'nid': cover.nid
        })
    category_list = Articles.category_choice
    return render(request, 'backend/edit_article.html', locals())


def reset_password(request):
    return render(request, 'backend/reset_password.html', locals())


def admin_home(request):
    return render(request,'admin_home.html')