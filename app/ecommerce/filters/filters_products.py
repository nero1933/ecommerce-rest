from django_filters import rest_framework as filters

from ..models.models_products import Product, Brand, Category, Style, Color, ProductItemSizeQuantity
from ..utils.products.products_size_choices import SIZE_CHOICES

class ProductFilter(filters.FilterSet):

    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
    ]

    brand = filters.ModelChoiceFilter(to_field_name='name', queryset=Brand.objects.all())
    category = filters.ModelChoiceFilter(to_field_name='name', queryset=Category.objects.all())
    style = filters.ModelChoiceFilter(to_field_name='name', queryset=Style.objects.all())
    gender = filters.ChoiceFilter(choices=GENDER_CHOICES)
    product_item__color = filters.ModelChoiceFilter(to_field_name='name', label='Color', queryset=Color.objects.all())

    product_item__product_item_size_quantity = \
        filters.ModelChoiceFilter(
            to_field_name='id',
            label='pisq',
            queryset=ProductItemSizeQuantity.objects.all()
            .select_related('product_item')
            .select_related('product_item__product')
            .select_related('product_item__color')
        )

    product_item__product_item_size_quantity__size = \
        filters.ChoiceFilter(
            choices=SIZE_CHOICES,
            label='Size',
            distinct=True,
        )

    class Meta:
        model = Product
        fields = ['brand',
                  'gender',
                  'category',
                  'style',
                  'product_item__color',
                  'product_item__product_item_size_quantity__size',
                  'product_item__product_item_size_quantity',
                  ]
