import random

from django import forms
from django.http import JsonResponse
from django.views import View
from markdown import markdown
from pyquery import PyQuery

from api.views.login import clean_form
from app01.models import *


# 添加文章或编辑文章的验证
class AddArticleForm(forms.Form):
    title = forms.CharField(error_messages={'required': '请输入文章标题'})
    content = forms.CharField(error_messages={'required': '请输入文章内容'})
    abstract = forms.CharField(required=False)  # 不进行为空验证
    cover_id = forms.IntegerField(required=False)

    category = forms.IntegerField(required=False)
    pwd = forms.CharField(required=False)
    recommend = forms.BooleanField(required=False)

    status = forms.IntegerField(required=False)

    # 全局钩子 分类 文章密码
    def clean(self):
        category = self.cleaned_data['category']
        if not category:
            self.cleaned_data.pop('category')

        pwd = self.cleaned_data['pwd']
        if not pwd:
            self.cleaned_data.pop('pwd')

    # 文章简介
    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if abstract:
            return self.cleaned_data['abstract']
        # 截取正文前30个字符
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:30]
            return abstract

    # 文章封面
    def clean_cover_id(self):
        cover_id = self.cleaned_data['cover_id']
        if cover_id:
            return cover_id
        cover_set = Cover.objects.all().values('nid')
        cover_id = random.choice(cover_set)['nid']
        return cover_id


# 给文章添加标签
def add_article_tags(article_obj, tags):
    for tag in tags:
        if tag.isdigit():
            article_obj.tag.add(tag)
        else:
            # 先创建，再多对多关联
            tag_obj = Tags.objects.create(title=tag)
            article_obj.tag.add(tag_obj.nid)


class ArticleView(View):
    # 添加文章
    def post(self, request):
        res = {
            'msg': '文章发布成功',
            'code': 412,
            'data': None
        }
        data = request.data
        data['status'] = 1

        form = AddArticleForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        form.cleaned_data['author'] = '无'
        form.cleaned_data['source'] = '未知'
        article_obj = Articles.objects.create(**form.cleaned_data)
        tags = data.get('tags')
        add_article_tags(article_obj=article_obj, tags=tags)
        res['code'] = 0
        res['data'] = article_obj.nid
        return JsonResponse(res)

    # 编辑文章
    def put(self, request, nid):
        res = {
            'msg': '文章编辑成功',
            'code': 412,
            'data': None
        }
        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = '请求错误'
            return JsonResponse(res)

        data = request.data
        data['status'] = 1
        form = AddArticleForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        form.cleaned_data['author'] = '无'
        form.cleaned_data['source'] = '未知'
        article_query.update(**form.cleaned_data)
        tags = data.get('tags')
        # 清空这篇文章所以标签
        article_query.first().tag.clear()
        add_article_tags(article_obj=article_query.first(), tags=tags)
        res['code'] = 0
        res['data'] = article_query.first().nid
        return JsonResponse(res)




# class ArticleView(View):
#     def post(self, request):
#         res = {
#             'mas': '文章发布成功',
#             'code': 412,
#             'data':None
#         }
#         data: dict = request.data
#         title = data.get('title')
#         if not title:
#             res['mas'] = '请输入文章标题'
#             return JsonResponse(res)
#         content = data.get('content')
#         recommend = data.get('recommend')
#         if not content:
#             res['mas'] = '请输入文章内容'
#             return JsonResponse(res)
#         extra = {
#             'title': title,
#             'content': content,
#             'recommend': recommend,
#             'status': 1
#         }
#
#         # 解析文本内容
#         abstract = data.get('abstract')
#         if not abstract:
#             abstract = PyQuery(markdown(content)).text()[:30]
#         extra['abstract'] = abstract
#         cover_id=data.get('cover_id')
#         if cover_id:
#             extra['cover_id']=cover_id
#         category = data.get('category_id')
#         if category:
#             extra['category'] = category
#         else:
#             extra['category'] = 1
#         pwd = data.get('pwd')
#         if pwd:
#             extra['pwd'] = pwd
#
#         article_obj = Articles.objects.create(**extra)
#         # 标签
#         tags = data.get('tags')
#         if tags:
#             for tag in tags:
#                 if not tag.isdigit():
#                     tag_obj = Tags.objects.create(title=tag)
#                     article_obj.tag.add(tag)
#                 else:
#                     article_obj.tag.add(tag)
#         res['data']=article_obj.nid
#         return JsonResponse(res)
