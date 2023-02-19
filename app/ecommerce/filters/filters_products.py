from django_filters import rest_framework as filters

from ..models.models_products import Product, Brand, Category, Style, Color, Size


class ProductFilter(filters.FilterSet):

    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
    ]

    brand = filters.ModelChoiceFilter(queryset=Brand.objects.all(), to_field_name='name')
    category = filters.ModelChoiceFilter(queryset=Category.objects.all(), to_field_name='name')
    style = filters.ModelChoiceFilter(queryset=Style.objects.all(), to_field_name='name')
    gender = filters.ChoiceFilter(choices=GENDER_CHOICES)
    product_item__color = filters.ModelChoiceFilter(queryset=Color.objects.all(), to_field_name='name', label='Color')
    product_item__product_item_sizes__size = filters.ModelChoiceFilter(queryset=Size.objects.all(), to_field_name='name', label='Size')

    class Meta:
        model = Product
        fields = ['brand', 'category', 'style', 'product_item__color', 'product_item__product_item_sizes__size']
