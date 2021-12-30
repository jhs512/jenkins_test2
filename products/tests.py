import django.test

from products.models import Product


class ProductModelTests(django.test.TestCase):

    def test_1(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """

        self.assertIs(Product.objects.order_by('id').first().id, 1)
