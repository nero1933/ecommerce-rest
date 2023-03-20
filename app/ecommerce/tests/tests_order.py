from collections import OrderedDict

from ..models import *
from ..utils.tests.tests_mixins import TestMixin


class TestOrderCreate(TestMixin):

    def setUp(self) -> None:
        self.create_user()
        self.create_address()
        self.create_shipping_method()
        self.create_products()

    def test_create_order(self):
        url_name = 'shopping_cart_items-list'
        data1 = {
            "product_item_size_quantity":
                ProductItemSizeQuantity.objects.get(
                    product_item=ProductItem.objects.get(SKU='000001'), size='M').pk,
            "quantity": 2
        }
        data2 = {
            "product_item_size_quantity":
                ProductItemSizeQuantity.objects.get(
                    product_item=ProductItem.objects.get(SKU='000010')).pk,
            "quantity": 1
        }

        response = self.get_response('POST', url_name, data1) # add to shopping cart first item
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        response = self.get_response('POST', url_name, data2) # add to shopping cart second item
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        data = {
            "payment_method": 1,
            "shipping_address": 1,
            "shipping_method": 1,
        }

        response = self.get_response('POST', 'create_order', data, follow=True) # create order
        self.assertEqual(response.redirect_chain, [('/api/v1/order/1', 302)], "Request must redirect to '/api/v1/order/1' with 302 code")
        self.assertEqual(response.status_code, 200, 'Order must be successfully created') # !!! change to 201 when redirect
        self.assertEqual(response.data['order_item'][0]['price'], '58.00', 'Price of first order item must be "58.00"')
        self.assertEqual(response.data['order_item'][1]['price'], '119.00', 'Price of second order item must be "119.00"')
        self.assertEqual(response.data['order_price'], '177.00', 'Order price must be "177.00"')

        response = self.get_response('GET', 'shopping_cart_items-list') # get shopping cart (must be empty)
        self.assertEqual(response.status_code, 200, 'Shopping cart must be displayed to authorized users')
        self.assertEqual(len(response.data), 0, 'Shopping cart must be empty')
