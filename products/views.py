import json
import random

from typing import Text
from json import JSONDecodeError

from django.http                import JsonResponse
from django.views               import View
from django.db.models           import Q, Count, Sum, Avg
from django.db.models.functions import Coalesce
from django.core.exceptions     import ObjectDoesNotExist

from users.validations          import Validation
from products.models            import Menu, Product
from decorators                 import validate_login

class ProductView(View):
    def get(self,request, product_id):
        try: 
            product = Product.objects.get(id=product_id) 

            product_detail = {
                'product_id' : product.id,
                'images'     : [product_images.url for product_images in product.productimage_set.all()],
                'menu'       : product.category.menu.name,
                'category'   : product.category.name,
                'name'       : product.name,
                'cost'       : product.cost,
                'clicks'     : product.clicks,
                'description': product.description_iamge_url,
                'size'       : [product_size.name for product_size in product.size_set.all()]
            }
            
            return JsonResponse({'productdetail': product_detail}, status=200)
       
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND_PRODUCT_ID'}, status=400)

class ProductListView(View):
    def get(self, request):
        MAX_THEME_MENU_ID = 7
        try:
            menu     = request.GET.get('menu', None)
            category = request.GET.get('category', None)
            theme    = request.GET.get('theme', None)
            size     = int(request.GET.get('size', '200'))
            page     = int(request.GET.get('page', '1'))

            list_criteria = {}
            if menu:
                if Menu.objects.get(name=menu).id < MAX_THEME_MENU_ID:
                    list_criteria['theme__menu__name'] = menu
                else:
                    list_criteria['category__menu__name'] = menu
            elif category:
                list_criteria['category__name'] = category
            elif theme:
                list_criteria['theme__name'] = theme

            sort_criteria = {
                    None           : '-clicks',
                    'POPULAR'      : '-clicks',
                    'TOTALSALE'    : '-sold',
                    'LOWPRICE'     : 'cost',
                    'RECENT'       : '-created_at',
                    'REVIEW'       : '-review_count',
                    'SATISFACTION' : '-rating'
            }
            sort = request.GET.get('sort', None)
            sort = None if sort not in sort_criteria else sort

            offset   = (page-1) * size
            limit    = page * size

            products = Product.objects\
                    .filter(**list_criteria)\
                    .annotate(
                            review_count=Count('productsize__review'),
                            rating=Coalesce(Avg('productsize__review__rating'), 0.0),
                            sold=Coalesce(Sum('productsize__productorder__quantity',
                                filter=Q(productsize__productorder__status__id__range=(2,4))), 0)
                            )\
                    .order_by(sort_criteria[sort])[offset:limit]

            results = [
                    {
                        'id'          : product.id,
                        'name'        : product.name,
                        'cost'        : int(product.cost),
                        'created_at'  : product.created_at,
                        'clicks'      : product.clicks,
                        'imgUrl'      : product.productimage_set.first().url,
                        'imgAlt'      : product.name,
                        'reviewCount' : product.review_count,
                        'rating'      : product.rating,
                        'sold'        : product.sold
                    } for product in products
            ]

            total_num = Product.objects.filter(**list_criteria).count()
                   
            return JsonResponse({'message': results, 'TOTAL_NUM': total_num}, status=200)
        except Menu.DoesNotExist:
            return JsonResponse({'message': 'INVALID_KEYWORD'}, status=400)
        except ValueError:
            return JsonResponse({'message': 'INVALID_KEYWORD'}, status=400)

class SearchView(View):
    def get(self,request):
        product_name = request.GET.get('search')
        products = Product.objects.filter(name__contains=product_name)
        try: 
            sort = request.GET.get('sort', None)
            if sort is None:
                sorted_products = products.order_by('name')
            if sort == 'LOWPRICE':
                sorted_products = products.order_by('cost')
            if sort == 'HIGHPRICE':
                sorted_products = products.order_by('-cost')
            if sort == 'RECENT':
                sorted_products = products.order_by('created_at')
            if sort == 'REVIEW':
                sorted_products = products.annotate(count_review=Count('productsize__review')).order_by('count_review')
            product_info = [{
                'category'  : product.category.name,
                'name'      : product.name,
                'cost'      : product.cost,
                'image_url' : product.productimage_set.first().url,
                'created_at': product.created_at,
            } for product in sorted_products]
            
            return JsonResponse({'results':product_info}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=200)

class MenuView(View):
    def get(self,request):
        try:
            menus = [{
                    'id'        : menu.id,
                    'menu'      : menu.name,
                    'categories': [{
                            'id'      : category.id, 
                            'category': category.name
                    } for category in menu.category_set.all()] + [{
                            'id'      : theme.id, 
                            'category': theme.name
                    } for theme in menu.theme_set.all() 
                    if theme.name != menu.name]
            } for menu in Menu.objects.all()]
                    
            return JsonResponse({'results':menus}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)