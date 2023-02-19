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
admin.site.register(Image)


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


# admin.site.register(ProductItemSizeQuantity)
