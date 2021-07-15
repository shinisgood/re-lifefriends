import json

from django.http       import JsonResponse
from django.views      import View

from products.models   import ProductSize
from orders.models     import Order, ProductOrder
from decorators        import validate_login

CART_STATUS_ID = 1

class CartView(View):
    @validate_login
    def post(self, request):
        try:
            data       = json.loads(request.body)
            product_id = data['product_id']
            size_name  = data['size']
            quantity   = int(data['quantity'])
            user       = request.account

            product_size = ProductSize.objects.filter(
                    product_id = product_id,
                    size__name = size_name
                    ).first()

            if quantity > product_size.quantity: 
                return JsonResponse({'MESSAGE': 'NO_INVENTORY', 'INVENTORY': product_size.quantity}, status=400)
            
            order = Order.objects.filter(user=user).first() \
                    or Order.objects.create(
                            user                   = user,
                            delivery_address       = 'address',
                            recipient_name         = user.name,
                            recipient_phone_number = user.phone_number
                            )

            product_order = ProductOrder.objects.filter(
                    order=order, 
                    product_size=product_size, 
                    status_id=CART_STATUS_ID
                    ).first()
            if product_order:
                product_order.quantity = quantity
                product_order.save()
            else:
                product_order = ProductOrder.objects.create(
                        order        = order,
                        product_size = product_size,
                        quantity     = quantity,
                        status_id    = CART_STATUS_ID
                        )

            cart = make_cart(user)
            
            return JsonResponse({'MESSAGE': 'SUCCESS', 'CART': cart}, status=201)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'NO_BODY'}, status=400)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

    @validate_login
    def get(self, request):
        user = request.account
        orders = Order.objects.filter(user=user)

        if not orders:
            return JsonResponse({'MESSAGE': 'EMPTY_CART'}, status=400)

        cart = make_cart(user)

        return JsonResponse({'MESSAGE': 'SUCCESS', 'CART': cart}, status=200)

    @validate_login
    def delete(self, request):
        data       = json.loads(request.body)
        product_id = data['product_id']
        size_name  = data['size']
        user       = request.account

        ProductOrder.objects.filter(
                order__user              = user,
                product_size__product_id = product_id,
                product_size__size__name = size_name,
                status_id                = CART_STATUS_ID
                ).delete()

        cart = make_cart(user)

        return JsonResponse({'MESSAGE': 'SUCCESS', 'CART': cart}, status=201)

class PurchaseView(View):
    @validate_login
    def post(self, request):
        try:
            data       = json.loads(request.body)
            product_id = data['product_id']
            size_name  = data['size']
            quantity   = int(data['quantity'])
            user       = request.account

            product_size = ProductSize.objects.filter(
                    product_id = product_id,
                    size__name = size_name
                    ).first()

            if quantity > product_size.quantity: 
                return JsonResponse({'MESSAGE': 'NO_INVENTORY', 'INVENTORY': product_size.quantity}, status=400)

            product_order = ProductOrder.objects.filter(
                    order__user  = user,
                    product_size = product_size,
                    status_id    = CART_STATUS_ID,
                    quantity     = quantity
                    ).first()
            if not product_order:
                return JsonResponse({'MESSAGE': 'NO_PRODUCT'}, status=400)
            else:
                product_size.quantity -= quantity
                product_size.save()
                product_order.status_id += 1
                product_order.save()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'NO_BODY'}, status=400)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

def make_cart(user):
    product_orders = ProductOrder.objects.filter(order__user=user, status_id=CART_STATUS_ID)
    cart = [{
        'user_name'    : product_order.order.user.name,
        'product_name' : product_order.product_size.product.name,
        'product_size' : product_order.product_size.size.name,
        'quantity'     : product_order.quantity,
        'img_url'      : product_order.product_size.product.productimage_set.first().url
        } for product_order in product_orders]
    return cart


