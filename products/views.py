from django.http import HttpResponse, HttpRequest

from products.models import Product


def product_list(request: HttpRequest):
    return HttpResponse(Product.objects.all())
