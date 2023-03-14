from django.core.management.base import BaseCommand

from slugify import slugify

from ...models import Product, ProductItem, Brand, Category, Style, Color, ProductItemSizeQuantity, Size


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        brand_names = ['nike', 'adidas', 'puma', 'reebok']
        categories_names = ['t-shirt', 'hoodie', 'sneakers', 'hat']
        style_names = ['sport', 'casual', 'classic', 'retro']
        color_names = ['white', 'black', 'red', 'blue']

        self.create_obj(Brand, brand_names)
        self.create_obj(Category, categories_names)
        self.create_obj(Style, style_names)

        self.create_obj(Color, color_names)

        Product.objects.create(
            name='nike t-shirt',
            slug=slugify('nike t-shirt'),
            description='1',
            brand=Brand.objects.get(name='nike'),
            gender='Men',
            category=Category.objects.get(name='t-shirt'),
            style=Style.objects.get(name='sport'),
        )

        self.create_productitem(color_names, 'nike t-shirt')

        Product.objects.create(
            name='nike hoodie',
            slug=slugify('nike hoodie'),
            description='1',
            brand=Brand.objects.get(name='nike'),
            gender='Men',
            category=Category.objects.get(name='hoodie'),
            style=Style.objects.get(name='sport'),
        )

        self.create_productitem(color_names, 'nike hoodie')

        Product.objects.create(
            name='adidas hoodie',
            slug=slugify('adidas hoodie'),
            description='4',
            brand=Brand.objects.get(name='adidas'),
            gender='Men',
            category=Category.objects.get(name='hoodie'),
            style=Style.objects.get(name='casual'),
        )

        self.create_productitem(color_names, 'adidas hoodie')

        Product.objects.create(
            name='adidas t-shirt',
            slug=slugify('adidas t-shirt'),
            description='1',
            brand=Brand.objects.get(name='adidas'),
            gender='Men',
            category=Category.objects.get(name='t-shirt'),
            style=Style.objects.get(name='casual'),
        )

        self.create_productitem(color_names, 'adidas t-shirt')

        Product.objects.create(
            name='puma sneakers',
            slug=slugify('puma sneakers'),
            description='4',
            brand=Brand.objects.get(name='puma'),
            gender='Men',
            category=Category.objects.get(name='sneakers'),
            style=Style.objects.get(name='classic'),
        )

        self.create_productitem(color_names, 'puma sneakers')

        Product.objects.create(
            name='reebok hat',
            slug=slugify('reebok hat'),
            description='4',
            brand=Brand.objects.get(name='reebok'),
            gender='Men',
            category=Category.objects.get(name='hat'),
            style=Style.objects.get(name='retro'),
        )

        self.create_productitem(color_names, 'reebok hat')

        print('Products where created!')


    def create_obj(self, obj, lst):
        available_models = [Brand, Category, Style, Color]

        if obj not in available_models:
            raise ValueError

        for value in lst:
            obj.objects.create(name=value, slug=slugify(value))

        print(f'Objects were created!')

    def create_productitem(self, lst, obj_name):
        if obj_name == 'puma sneakers':
            for name in lst:
                temp = ProductItem.objects.create(
                           product=Product.objects.get(name=obj_name),
                           SKU=slugify(obj_name),
                           price='119',
                           color=Color.objects.get(name=name),
                       )

                for size in ('44', '44.5', '45'):
                    ProductItemSizeQuantity.objects.create(
                        produc_titem=temp,
                        size=Size.objects.get(name=Size.objects.get(name=size)),
                        quantity=10,
                    )

                temp.save()
        else:
            for name in lst:
                temp = ProductItem.objects.create(
                           product=Product.objects.get(name=obj_name),
                           SKU=slugify(obj_name),
                           price='29',
                           color=Color.objects.get(name=name),
                       )

                for size in ('S', 'M', 'L'):
                    ProductItemSizeQuantity.objects.create(
                        produc_titem=temp,
                        size=Size.objects.get(name=Size.objects.get(name=size)),
                        quantity=50,
                    )

                temp.save()
