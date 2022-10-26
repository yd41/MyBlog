

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
