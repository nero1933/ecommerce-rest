from django.contrib import admin
from ..models.models_products import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Style)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Discount)


class ProductItemSizeQuantityInline(admin.TabularInline):
    model = ProductItemSizeQuantity
    fields = ['size', 'quantity']
    extra = 0


class ImageInline(admin.TabularInline):
    model = Image
    fields = ['main_image', 'image_url', 'description']
    extra = 0


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    model = ProductItem
    inlines = [ProductItemSizeQuantityInline, ImageInline]
#    fields = ('price', )
#    fields = ('products', 'price', 'discount_price', 'SKU', 'quantity', 'gender', 'size', 'color', 'discount', 'created')
#    readonly_fields = ('discount_price', )

    def get_queryset(self, request):
        return ProductItem.objects.all() \
            .select_related('product') \
            .select_related('color')


@admin.register(ProductItemSizeQuantity)
class ProductItemSizeQuantityAdmin(admin.ModelAdmin):
    model = ProductItemSizeQuantity

    def get_queryset(self, request):
        return ProductItemSizeQuantity.objects.all() \
            .select_related('product_item') \
            .select_related('product_item__product') \
            .select_related('product_item__color') \
            .select_related('size')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    model = Image

    def get_queryset(self, request):
        return Image.objects.all() \
            .select_related('product_item') \
            .select_related('product_item__product') \
            .select_related('product_item__color')