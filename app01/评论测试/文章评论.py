import os

if __name__ == '__main__':
    # 加载Django项目的配置信息
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings')
    # 导入Django，并启动Django项目
    import django

    django.setup()
    from app01.models import Comment

    # 方案一
    """
    {
        父评论1:[
        {},{},{}...
        ],
    }
    """
    comment_dict = {

    }
    # 找到某个文章的所以评论
    comment_query = Comment.objects.filter(article_id=1)
    for comment in comment_query:
        if not comment.parent_comment:
            # 把评论放入字典
            comment_dict[comment.nid] = comment
