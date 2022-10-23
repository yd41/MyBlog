import json

from django.utils.deprecation import MiddlewareMixin


class Md1(MiddlewareMixin):
    # 请求中间件

    def process_request(self, request):
        if request.method == 'POST' and request.META.get('CONTENT_TYPE') == 'application/json':
            data = json.loads(request.body)
            request.data = data

    # 相应中间件
    def process_response(self, request, response):
        return response
