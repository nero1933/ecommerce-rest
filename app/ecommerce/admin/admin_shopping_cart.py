from django.contrib import admin
from ..models.models_shopping_cart import *

admin.site.register(ShoppingCart)



@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(admin.ModelAdmin):
    model = ShoppingCartItem
#    list_select_related = ('product_item_size_quantity', 'size', )
    readonly_fields = ('cart', )

    def get_queryset(self, request):
        queryset = ShoppingCartItem.objects.all() \
            .select_related('product_item_size_quantity') \
            .select_related('product_item_size_quantity__size') \

        return queryset

    # def get_object(self, request, object_id, from_field=None):
    #     obj = ShoppingCartItem.objects.get(pk=object_id) \
    #         .select_related('product_item_size_quantity') \
    #         .select_related('product_item_size_quantity__size') \
    #
    #     return obj