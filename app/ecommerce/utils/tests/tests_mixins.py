from django.contrib.auth import authenticate, login, logout
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ecommerce.models import UserProfile, Address, ShippingMethod, Brand, Category, Style, Product, Color, ProductItem, \
    ProductItemSizeQuantity, ShoppingCart, ShoppingCartItem


class TestMixin(APITestCase):

    def create_user(self, email):
        user = UserProfile.objects \
            .create_user(email=email,
                         name='tests',
                         phone='+380951112233',
                         password='123456'
                         )

        user_data = {"email": email, "password": "123456"}

        return user, user_data


    def create_address(self):
        self.address_1 = \
            Address.objects.create(
                name='r',
                surname='n',
                street='dm 15',
                country='Ukraine',
                region='ch',
                city='ch',
                post_code=49000,
                phone='+380956663321',
                )

    def create_shipping_method(self):
        self.shipping_method_1 = ShippingMethod.objects.create(delivery_company_name='DHL')

    def create_products(self):
        Brand.objects.create(name='nike', slug='nike')
        Category.objects.create(name='t-shirt', slug='t-shirt')
        Style.objects.create(name='sport', slug='sport')

        Brand.objects.create(name='puma', slug='puma')
        Category.objects.create(name='hoodie', slug='hoodie')
        Style.objects.create(name='casual', slug='casual')

        self.p1 = Product.objects.create(
            name='nike t-shirt',
            slug='nike_t-shirt',
            description='1',
            brand=Brand.objects.get(name='nike'),
            gender='Men',
            category=Category.objects.get(name='t-shirt'),
            style=Style.objects.get(name='sport'),
        )

        self.p2 = Product.objects.create(
            name='puma hoodie',
            slug='puma_hoodie',
            description='1',
            brand=Brand.objects.get(name='puma'),
            gender='Women',
            category=Category.objects.get(name='hoodie'),
            style=Style.objects.get(name='casual'),
        )

        Color.objects.create(name='white', slug='white')
        Color.objects.create(name='black', slug='black')

        ProductItem.objects.create(
            product=Product.objects.get(slug='nike_t-shirt'),
            SKU='000001',
            price='29',
            color=Color.objects.get(name='white'),
        )

        ProductItem.objects.create(
            product=Product.objects.get(slug='puma_hoodie'),
            SKU='000010',
            price='119',
            color=Color.objects.get(name='black'),
        )

        # nike t-shirt / Color: white / Size: M / Quantity: 100
        self.pisq_1 = ProductItemSizeQuantity.objects.create(
            product_item=ProductItem.objects.get(SKU='000001'),
            size='M',
            quantity=100,
        )

        # nike t-shirt / Color: black / Size: M / Quantity: 50
        self.pisq_2 = ProductItemSizeQuantity.objects.create(
            product_item=ProductItem.objects.get(SKU='000001'),
            size='L',
            quantity=50,
        )

        # puma hoodie / Color: black / Size: M / Quantity: 50
        self.pisq_3 = ProductItemSizeQuantity.objects.create(
            product_item=ProductItem.objects.get(SKU='000010'),
            size='M',
            quantity=50,
        )

    def get_token(self, user_data):
        response = self.client.post(reverse('token_obtain_pair'), user_data, format='json')
        self.assertEqual(response.status_code, 200, 'The token should be successfully returned.')

        return response.data['access']

    def fill_shopping_cart(self, user, user_data, items=3):
        self.get_token(user_data)
        cart = ShoppingCart.objects.get(user=user)


        if items >= 1:
            ShoppingCartItem.objects.create(cart=cart,
                                            product_item_size_quantity=self.pisq_1,
                                            quantity=1,
                                            item_price=self.pisq_1.product_item.price,
                                            )
        if items >= 2:
            ShoppingCartItem.objects.create(cart=cart,
                                            product_item_size_quantity=self.pisq_2,
                                            quantity=1,
                                            item_price=self.pisq_2.product_item.price,
                                            )
        if items >= 3:
            ShoppingCartItem.objects.create(cart=cart,
                                            product_item_size_quantity=self.pisq_3,
                                            quantity=1,
                                            item_price=self.pisq_3.product_item.price,
                                            )

    def create_order(self, user_data):
        data = {
            "payment_method": 1,
            "shipping_address": self.address_1.pk,
            "shipping_method": self.shipping_method_1.pk,
        }

        response = self.get_response('POST', 'create_order', data=data, user_data=user_data, follow=True)
        order_id = response.data['id']
        order_item_id = [item['id'] for item in response.data['order_item']]
        return order_id, order_item_id

    def get_response(self, method, url_name, reverse_kwargs=None, data=None, user_data=None, **kwargs):
        if user_data is None:
            user_data = self.user_data

        if data is None:
            data = {}

        if method == 'GET':
            return self.client.get(reverse(url_name, kwargs=reverse_kwargs),
                                   data,
                                   HTTP_AUTHORIZATION=f'Bearer {self.get_token(user_data)}',
                                   format='json',
                                   **kwargs)
        elif method == 'POST':
            return self.client.post(reverse(url_name, kwargs=reverse_kwargs),
                                    data,
                                    HTTP_AUTHORIZATION=f'Bearer {self.get_token(user_data)}',
                                    format='json',
                                    **kwargs)
        elif method == 'PUT':
            return self.client.put(reverse(url_name, kwargs=reverse_kwargs),
                                   data,
                                   HTTP_AUTHORIZATION=f'Bearer {self.get_token(user_data)}',
                                   format='json',
                                   **kwargs)

        return None
