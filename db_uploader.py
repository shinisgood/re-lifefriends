import os
import django
import csv
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'life_friends.settings') 
django.setup() 

from products.models import * 
from users.models import *
from orders.models import *


CSV_PATH_PRODUCTS = './CSV/menu.csv'  # 가지고있는 CSV경로도 변수화 해서 저장
with open(CSV_PATH_PRODUCTS) as in_file: # CSV_PATH_PRODUCTS 경로에서 in_file 이란 이름으로 파일열기
    data_reader = csv.reader(in_file)  # 데이터 한줄 씩 읽기
    next(data_reader, None) # 첫줄을 스킵하기위해 추가
    for row in data_reader:  
        if row[0]:
            menu_name = row[0]
            update, create = Menu.objects.update_or_create(name=menu_name)
    update.save()

CSV_PATH_PRODUCTS= './CSV/category.csv'
with open(CSV_PATH_PRODUCTS) as in_file: 
    data_reader = csv.reader(in_file) 
    next(data_reader, None)
    for row in data_reader:  
        if row[0]:
            menu_name = row[0]
        category_name = row[1]
        menu_id=Menu.objects.get(name=menu_name)
        update, create = Category.objects.update_or_create(menu=menu_id, name=category_name)
    update.save()

CSV_PATH_PRODUCTS= './CSV/theme.csv'
with open(CSV_PATH_PRODUCTS) as in_file: 
    data_reader = csv.reader(in_file) 
    next(data_reader, None)
    for row in data_reader:  
        if row[0]:
            menu_name = row[0]
        theme_name = row[1]
        menu_id=Menu.objects.get(name=menu_name)
        update, create = Theme.objects.update_or_create(menu=menu_id, name=theme_name)
    update.save()

CSV_PATH_PRODUCTS= './CSV/product.csv'
with open(CSV_PATH_PRODUCTS) as in_file: 
    data_reader = csv.reader(in_file) 
    next(data_reader, None)
    for row in data_reader:  
        category_name = row[0]
        product_name = row[1]
        cost = row[2]
        description_iamge_url = row[3]
        category_object=Category.objects.get(name=category_name)
        update, create = Product.objects.update_or_create(
            category=category_object, 
            name=product_name,
            cost=float(cost),
            description_iamge_url=description_iamge_url
            )
    update.save()

CSV_PATH_PRODUCTS= './CSV/productimage.csv'
with open(CSV_PATH_PRODUCTS) as in_file: 
    data_reader = csv.reader(in_file) 
    next(data_reader, None)
    for row in data_reader:  
        product_name = row[1]
        url = row[3]
        product_name=Product.objects.get(name=product_name)
        update, create = ProductImage.objects.update_or_create(
            product=product_name, 
            url=url,
            )
    update.save()

CSV_PATH_PRODUCTS= './CSV/size.csv'
with open(CSV_PATH_PRODUCTS) as in_file: 
    data_reader = csv.reader(in_file) 
    next(data_reader, None)
    for row in data_reader:  
        size = row[0]
        update, create = Size.objects.update_or_create(
            name=size
            )
    update.save()

CSV_PATH_PRODUCTS= './CSV/gender.csv'
with open(CSV_PATH_PRODUCTS) as in_file: 
    data_reader = csv.reader(in_file) 
    next(data_reader, None)
    for row in data_reader:  
        gender = row[0]
        update, create = Gender.objects.update_or_create(
            gender=gender
            )
    update.save()

CSV_PATH_PRODUCTS= './CSV/status.csv'
with open(CSV_PATH_PRODUCTS) as in_file: 
    data_reader = csv.reader(in_file) 
    next(data_reader, None)
    for row in data_reader:  
        status = row[0]
        update, create = Status.objects.update_or_create(
            status=status
            )
    update.save()

CSV_PATH_PRODUCTS= './CSV/coupon.csv'
with open(CSV_PATH_PRODUCTS) as in_file: 
    data_reader = csv.reader(in_file) 
    next(data_reader, None)
    for row in data_reader:  
        coupon = row[0]
        update, create = Coupon.objects.update_or_create(
            coupon=coupon
            )
    update.save()

CSV_PATH_PRODUCTS= './CSV/productsize.csv'
with open(CSV_PATH_PRODUCTS) as in_file: 
    data_reader = csv.reader(in_file) 
    next(data_reader, None)
    for row in data_reader:  
        product_name = row[0]
        size = row[1]
        quantity = row[2]
        update, create = ProductSize.objects.update_or_create(
            product  = Product.objects.get(name=product_name),
            size     = Size.objects.get(name=size),
            quantity = int(quantity)
            )
    update.save()

CSV_PATH_PRODUCTS= './CSV/themeproduct.csv'
with open(CSV_PATH_PRODUCTS) as in_file: 
    data_reader = csv.reader(in_file) 
    next(data_reader, None)
    for row in data_reader:  
        theme_name = row[1]
        product_name = row[2]
        print(theme_name, product_name)
        update, create = ThemeProduct.objects.update_or_create(
            product  = Product.objects.get(name=product_name),
            theme     = Theme.objects.get(name=theme_name),
            )
    update.save()
