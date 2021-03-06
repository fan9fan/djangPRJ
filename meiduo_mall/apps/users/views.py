import redis
from django.db.models import constants


# Create your views here.
from django.template.base import logger

"""
需求分析： 根据页面的功能（从上到下，从左到右），哪些功能需要和后端配合完成
如何确定 哪些功能需要和后端进行交互呢？？？
        1.经验
        2.关注类似网址的相似功能

"""

"""
判断用户名是否重复的功能。

前端(了解)：     当用户输入用户名之后，失去焦点， 发送一个axios(ajax)请求

后端（思路）：
    请求:         接收用户名 
    业务逻辑：     
                    根据用户名查询数据库，如果查询结果数量等于0，说明没有注册
                    如果查询结果数量等于1，说明有注册
    响应          JSON 
                {code:0,count:0/1,errmsg:ok}
    
    路由      GET         usernames/<username>/count/        
   步骤：
        1.  接收用户名
        2.  根据用户名查询数据库
        3.  返回响应         
    
"""
from django.views import View
from apps.users.models import User, Address
from django.http import JsonResponse
import re
class UsernameCountView(View):

    def get(self,request,username):
        # 1.  接收用户名，对这个用户名进行一下判断
        # if not re.match('[a-zA-Z0-9_-]{5,20}',username):
        #     return JsonResponse({'code':200,'errmsg':'用户名不满足需求'})
        # 2.  根据用户名查询数据库
        count=User.objects.filter(username=username).count()
        # 3.  返回响应
        return JsonResponse({'code':0,'count':count,'errmsg':'ok'})

"""
我们不相信前端提交的任何数据！！！！

前端：     当用户输入 用户名，密码，确认密码，手机号，是否同意协议之后，会点击注册按钮
            前端会发送axios请求

后端：
    请求：             接收请求（JSON）。获取数据
    业务逻辑：          验证数据。数据入库
    响应：             JSON {'code':0,'errmsg':'ok'}
                     响应码 0 表示成功 400表示失败
    
    路由：     POST    register/
    
    步骤：
    
        1. 接收请求（POST------JSON）
        2. 获取数据
        3. 验证数据
            3.1 用户名，密码，确认密码，手机号，是否同意协议 都要有
            3.2 用户名满足规则，用户名不能重复
            3.3 密码满足规则
            3.4 确认密码和密码要一致
            3.5 手机号满足规则，手机号也不能重复
            3.6 需要同意协议
        4. 数据入库
        5. 返回响应


"""
import json

