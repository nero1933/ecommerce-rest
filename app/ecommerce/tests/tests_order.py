from ..models import *
from ..utils.tests.tests_mixins import TestMixin


class TestOrderCreate(TestMixin):

    def setUp(self) -> None:
        self.user, self.user_data = self.create_user('tests@tests.com')
        self.create_address()
        self.create_shipping_method()
        self.create_products()
        self.create_discount()
        self.pi_1.discount = self.discount_1  # Apply discount to 'nike t-shirt' product item
        self.pi_1.save()

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
            "email": 'test1@test.com',
            "payment_method": 1,
            "shipping_address": {
                'name': 'r',
                'surname': 'n',
                'street': 'dm 15',
                'country': 'Ukraine',
                'region': 'ch',
                'city': 'ch',
                'post_code': 49000,
                'phone': '+380956663321',
            },
            "shipping_method": 1,
        }

        self.client.credentials(HTTP_REFERER='http://127.0.0.1:8000/api/v1/accounts/create_order')
        response = self.get_response('POST', 'create_order', data=data, follow=True) # create order
        self.assertEqual(response.redirect_chain, [('/api/v1/accounts/orders/1/', 302)], "Request must redirect to '/api/v1/accounts/orders/1' with 302 code")
        self.assertEqual(response.status_code, 201, 'Order must be successfully created')
        self.assertEqual(response.data['order_item'][0]['price'], Decimal('46.40'), "Price of first order item must be Decimal('46.40') [discount 20% is applied]")
        self.assertEqual(response.data['order_item'][1]['price'], Decimal('119.00'), "Price of second order item must be '119.00'")
        self.assertEqual(response.data['order_price'], Decimal('165.40'), "Order price must be Decimal('165.40')  [discount 20% is applied to first product]")

        response = self.get_response('GET', 'shopping_cart_items-list') # get shopping cart (must be empty)
        self.assertEqual(response.status_code, 200, 'Shopping cart must be displayed to authorized users')
        self.assertEqual(len(response.data), 0, 'Shopping cart must be empty')
