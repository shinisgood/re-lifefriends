from django.db import models

# Create your models here.
class Menu(models.Model):
    name            = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'menus'

class Category(models.Model):
    menu            = models.ForeignKey('Menu',on_delete=models.CASCADE)
    name            = models.CharField(max_length=20)

    class Meta:
        db_table = 'categories'

class Theme(models.Model):
    menu            = models.ForeignKey('Menu',on_delete=models.CASCADE)
    name            = models.CharField(max_length=45)
    products        = models.ManyToManyField('Product',through='ThemeProduct')

    class Meta:
        db_table = 'themes'

class ThemeProduct(models.Model):
    theme           = models.ForeignKey('Theme',on_delete=models.CASCADE)
    product         = models.ForeignKey('Product',on_delete=models.CASCADE)

    class Meta:
        db_table = 'themes_products'

class Product(models.Model):
    category              = models.ForeignKey('Category',on_delete=models.CASCADE)
    name                  = models.CharField(max_length=50)
    cost                  = models.DecimalField(max_digits=9, decimal_places=2)
    created_at            = models.DateTimeField(auto_now_add=True)
    clicks                = models.IntegerField(default=0)
    description_iamge_url = models.URLField(max_length=2000,default='')

    class Meta: 
        db_table = 'products'

class ProductImage(models.Model):
    product         = models.ForeignKey('Product',on_delete=models.CASCADE)
    url             = models.URLField(max_length=2000)

    class Meta:
        db_table = 'product_images'

class Size(models.Model):
    name            = models.CharField(max_length=20)
    products        = models.ManyToManyField('Product',through='ProductSize')

    class Meta:
        db_table = 'sizes'

class ProductSize(models.Model):
    product         = models.ForeignKey('Product',on_delete=models.CASCADE)
    size            = models.ForeignKey('Size',on_delete=models.CASCADE)
    quantity        = models.IntegerField()

    class Meta:
        db_table = 'products_sizes'