class RegisterView(View):

    def post(self,request):
        # 1. 接收请求（POST------JSON）
        body_bytes=request.body
        body_str=body_bytes.decode()
        body_dict=json.loads(body_str)

        # 2. 获取数据
        username=body_dict.get('username')
        password=body_dict.get('password')
        password2=body_dict.get('password2')
        mobile=body_dict.get('mobile')
        allow=body_dict.get('allow')

        # 3. 验证数据
        #     3.1 用户名，密码，确认密码，手机号，是否同意协议 都要有
        # all([xxx,xxx,xxx])
        # all里的元素 只要是 None,False
        # all 就返回False，否则返回True
        if not all([username,password,password2,mobile,allow]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        #     3.2 用户名满足规则，用户名不能重复
        if not re.match('[a-zA-Z_-]{5,20}',username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足规则'})
        #     3.3 密码满足规则
        #     3.4 确认密码和密码要一致
        #     3.5 手机号满足规则，手机号也不能重复
        #     3.6 需要同意协议
        # 4. 数据入库
        # user=User(username=username,password=password,moble=mobile)
        # user.save()

        # User.objects.create(username=username,password=password,mobile=mobile)

        #以上2中方式，都是可以数据入库的
        # 但是 有一个问题 密码没有加密

        # 密码就加密
        user=User.objects.create_user(username=username,password=password,mobile=mobile)

        # 如何设置session信息
        # request.session['user_id']=user.id

        # 系统（Django）为我们提供了 状态保持的方法
        from django.contrib.auth import login
        # request, user,
        # 状态保持 -- 登录用户的状态保持
        # user 已经登录的用户信息
        login(request,user)

        # 5. 返回响应
        return JsonResponse({'code':0,'errmsg':'ok'})

"""
如果需求是注册成功后即表示用户认证通过，那么此时可以在注册成功后实现状态保持 (注册成功即已经登录)  v
如果需求是注册成功后不表示用户认证通过，那么此时不用在注册成功后实现状态保持 (注册成功，单独登录)

实现状态保持主要有两种方式：
    在客户端存储信息使用Cookie
    在服务器端存储信息使用Session

"""

"""
登录
    
前端：
        当用户把用户名和密码输入完成之后，会点击登录按钮。这个时候前端应该发送一个axios请求
        
后端：
    请求    ：  接收数据，验证数据
    业务逻辑：   验证用户名和密码是否正确，session
    响应    ： 返回JSON数据 0 成功。 400 失败

    POST        /login/
步骤：
    1. 接收数据
    2. 验证数据
    3. 验证用户名和密码是否正确
    4. session
    5. 判断是否记住登录
    6. 返回响应

"""

class LoginView(View):

    def post(self,request):
        # 1. 接收数据
        data=json.loads(request.body.decode())
        username=data.get('username')
        password=data.get('password')
        remembered=data.get('remembered')
        # 2. 验证数据
        if not all([username,password]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})


        # 确定 我们是根据手机号查询 还是 根据用户名查询

        # USERNAME_FIELD 我们可以根据 修改 User. USERNAME_FIELD 字段
        # 来影响authenticate 的查询
        # authenticate 就是根据 USERNAME_FIELD 来查询
        if re.match('1[3-9]\d{9}',username):
            User.USERNAME_FIELD='mobile'
        else:
            User.USERNAME_FIELD='username'

        # 3. 验证用户名和密码是否正确
        # 我们可以通过模型根据用户名来查询
        # User.objects.get(username=username)


        # 方式2
        from django.contrib.auth import authenticate
        # authenticate 传递用户名和密码
        # 如果用户名和密码正确，则返回 User信息
        # 如果用户名和密码不正确，则返回 None
        user=authenticate(username=username,password=password)

        if user is None:
            return JsonResponse({'code':400,'errmsg':'账号或密码错误'})

        # 4. session
        from django.contrib.auth import login
        login(request,user)
        # 5. 判断是否记住登录
        if remembered:
            # 记住登录 -- 2周 或者 1个月 具体多长时间 产品说了算
            request.session.set_expiry(None)

        else:
            #不记住登录  浏览器关闭 session过期
            request.session.set_expiry(0)

        # 6. 返回响应
        response = JsonResponse({'code':0,'errmsg':'ok'})
        # 为了首页显示用户信息
        response.set_cookie('username',username)

        return response

"""
前端：
    当用户点击退出按钮的时候，前端发送一个axios delete请求

后端：
    请求
    业务逻辑        退出
    响应      返回JSON数据

"""
from django.contrib.auth import logout
class LogoutView(View):

    def get(self,request):
        # 1. 删除session信息
        logout(request)

        response = JsonResponse({'code':0,'errmsg':'ok'})
        # 2. 删除cookie信息，为什么要是删除呢？ 因为前端是根据cookie信息来判断用户是否登录的
        response.delete_cookie('username')

        return response

# 用户中心，也必须是登录用户

"""

LoginRequiredMixin 未登录的用户 会返回 重定向。重定向并不是JSON数据

我们需要是  返回JSON数据
"""


from utils.views import LoginRequiredJSONMixin
class CenterView(LoginRequiredJSONMixin,View):

    def get(self,request):
        # request.user 就是 已经登录的用户信息
        # request.user 是来源于 中间件
        # 系统会进行判断 如果我们确实是登录用户，则可以获取到 登录用户对应的 模型实例数据
        # 如果我们确实不是登录用户，则request.user = AnonymousUser()  匿名用户
        info_data = {
            'username':request.user.username,
            'email':request.user.email,
            'mobile':request.user.mobile,
            'email_active':request.user.email_active,
        }

        return JsonResponse({'code':0,'errmsg':'ok','info_data':info_data})

"""
需求：     1.保存邮箱地址  2.发送一封激活邮件  3. 用户激活邮件

前端：
    当用户输入邮箱之后，点击保存。这个时候会发送axios请求。
    
后端：
    请求           接收请求，获取数据
    业务逻辑        保存邮箱地址  发送一封激活邮件
    响应           JSON  code=0
    
    路由          PUT     
    步骤
        1. 接收请求
        2. 获取数据
        3. 保存邮箱地址
        4. 发送一封激活邮件
        5. 返回响应
        

需求（要实现什么功能） --> 思路（ 请求。业务逻辑。响应） --> 步骤  --> 代码实现
"""

class EmailView(LoginRequiredJSONMixin,View):

    def put(self,request):
        # 1. 接收请求
        #ｐｕｔ post －－－　ｂｏdy
        data=json.loads(request.body.decode())
        # 2. 获取数据
        email=data.get('email')
        # 验证数据
        # 正则　
        # 3. 保存邮箱地址
        user=request.user
        # user / request.user 就是　登录用户的　实例对象
        # user --> User
        user.email=email
        user.save()
        # 4. 发送一封激活邮件
        # 一会单独讲发送邮件

        # subject, message, from_email, recipient_list,
        # subject,      主题
        subject='美多商城激活邮件'
        # message,      邮件内容
        message=""
        # from_email,   发件人
        from_email='美多商城<zhuche99@126.com>'
        # recipient_list, 收件人列表
        recipient_list = ['zhuche99@126.com','zhuche99@126.com']

        # 邮件的内容如果是 html 这个时候使用 html_message
        # 4.1 对a标签的连接数据进行加密处理
        # user_id=1
        from apps.users.utils import generic_email_verify_token
        token=generic_email_verify_token(request.user.id)

        verify_url = "http://www.meiduo.site:8080/success_verify_email.html?token=%s"%token
        # 4.2 组织我们的激活邮件
        html_message = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用美多商城。</p>' \
                       '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                       '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)


        # html_message="点击按钮进行激活 <a href='http://www.itcast.cn/?token=%s'>激活</a>"%token

        # send_mail(subject=subject,
        #           message=message,
        #           from_email=from_email,
        #           recipient_list=recipient_list,
        #           html_message=html_message)
        from celery_tasks.email.tasks import celery_send_email
        celery_send_email.delay(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message
        )

        # 5. 返回响应
        return JsonResponse({'code':0,'errmsg':'ok'})

"""
django 项目
1. django的基础 夯实
2. 需求分析
3. 学习新知识
4. 掌握分析问题，解决问题的能力（debug）
"""

"""

1. 设置邮件服务器

    我们设置 163邮箱服务器
    相当于 我们开启了 让163帮助我们发送邮件。同时设置了 一些信息（特别是授权码）

2.  设置邮件发送的配置信息
    #  让django的哪个类来发送邮件
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    # 邮件服务器的主机和端口号
    EMAIL_HOST = 'smtp.163.com'
    EMAIL_PORT = 25
    
    # 使用我的 163服务器 和 授权码
    #发送邮件的邮箱
    EMAIL_HOST_USER = 'qi_rui_hua@163.com'
    #在邮箱中设置的客户端授权密码
    EMAIL_HOST_PASSWORD = '123456abc'
    
3. 调用  send_mail 方法
"""



"""
需求（知道我们要干什么？？？）：
    激活用户的邮件
前端(用户干了什么，传递了什么参数)：
        用户会点击那个激活连接。那个激活连接携带了token
后端：
    请求：         接收请求，获取参数，验证参数
    业务逻辑：       user_id, 根据用户id查询数据，修改数据
    响应：         返回响应JSON
    
    路由：         PUT     emails/verification/  说明： token并没有在body里
    步骤：
        
        1. 接收请求
        2. 获取参数
        3. 验证参数
        4. 获取user_id
        5. 根据用户id查询数据
        6. 修改数据
        7. 返回响应JSON

"""

class EmailVerifyView(View):

    def put(self,request):
        # 1. 接收请求
        params=request.GET
        # 2. 获取参数
        token=params.get('token')
        # 3. 验证参数
        if token is None:
            return JsonResponse({'code':400,'errmsg':'参数缺失'})
        # 4. 获取user_id
        from apps.users.utils import check_verify_token
        user_id=check_verify_token(token)
        if user_id is None:
            return JsonResponse({'code':400,'errmsg':'参数错误'})
        # 5. 根据用户id查询数据
        user=User.objects.get(id=user_id)
        # 6. 修改数据
        user.email_active=True
        user.save()
        # 7. 返回响应JSON
        return JsonResponse({'code':0,'errmsg':'ok'})

"""
请求
业务逻辑（数据库的增删改查）
响应


增 （注册）
    1.接收数据
    2.验证数据
    3.数据入库
    4.返回响应
    
删 
    1.查询到指定记录
    2.删除数据（物理删除，逻辑删除）
    3.返回响应
    
改  （个人的邮箱）
    1.查询指定的记录
    2.接收数据
    3.验证数据
    4.数据更新
    5.返回响应
    
查   （个人中心的数据展示，省市区）
    1.查询指定数据
    2.将对象数据转换为字典数据
    3.返回响应
"""

from django import http
class AddressCreateView(LoginRequiredJSONMixin, View):

    def post(self, request, RETCODE=None):
        count = request.user.addresses.count()
        if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '超过地址数量上限'})
        # 接收数据
        data=json.loads(request.body.decode())
        # 获取参数，验证参数
        receiver=data.get('receiver')
        province_id=data.get('province_id')
        city_id=data.get('city_id')
        district_id=data.get('district_id')
        place=data.get('place')
        mobile=data.get('mobile')
        tel=data.get('tel')
        email=data.get('email')

        user = request.user
        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseBadRequest('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseBadRequest('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseBadRequest('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseBadRequest('参数email有误')

        # 保存地址信息
        try:
            address = Address.objects.create(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )

            # 设置默认地址
            if not request.user.default_address:
                request.user.default_address = address
                request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '新增地址失败'})

        # 新增地址成功，将新增的地址响应给前端实现局部刷新
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 响应保存结果
        return JsonResponse({'code': 0, 'errmsg': '新增地址成功', 'address': address_dict})


