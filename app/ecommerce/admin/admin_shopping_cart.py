from django.contrib import admin
from ..models.models_shopping_cart import *


class ShoppingCartItemInline(admin.TabularInline):
    model = ShoppingCartItem
    fields = ['cart', 'product_item_size_quantity', 'quantity']
    readonly_fields = ('cart',)
    extra = 0


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    model = ShoppingCart
    inlines = [ShoppingCartItemInline]
    #readonly_fields = ('cart', )

    # def get_queryset(self, request):
    #     queryset = ShoppingCartItem.objects.all() \
    #         .select_related('product_item_size_quantity') \
    #         .select_related('product_item_size_quantity__size') \
    #
    #     return queryset

@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(admin.ModelAdmin):
    model = ShoppingCartItem
    readonly_fields = ('cart', )

    def get_queryset(self, request):
        queryset = ShoppingCartItem.objects.all() \
            .select_related('product_item_size_quantity') \
            .select_related('product_item_size_quantity__size') \

        return queryset
