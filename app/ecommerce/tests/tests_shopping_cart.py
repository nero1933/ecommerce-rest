from ..models import ProductItem, ProductItemSizeQuantity
from ..utils.tests.tests_mixins import TestMixin


class TestShoppingCartItem(TestMixin):

    def setUp(self) -> None:
        self.user, self.user_data = self.create_user('tests@tests.com')
        self.create_products()

    def test_shopping_cart_duplicates(self):
        url_name = 'shopping_cart_items-list'
        data = {
            "product_item_size_quantity": self.pisq_1.pk,
            "quantity": 1
        }

        response = self.get_response('GET', url_name)
        self.assertEqual(response.status_code, 200, 'Shopping cart must be displayed to authorized users')

        response = self.get_response('POST', url_name, data=data)
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        response = self.get_response('POST', url_name, data=data)
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        response = self.get_response('GET', url_name)
        self.assertEqual(response.status_code, 200, 'Shopping cart items must be displayed to authorized users')
        self.assertEqual(len(response.data), 1, 'There is supposed to be only one product')
        self.assertEqual(response.data[0]['quantity'], 2, 'Quantity must be equal to 2')

    def test_shopping_cart_create_quantity(self):
        url_name = 'shopping_cart_items-list'
        data1 = {
           "product_item_size_quantity": self.pisq_1.pk,
           "quantity": 1000
        }
        data2 = {
           "product_item_size_quantity": self.pisq_2.pk,
           "quantity": 1000
        }

        response = self.get_response('POST', url_name, data=data1)
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        response = self.get_response('POST', url_name, data=data2)
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        response = self.get_response('GET', url_name)
        self.assertEqual(response.status_code, 200, 'Shopping cart items must be displayed to authorized users')
        self.assertEqual(response.data[0]['quantity'], 100, 'Quantity must be equal to 50')
        self.assertEqual(response.data[1]['quantity'], 50, 'Quantity must be equal to 50')
        self.assertEqual(len(response.data), 2, 'There are supposed to be two products')

    def test_shopping_cart_update_quantity(self):
        url_name = 'shopping_cart_items-list'
        url_name_for_update = 'shopping_cart_items-detail'
        data = {
           "product_item_size_quantity": self.pisq_1.pk,
           "quantity": 1
        }
        data_for_update = {
           "product_item_size_quantity": self.pisq_2.pk,
           "quantity": 1000
        }

        response = self.get_response('POST', url_name, data=data)
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        reverse_kwargs = {'pk': response.data['id']}

        response = self.get_response('PUT', url_name_for_update, data=data_for_update, reverse_kwargs=reverse_kwargs)
        self.assertEqual(response.status_code, 200, 'Product must be successfully updated')
        self.assertEqual(response.data['quantity'], 100, 'Quantity must de equal to 100')

        response = self.get_response('GET', url_name)
        self.assertEqual(response.status_code, 200, 'Product must be successfully added')
        self.assertEqual(response.data[0]['quantity'], 100, 'Quantity must de equal to 100')

    def test_add_out_of_stock_item(self):
        url_name = 'shopping_cart_items-list'
        self.pisq_1.quantity = 0 # out of stock
        self.pisq_1.save()
        data = {
           "product_item_size_quantity": self.pisq_1.pk,
           "quantity": 1
        }

        response = self.get_response('POST', url_name, data=data)
        self.assertEqual(response.status_code, 400, "Product can't be added due to out of stock")
