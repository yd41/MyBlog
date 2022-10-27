from django.http import JsonResponse
from django.views import View

from app01.models import Comment


class CommentView(View):

    # 发布评论
    def post(self, request, nid):
        # /api/article_nid_comment/
        # 文章id
        # 用户
        # 评论的内容
        res = {
            'msg': '文章评论成功',
            'code': 412,
            'self': None
        }
        data = request.data
        if not request.user.username:
            res['msg'] = '请登录'
            return JsonResponse(res)
        content = data.get('content')
        if not content:
            res['msg'] = '请输入评论内容'
            res['self'] = 'content'
            return JsonResponse(res)
        pid=data.get('pid')
        if pid:
            Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid,
                parent_comment_id=pid
            )
        else:
            # 评论成功
            Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid
            )
        res['code'] = 0
        return JsonResponse(res)
