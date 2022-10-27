from django import template

# 注册
register = template.Library()


@register.filter
def is_user_collects(article, request):
    if str(request.user) == 'AnonymousUser':
        # 没有登录
        return ''
    if article in request.user.collects.all():
        return 'show'
    return ''