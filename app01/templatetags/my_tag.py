from django import template
from django.utils.safestring import mark_safe

from app01.models import Tags
from app01.utils.search import Search

register = template.Library()


# @register.filter
# def add1(item):
#     return int(item) + 1
@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name, article=None):
    img_list = ["../media/article_img/img.png", "../media/article_img/img_1.png", "../media/article_img/img_2.png"]

    if article:
        # 说明是文章详情页面
        # 拿到文章封面
        cover = article.cover.url.url
        img_list = [cover]
    return {'img_list': img_list}


@register.simple_tag
def generate_order_html(request, key):
    order = request.GET.get(key, '')
    order_list = []
    if key == 'order':
        order_list = [
            ('-change_date', '综合排序'),
            ('-create_date', '最新发布'),
            ('-look_count', '最多浏览'),
            ('-digg_count', '最多点赞'),
            ('-collects_count', '最多收藏'),
            ('-comment_count', '最多评论')
        ]
    elif key == 'word':
        order = request.GET.getlist(key, '')
        order_list = [
            ([''], '全部字数'),
            (['0', '500'], '500字以内'),
            (['500', '1000'], '1000字以内'),
            (['1000', '3000'], '3000字以内'),
            (['3000', '50000'], 'more')
        ]
    elif key == 'tag':
        tag_list = Tags.objects.exclude(articles__isnull=True)
        order_list.append(('', '全部标签'))
        for tag in tag_list:
            order_list.append((tag.title, tag.title))
    query_params = request.GET.copy()
    order = Search(
        key=key,
        order=order,
        order_list=order_list,
        query_params=query_params
    )
    return mark_safe(order.order_html())


# 动态导航
@register.simple_tag
def dynamic_navigation(request):
    path = request.path_info
    path_dict = {
        '/': '首页',
        '/news/': '新闻',
        '/moods/': '心情',
        '/history/': '回忆录',
        '/about/': '关于',
        '/sutes/': '网站导航'
    }
    nav_list = []
    for k, v in path_dict.items():
        if k == path:
            nav_list.append(f'<a href="{k}" class="active">{v}</a>')
            continue
        nav_list.append(f'<a href="{k}">{v}</a>')
    return mark_safe(''.join(nav_list))
