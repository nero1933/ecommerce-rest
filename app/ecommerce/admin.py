from django.contrib import admin
from .models.models_products import *

# Register your models here.
admin.site.register(Product)
# admin.site.register(ProductItem)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Style)
admin.site.register(Color)
admin.site.register(Discount)

@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    model = ProductItem
#    fields = ('price', )
#    fields = ('product', 'price', 'discount_price', 'SKU', 'quantity', 'gender', 'size', 'color', 'discount', 'created')
#    readonly_fields = ('discount_price', )

#admin.site.register(ProductItem, ProductItemAdmin)