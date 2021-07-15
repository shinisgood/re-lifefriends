import json
from json import JSONDecodeError


from django.http import JsonResponse
from django.views import View
from django.db.models import Count, Avg
from django.core.exceptions import ObjectDoesNotExist

from reviews.models import ReviewImage
from products.models import Product, ProductSize
from orders.models  import ProductOrder
from reviews.models import Review, ReviewImage
from users.models   import User
from decorators     import validate_login

from users.validations import Validation

class ReviewView(View):
    @validate_login
    def post(self, request, product_id):
        try:
            DELIVERED = 4 # status_id = 4(배송완료) 

            data = json.loads(request.body)
            
            product_size = ProductSize.objects.get(product_id=product_id, size__name=data['product_size'])
            user         = User.objects.get(id=request.account.id)  

            if not ProductOrder.objects.filter(order__user=request.account, status_id=DELIVERED):
                return JsonResponse({'MESSAGE':'NO_PURCHASE_HISTORY'}, status=400)  

            review_info = Review.objects.create(
                product_size = product_size,
                user         = user,
                rating       = data['rating'],
                text         = data['text'],
            )

            ReviewImage.objects.create(
                review_image_url = data['review_image_url'],
                review_id        = review_info.id,
            )

            return JsonResponse({'REVIEW': 'SUCCESS'}, status=200)

        except KeyError: 
            return JsonResponse({'MESSAGE':'INVALID_INPUT'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'MESSAGE':'INVALID_INPUT'}, status=400)
            

    def get (self,request, product_id):
        try:
            product  = Product.objects.get(id=product_id) 
            if not Product.objects.filter(id=product_id).exists():    
                return JsonResponse({'MESSAGE':'INVALID_PRODUCT'}, status=400)
                
            for productsize in product.productsize_set.all():
                reviews = productsize.review_set.all()
                review_info = [{
                    'user_name'    : review.user.name,
                    'created_at'   : review.created_at,
                    'product_size' : review.product_size.size.name,
                    'text'         : review.text,
                    'review_image' : [review_images.review_image_url for review_images in review.reviewimage_set.all()],
                    'rating'       : review.rating,
                    } for review in productsize.review_set.all()]

                rate_average       = reviews.aggregate(rate_average=Avg('rating'))  
                total_review_count = reviews.aggregate(total_review_count=Count('id'))  
                photo_review_count = reviews.aggregate(photo_review_count=Count('reviewimage'))

                review_summary = {
                    'rate_average' : float("%.2f" % rate_average['rate_average']),
                    'rate_count'   : [reviews_count for reviews_count in reviews.values('rating').annotate(rate_count=Count('rating'))],
                    'total_review_count' : total_review_count['total_review_count'],
                    'photo_review_count' : photo_review_count['photo_review_count']
                }

                return JsonResponse({'review_info' :review_info, 'review_summary': review_summary}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'INVALID_PRODUCT'}, status=400)  
        except TypeError:
            return JsonResponse({'MESSAGE':'NO_REVIEW'}, status=400)  
        except ObjectDoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_PRODUCT'}, status=400)  
        
