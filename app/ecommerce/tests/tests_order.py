from ..models import *
from ..utils.tests.tests_mixins import TestMixin


class TestOrderCreate(TestMixin):

    def setUp(self) -> None:
        self.user, self.user_data = self.create_user('tests@tests.com')
        self.create_address()
        self.create_shipping_method()
        self.create_discount()
        self.create_products()
        self.pi_1.discount = self.discount_1  # Apply discount to 'nike t-shirt' product item

    def test_create_order(self):
        # Try to fill in shopping cart and create order
        # must be created successfully

        url_name = 'shopping_cart_items-list'
        data1 = {
            "product_item_size_quantity": self.pisq_1.pk,
            "quantity": 2
        }
        data2 = {
            "product_item_size_quantity": self.pisq_3.pk,
            "quantity": 1
        }

        response = self.get_response('POST', url_name, data=data1) # add to shopping cart first item
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        response = self.get_response('POST', url_name, data=data2) # add to shopping cart second item
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        data = {
            "payment_method": 1,
            "shipping_address": 1,
            "shipping_method": 1,
        }

        response = self.get_response('POST', 'create_order', data=data, follow=True) # create order
        self.assertEqual(response.redirect_chain, [('/api/v1/accounts/orders/1/', 302)], "Request must redirect to '/api/v1/accounts/orders/1' with 302 code")
        self.assertEqual(response.status_code, 200, 'Order must be successfully created') # !!! change to 201 when redirect
        self.assertEqual(response.data['order_item'][0]['price'], Decimal('58.00'), "Price of first order item must be '58.00'")
        self.assertEqual(response.data['order_item'][1]['price'], Decimal('119.00'), "Price of second order item must be '119.00'")
        self.assertEqual(response.data['order_price'], Decimal('177.00'), "Order price must be '177.00'")

        response = self.get_response('GET', 'shopping_cart_items-list') # get shopping cart (must be empty)
        self.assertEqual(response.status_code, 200, 'Shopping cart must be displayed to authorized users')
        self.assertEqual(len(response.data), 0, 'Shopping cart must be empty')
