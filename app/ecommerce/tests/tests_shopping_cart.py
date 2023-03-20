from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from ..models import UserProfile, Product, Brand, Category, Style, ProductItem, Color, ProductItemSizeQuantity


class TestShoppingCartItem(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

        self.user = UserProfile.objects \
            .create_user(email='tests@tests.com',
                         name='tests',
                         phone='+380951112233',
                         password='123456'
                         )

        self.user_data = {
            "email": "tests@tests.com",
            "password": "123456"
        }

        Brand.objects.create(name='nike', slug='nike')
        Category.objects.create(name='t-shirt', slug='t-shirt')
        Style.objects.create(name='sport', slug='sport')

        Product.objects.create(
            name='nike t-shirt',
            slug='nike_t-shirt',
            description='1',
            brand=Brand.objects.get(name='nike'),
            gender='Men',
            category=Category.objects.get(name='t-shirt'),
            style=Style.objects.get(name='sport'),
        )

        Color.objects.create(name='white', slug='white')

        ProductItem.objects.create(
            product=Product.objects.get(slug='nike_t-shirt'),
            SKU='000001',
            price='29',
            color=Color.objects.get(name='white'),
        )

        ProductItemSizeQuantity.objects.create(
            product_item=ProductItem.objects.get(SKU='000001'),
            size='M',
            quantity=100,
        )

        ProductItemSizeQuantity.objects.create(
            product_item=ProductItem.objects.get(SKU='000001'),
            size='L',
            quantity=50,
        )

    def get_token(self):
        response = self.client.post(reverse('token_obtain_pair'), self.user_data, format='json')
        self.assertEqual(response.status_code, 200, 'The token should be successfully returned.')

        return response.data['access']

    def get_response(self, method, url_name, data=None, detail=None):
        if data is None:
            data = {}

        if method == 'GET':
            return self.client.get(reverse(url_name),
                                   data,
                                   HTTP_AUTHORIZATION=f'Bearer {self.get_token()}',
                                   format='json'
                                   )
        elif method == 'POST':
            return self.client.post(reverse(url_name),
                                   data,
                                   HTTP_AUTHORIZATION=f'Bearer {self.get_token()}',
                                   format='json'
                                   )
        elif method == 'PUT':
            return self.client.put(reverse(url_name, kwargs=detail),
                                   data,
                                   HTTP_AUTHORIZATION=f'Bearer {self.get_token()}',
                                   format='json'
                                   )
        return None

    def test_shopping_cart_duplicates(self):
        url_name = 'shopping_cart_items-list'
        data = {
            "product_item_size_quantity": ProductItemSizeQuantity.objects.get(quantity=100).pk,
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
           "product_item_size_quantity": ProductItemSizeQuantity.objects.get(quantity=50).pk,
           "quantity": 1000
        }
        data2 = {
           "product_item_size_quantity": ProductItemSizeQuantity.objects.get(quantity=100).pk,
           "quantity": 1000
        }

        response = self.get_response('POST', url_name, data1)
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        response = self.get_response('POST', url_name, data2)
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        response = self.get_response('GET', url_name)
        self.assertEqual(response.status_code, 200, 'Shopping cart items must be displayed to authorized users')
        self.assertEqual(response.data[0]['quantity'], 50, 'Quantity must be equal to 50')
        self.assertEqual(response.data[1]['quantity'], 100, 'Quantity must be equal to 50')
        self.assertEqual(len(response.data), 2, 'There are supposed to be two products')

    def test_shopping_cart_update_quantity(self):
        url_name = 'shopping_cart_items-list'
        url_name_for_update = 'shopping_cart_items-detail'
        data = {
           "product_item_size_quantity": ProductItemSizeQuantity.objects.get(quantity=50).pk,
           "quantity": 1
        }
        data_for_update = {
           "product_item_size_quantity": ProductItemSizeQuantity.objects.get(quantity=50).pk,
           "quantity": 1000
        }

        response = self.get_response('POST', url_name, data)
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        detail = {'pk': response.data['id']}

        response = self.get_response('PUT', url_name_for_update, data_for_update, detail)
        self.assertEqual(response.status_code, 200, 'Product must be successfully updated')
        self.assertEqual(response.data['quantity'], 50, 'Quantity must de equal to 50')

        response = self.get_response('GET', url_name, data)
        self.assertEqual(response.status_code, 200, 'Product must be successfully added')
        self.assertEqual(response.data[0]['quantity'], 50, 'Quantity must de equal to 50')
