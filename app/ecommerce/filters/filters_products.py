from django_filters import rest_framework as filters

from ..models.models_products import Product, Brand, Category, Style


class ProductFilter(filters.FilterSet):

    brand = filters.ModelChoiceFilter(queryset=Brand.objects.all(), to_field_name='name')
    category = filters.ModelChoiceFilter(queryset=Category.objects.all(), to_field_name='name')
    style = filters.ModelChoiceFilter(queryset=Style.objects.all(), to_field_name='name')

    class Meta:
        model = Product
        fields = ['brand', 'category', 'style']
