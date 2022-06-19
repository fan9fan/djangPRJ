from django.utils.deprecation import MiddlewareMixin


class TestMiddleware(MiddlewareMixin):

    def process_request(self,request):
        print('每次请求前都会调用执行')

        username = request.COOKIES.get('username')
        if username is None:
            print('没有用户信息')
        else:
            print('用户信息存在')



    def process_response(self, request, response):

        print('每次响应前都会调用')
        return response