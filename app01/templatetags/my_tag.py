from django import template

register = template.Library()


# @register.filter
# def add1(item):
#     return int(item) + 1
@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name,article=None):
    img_list=["media/article_img/img.png","media/article_img/img_1.png","media/article_img/img_2.png"]

    if article:
        # 说明是文章详情页面
        # 拿到文章封面
        cover=article.cover.url.url
        img_list=[cover]
    return {'img_list':img_list}