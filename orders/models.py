from django.db import models

# Create your models here.
class ProductOrder(models.Model):
    product_size           = models.ForeignKey('products.ProductSize',on_delete=models.CASCADE)
    order                  = models.ForeignKey('Order',on_delete=models.CASCADE)  
    quantity               = models.IntegerField()
    status                 = models.ForeignKey('Status',on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_orders'

class Order(models.Model):
    user                   = models.ForeignKey('users.User',on_delete=models.CASCADE)
    delivery_address       = models.CharField(max_length=200)
    recipient_phone_number = models.CharField(max_length=45) 
    recipient_name         = models.CharField(max_length=45)
    created_at             = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'

class Status(models.Model):
    status                 = models.CharField(max_length=20)

    class Meta:
        db_table = 'status'
