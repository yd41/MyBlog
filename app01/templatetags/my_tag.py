from django import template

register = template.Library()


# @register.filter
# def add1(item):
#     return int(item) + 1
@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name,article=None):
    img_list=['http://www.fengfengzhidao.com/media/site_bg/wallhaven-k7jmg6.jpg',
              'http://www.fengfengzhidao.com/media/site_bg/wallhaven-k7jmg6.jpg',
              'http://www.fengfengzhidao.com/media/site_bg/311.jpg']

    if article:
        # 说明是文章详情页面
        # 拿到文章封面
        cover=article.cover.url.url
        img_list=[cover]
    return {'img_list':img_list}