'''
添加浏览记录
前端：
当注册用户访问某一个具体的SKU页面时，axios发送一个请求

后端：
1.接收请求
2.验证数据
3.记录用户id,sku_id,时间
4.将数据保存到redis,去重，每页显示5条信息
5.返回Json数据回前端
'''
from apps.users.models import User
from apps.goods.models import SKU
from django.core.exceptions import ObjectDoesNotExist
from django_redis import get_redis_connection



class UserHistoryView(LoginRequiredJSONMixin, View):

    def post(self, request, user=None):
        # 1.接收请求
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        # 2.验证数据
        try:
            sku = SKU.objects.get(id=sku_id)
        except ObjectDoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '查无此ID'})
        # 3.记录用户id, sku_id, 时间
        # 4.连接redis ---->在setting里单独设定一个redis库 history 保存浏览数据
        redis_cli = redis.Connection('history')
        # 将数据redis去重-->lrem表示先将这个id删除，然后再添加就
        redis_cli.lrem('history_%s'% user.id, sku_id)
        # lpush表示将最新浏览的数据插到最左边 left push
        redis_cli.lpush('history_%s'%user.id, sku_id)
        # 将数据保存到redis, 每页显示5条信息-->0到4共5条
        redis_cli.ltrim('history_%s' % user.id, sku_id, 0, 4)

        # 5.返回Json数据回前端
        return JsonResponse({'code': 0, 'errmsg': 'PASS'})

    def get(self,request):
        # 连接redis
        redis_cli = get_redis_connection('history')
        #获取redis数据
        ids = redis_cli.lrange('history_%s'%request.user.id, 0, 4)
        history_list = []
        for sku_id in ids:
            sku = SKU.objects.get(id=sku_id)
            #将对象转换为字典
            history_list.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image_url,
                'price': sku.price
            })

        return JsonResponse({'code': 0, 'errmsg': 'PASS', 'skus': history_list})