from django.shortcuts import render
from utils.goods import get_categories
from django.views import View
from apps.contents.models import ContentCategory
from django.http import JsonResponse

class IndexView(View):

    def get(self, request):

        # 商品分类数据
        categories = get_categories()

        #广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        context = {
            'categories': categories,
            'contents': contents,
        }

        return render(request, 'index.html', context)


'''
前端
前端发送一个axios，分类id在路由中
分页的页码、每页多少条数据、排序--->前端要传过来的数据

后端
请求  接收请求
业务逻辑  根据需求查义数据，将查询数据转换为字典数据
响应 Json

路由  GET /list/category_id/sku/

'''
from apps.goods.models import GoodsCategory
from django.core.exceptions import ObjectDoesNotExist
from utils.goods import get_breadcrumb
from apps.goods.models import SKU



class ListView(View):

    def get(self, request, category_id):
        # 排序字段
        ordering = request.GET.get('ordering')
        # 分页数据--->每页数据大小（从前端获取）
        page_size = request.GET.get('page_size')
        # 获取页码
        page = request.GET.get('page')


        try:
            category = GoodsCategory.objects.get(id=category_id)
        except ObjectDoesNotExist:
            return JsonResponse({'code':400, 'errmsg':'参数缺失'})

        # 获取面包屑数据
        breadcrumb = get_breadcrumb(category)

        # 查询分类对应的SKU数据--> 排序 ---> 分页
        skus = SKU.objects.filter(category=category).order_by(ordering)

        # 分页：两个参数 1.要分页的数据列表  skus; 2.每页的多少条数据 per_page，从前端获取
        from django.core.paginator import Paginator
        paginator = Paginator(skus, per_page=page_size)
        #获取某一页的数据
        page_skus = paginator.page(page)
        #将对象转换为列表数据
        sku_list= []
        for sku in page_skus.object_list:
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url
            })

        # 获取总页数
        total_page = paginator.num_pages

        #返回响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'PASS',
            'list': sku_list,
            'count': total_page,
            'breadcrumb': breadcrumb})


'''
程序员与搜索之间用 haystack 与 elasticsearch 连接----> 我---haystack---elasticsearch
'''
from haystack.views import SearchView
from django.http import JsonResponse

class SKUSearch(SearchView):
    def create_response(self):
        context = self.get_context()
        sku_list = []
        for sku in context ['page'].object_list:
            sku_list.append({
                'id': sku.object.id,
                'name': sku.object.name,
                'price': sku.object.price,
                'default_image_url': sku.object.default_image.url,
                'searchkey': context.get('query'),
                'page_size': context['page'].paginator.num_pages,
                'count': context['page'].paginator.count
            })

        return JsonResponse(sku_list, safe=False)


"""
需求：
    详情页面

    1.分类数据
    2.面包屑
    3.SKU信息
    4.规格信息


    我们的详情页面也是需要静态化实现的。
    但是我们再讲解静态化之前，应该可以先把 详情页面的数据展示出来

"""
from utils.goods import get_categories
from utils.goods import get_breadcrumb
from utils.goods import get_goods_specs


class DetailView(View):

    def get(self, request, sku_id):
        try:
            sku = SKU.objects.get(id=sku_id)
        except ObjectDoesNotExist:
            pass
        # 1.分类数据
        categories = get_categories()
        # 2.面包屑
        breadcrumb = get_breadcrumb(sku.category)
        # 3.SKU信息
        # 4.规格信息
        goods_specs = get_goods_specs(sku)

        context = {

            'categories': categories,
            'breadcrumb': breadcrumb,
            'sku': sku,
            'specs': goods_specs,

        }
        return render(request, 'detail.html', context)


"""
需求：
    统计每一天的分类商品访问量

前端：
    当访问具体页面的时候，会发送一个axios请求。携带分类id
后端：
    请求：         接收请求，获取参数
    业务逻辑：       查询有没有，有的话更新数据，没有新建数据
    响应：         返回JSON

    路由：     POST    detail/visit/<category_id>/
    步骤：

        1.接收分类id
        2.验证参数（验证分类id）
        3.查询当天 这个分类的记录有没有
        4. 没有新建数据
        5. 有的话更新数据
        6. 返回响应


"""
from apps.goods.models import GoodsVisitCount
from datetime import date


class CategoryVisitCountView(View):

    def post(self, request, category_id):
        # 1.接收分类id
        # 2.验证参数（验证分类id）
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except ObjectDoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '没有此分类'})
        # 3.查询当天 这个分类的记录有没有

        today = date.today()
        try:
            gvc = GoodsVisitCount.objects.get(category=category, date=today)
        except ObjectDoesNotExist:
            # 4. 没有新建数据
            GoodsVisitCount.objects.create(category=category,
                                           date=today,
                                           count=1)
        else:
            # 5. 有的话更新数据
            gvc.count += 1
            gvc.save()
        # 6. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})



# 以下是图片上传到容器的代码
# # Create your views here.
# from fdfs_client.client import Fdfs_client,get_tracker_conf
#
# tracker_conf = get_tracker_conf('utils/fastdfs/client.conf')
#
# client = Fdfs_client(trackers=tracker_conf)
#
# client.upload_by_filename('/home/jacky/桌面/test_1/veer-307491791.jpg')



