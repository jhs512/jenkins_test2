from django.db import models

# Create your models here.

class Product(models.Model):
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('등록날짜', auto_now=True)
    name = models.CharField('내부상품명', max_length=100)
    display_name = models.CharField('노출상품명', max_length=100)
    price = models.PositiveIntegerField('권장판매가격')
    sale_price = models.PositiveIntegerField('실제판매가격')
    hit_count = models.PositiveIntegerField('조회수')
    review_count = models.PositiveIntegerField('리뷰수')
    review_point = models.PositiveIntegerField('리뷰평점')