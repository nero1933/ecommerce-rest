from ..models import ProductItem, ProductItemSizeQuantity
from ..utils.tests.tests_mixins import TestMixin


class TestShoppingCartItem(TestMixin):

    def setUp(self) -> None:
        self.create_user()
        self.create_products()

    def test_shopping_cart_duplicates(self):
        url_name = 'shopping_cart_items-list'
        data = {
            "product_item_size_quantity": ProductItemSizeQuantity.objects.get(
                product_item=ProductItem.objects.get(SKU='000001'), size='M').pk,
            "quantity": 1
        }

        response = self.get_response('GET', url_name)
        self.assertEqual(response.status_code, 200, 'Shopping cart must be displayed to authorized users')

        response = self.get_response('POST', url_name, data)
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        response = self.get_response('POST', url_name, data)
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        response = self.get_response('GET', url_name)
        self.assertEqual(response.status_code, 200, 'Shopping cart items must be displayed to authorized users')
        self.assertEqual(len(response.data), 1, 'There is supposed to be only one product')
        self.assertEqual(response.data[0]['quantity'], 2, 'Quantity must be equal to 2')

    def test_shopping_cart_create_quantity(self):
        url_name = 'shopping_cart_items-list'
        data1 = {
           "product_item_size_quantity": ProductItemSizeQuantity.objects.get(
               product_item=ProductItem.objects.get(SKU='000001'), size='M').pk,
           "quantity": 1000
        }
        data2 = {
           "product_item_size_quantity": ProductItemSizeQuantity.objects.get(
               product_item=ProductItem.objects.get(SKU='000001'), size='L').pk,
           "quantity": 1000
        }

        response = self.get_response('POST', url_name, data1)
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        response = self.get_response('POST', url_name, data2)
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
           "product_item_size_quantity": ProductItemSizeQuantity.objects.get(
               product_item=ProductItem.objects.get(SKU='000001'), size='M').pk,
           "quantity": 1
        }
        data_for_update = {
           "product_item_size_quantity": ProductItemSizeQuantity.objects.get(
               product_item=ProductItem.objects.get(SKU='000001'), size='L').pk,
           "quantity": 1000
        }

        response = self.get_response('POST', url_name, data)
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        detail = {'pk': response.data['id']}

        response = self.get_response('PUT', url_name_for_update, data_for_update, detail)
        self.assertEqual(response.status_code, 200, 'Product must be successfully updated')
        self.assertEqual(response.data['quantity'], 100, 'Quantity must de equal to 50')

        response = self.get_response('GET', url_name, data)
        self.assertEqual(response.status_code, 200, 'Product must be successfully added')
        self.assertEqual(response.data[0]['quantity'], 100, 'Quantity must de equal to 50')
