from ..models import *
from ..utils.tests.tests_mixins import TestMixin


class TestReviews(TestMixin):

    def setUp(self) -> None:
        self.user, self.user_data = self.create_user('tests@tests.com')
        self.user2, self.user_data2 = self.create_user('tests2@tests.com')
        self.create_products()
        self.create_address()
        self.create_shipping_method()
        self.fill_shopping_cart(self.user, self.user_data)
        self.fill_shopping_cart(self.user2, self.user_data2, items=1)
        self.create_order(self.user_data)
        self.create_order(self.user_data2)

    def test(self):
        print('hi')
#        reverse_kwargs = {'order_id': 1, 'order_item_id': 1}
#        r = self.get_response('GET', 'reviews', reverse_kwargs=reverse_kwargs)



    def create_review1(self):
        # Try to create review by not authenticated user.
        # Must be restricted
        pass

    def create_review2(self):
        # Try to create review by user who didn't buy product.
        # Must be restricted
        pass

    def create_review3(self):
        # Try to create review by user which order status isn't done.
        # Must be restricted
        pass

    def create_review4(self):
        # Try to create review by user who bought product and which order is done.
        # Must be successful
        pass

    def update_review1(self):
        # Try to update review by user who isn't creator of this review.
        # Must be restricted
        pass

    def update_review2(self):
        # Try to update review by user who is creator of this review.
        # Must be successful
        pass
