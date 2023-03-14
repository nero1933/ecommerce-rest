from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.utils import json

from users.models import UserProfile
from ecommerce.models import ShoppingCartItem, ShoppingCart, Product, Brand, Category, Style, ProductItem, Color, \
    ProductItemSizeQuantity, Size


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

        Size.objects.create(name='M')

        ProductItemSizeQuantity.objects.create(
            product_item=ProductItem.objects.get(SKU='000001'),
            size=Size.objects.get(name='M'),
            quantity=100,
        )

    def test_get_products(self):
#        request = self.factory.get(reverse('shopping_cart_items-list'))
        self.assertEqual(ShoppingCart.objects.get(user=self.user).user, self.user)
        self.assertEqual(Product.objects.get(slug='nike_t-shirt').description, '1')
        self.assertEqual(ProductItem.objects.get(SKU='000001').price, 29.00)
        self.assertEqual(ProductItemSizeQuantity.objects.get(quantity=100).size.name, 'M')

    def test_try_unauthenticated(self):
        response = self.client.get(reverse('shopping_cart_items-list'), format='json')
        self.assertEqual(response.status_code, 401, 'Shopping cart must be displayed only to authorized users')

    def get_token(self):
        response = self.client.post(reverse('token_obtain_pair'), self.user_data, format='json')
        self.assertEqual(response.status_code, 200, 'The token should be successfully returned.')

        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content["access"]
        return token

    def test_add_to_shopping_cart(self):
        response = self.client.get(reverse('shopping_cart_items-list'),
                                   {},
                                   HTTP_AUTHORIZATION=f'Bearer {self.get_token()}',
                                   format='json')
        self.assertEqual(response.status_code, 200, 'Shopping cart must be displayed only to authorized users')

        data = {
            "product_item_size_quantity": 1,
            "quantity": 1
        }

        response = self.client.post(reverse('shopping_cart_items-list'),
                                   data,
                                   HTTP_AUTHORIZATION=f'Bearer {self.get_token()}',
                                   format='json')

        response = self.client.post(reverse('shopping_cart_items-list'),
                                    data,
                                    HTTP_AUTHORIZATION=f'Bearer {self.get_token()}',
                                    format='json')

        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        response = self.client.get(reverse('shopping_cart_items-list'),
                                   {},
                                   HTTP_AUTHORIZATION=f'Bearer {self.get_token()}',
                                   format='json')

        self.assertEqual(response.status_code, 200, 'Product must be successfully added')
        print(json.loads(response.content.decode('utf-8')))


    # def test_try1_authenticated(self):
    #
    #     response = self.client.get(reverse('shopping_cart_items-list'),
    #                                {},
    #                                HTTP_AUTHORIZATION=f'Bearer {self.token}',
    #                                format='json')
    #     self.assertEqual(response.status_code, 200)

