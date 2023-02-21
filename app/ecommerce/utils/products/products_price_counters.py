from ecommerce.models import ProductItem


class DiscountCalculator:
    """ Calculates discount price. """

    @staticmethod
    def get_discount_price(obj) -> str:
        """
        Takes 'price', and 'discount_rate' form object of 'ProductItem' model
        and calculates 'discount_price'. Returns it as a string.
        """

        if not isinstance(obj, ProductItem):
            raise ValueError('obj must be "ProductItem" class')

        if not obj.discount:
            return str(obj.price)

        price = obj.price
        discount_rate = obj.discount.discount_rate
        discount_price = price - (price * discount_rate / 100)
        return str(discount_price)
