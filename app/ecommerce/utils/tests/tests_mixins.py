from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ecommerce.models import UserProfile, Address, ShippingMethod, Brand, Category, Style, Product, Color, ProductItem, \
    ProductItemSizeQuantity


class TestMixin(APITestCase):

    def create_user(self):
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

    def create_address(self):
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
        ShippingMethod.objects.create(delivery_company_name='DHL')

    def create_products(self):
        Brand.objects.create(name='nike', slug='nike')
        Category.objects.create(name='t-shirt', slug='t-shirt')
        Style.objects.create(name='sport', slug='sport')

        Brand.objects.create(name='puma', slug='puma')
        Category.objects.create(name='hoodie', slug='hoodie')
        Style.objects.create(name='casual', slug='casual')

        Product.objects.create(
            name='nike t-shirt',
            slug='nike_t-shirt',
            description='1',
            brand=Brand.objects.get(name='nike'),
            gender='Men',
            category=Category.objects.get(name='t-shirt'),
            style=Style.objects.get(name='sport'),
        )

        Product.objects.create(
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

        ProductItemSizeQuantity.objects.create(
            product_item=ProductItem.objects.get(SKU='000010'),
            size='M',
            quantity=50,
        )

    def get_token(self):
        response = self.client.post(reverse('token_obtain_pair'), self.user_data, format='json')
        self.assertEqual(response.status_code, 200, 'The token should be successfully returned.')

        return response.data['access']


    def get_response(self, method, url_name, data=None, detail=None, **kwargs):
        if data is None:
            data = {}

        if method == 'GET':
            return self.client.get(reverse(url_name),
                                   data,
                                   HTTP_AUTHORIZATION=f'Bearer {self.get_token()}',
                                   format='json',
                                   **kwargs
                                   )
        elif method == 'POST':
            return self.client.post(reverse(url_name),
                                    data,
                                    HTTP_AUTHORIZATION=f'Bearer {self.get_token()}',
                                    format='json',
                                    **kwargs
                                    )
        elif method == 'PUT':
            return self.client.put(reverse(url_name, kwargs=detail),
                                   data,
                                   HTTP_AUTHORIZATION=f'Bearer {self.get_token()}',
                                   format='json',
                                   **kwargs
                                   )
        return None