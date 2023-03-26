from ..models import *
from ..utils.tests.tests_mixins import TestMixin


class TestReviews(TestMixin):

    def setUp(self) -> None:
        self.url = 'reviews-list'
        self.data = {'rating_value': 1, 'comment': 'bad'}
        self.user, self.user_data = self.create_user('tests@tests.com')
        self.user2, self.user_data2 = self.create_user('tests2@tests.com')
        self.create_products()
        self.create_address()
        self.create_shipping_method()
        self.fill_shopping_cart(self.user, self.user_data)
        self.fill_shopping_cart(self.user2, self.user_data2, items=1)
        self.user_order_id, self.user_order_item_id = self.create_order(self.user_data)
        self.user2_order_id, self.user2_order_item_id = self.create_order(self.user_data2)

    def test_create_review1(self):
        # Try to create review by not authenticated user.
        # Must be restricted

        kwargs = {'order_id': self.user_order_id, 'order_item_id': self.user_order_item_id[0]}

        response = self.client.post(
            reverse(self.url, kwargs=kwargs),
            self.data,
            format='json',
        )
        self.assertEqual(response.status_code, 401, "Unauthenticated users can't create reviews")

    def test_create_review2(self):
        # Try to create review by user2 for user1.
        # Must be restricted

        reverse_kwargs = {'order_id': self.user_order_id, 'order_item_id': self.user_order_item_id[0]}

        response = self.get_response('POST', self.url, reverse_kwargs=reverse_kwargs, data=self.data, user_data=self.user_data2)
        self.assertEqual(response.status_code, 403, "User2 can't create reviews for user1's purchase")


    def test_create_review3(self):
        # Try to create review by user which order status isn't done.
        # Must be restricted

        reverse_kwargs = {'order_id': self.user_order_id, 'order_item_id': self.user_order_item_id[0]}

        response = self.get_response('POST', self.url, reverse_kwargs=reverse_kwargs, data=self.data)
        self.assertEqual(response.status_code, 403, "User can't create reviews while his order isn't done")

    def test_create_review4(self):
        # Try to create review by user who bought product and which order is done.
        # Must be successful

        reverse_kwargs = {'order_id': self.user_order_id, 'order_item_id': self.user_order_item_id[0]}
        order = Order.objects.get(pk=self.user_order_id)
        order.order_status = 4 # 4 is Done
        order.save()

        response = self.get_response('POST', self.url, reverse_kwargs=reverse_kwargs, data=self.data)
        self.assertEqual(response.status_code, 201, "User can't create reviews while his order isn't done")


    def test_create_review5(self):
        # Try to get review for unauthenticated user
        # Must be successful

        reverse_kwargs = {'order_id': self.user_order_id, 'order_item_id': self.user_order_item_id[0]}
        order = Order.objects.get(pk=self.user_order_id)
        order.order_status = 4 # 4 is Done
        order.save()

        self.get_response('POST', self.url, reverse_kwargs=reverse_kwargs, data=self.data) # review is created

        response = self.client.get(reverse('read_reviews-list', kwargs={'product_slug': self.p1.slug}))

        self.assertEqual(response.data['results'][0]['rating_value'], 1,
                         "'rating_value' must be equal to 1, see self.data in setUp")
        self.assertEqual(response.data['results'][0]['comment'], 'bad',
                         "'comment' must be equal to 'bad', see self.data in setUp")


    def test_update_review1(self):
        # Try to update review by user who isn't creator of this review.
        # Must be restricted

        reverse_kwargs = {'order_id': self.user_order_id, 'order_item_id': self.user_order_item_id[0]}
        data = {'rating_value': 5, 'comment': 'perfect'}
        order = Order.objects.get(pk=self.user_order_id)
        order.order_status = 4  # 4 is Done
        order.save()

        r = self.get_response('POST', self.url, reverse_kwargs=reverse_kwargs, data=self.data)  # review is created by user1
        reverse_kwargs['pk'] = r.data['id']

        response = self.get_response('PUT', 'reviews-detail', reverse_kwargs=reverse_kwargs, data=data, user_data=self.user_data2)
        self.assertEqual(response.status_code, 403, "User can't update reviews which he didn't create")

    def test_update_review2(self):
        # Try to update review by user who is creator of this review.
        # Must be successful

        reverse_kwargs = {'order_id': self.user_order_id, 'order_item_id': self.user_order_item_id[0]}
        data = {'rating_value': 5, 'comment': 'perfect'}
        order = Order.objects.get(pk=self.user_order_id)
        order.order_status = 4  # 4 is Done
        order.save()

        r = self.get_response('POST', self.url, reverse_kwargs=reverse_kwargs, data=self.data)  # review is created by user1
        reverse_kwargs['pk'] = r.data['id']

        response = self.get_response('PUT', 'reviews-detail', reverse_kwargs=reverse_kwargs, data=data)
        self.assertEqual(response.status_code, 200, "User must have ability to update reviews his reviews")
        self.assertEqual(response.data['rating_value'], 5, "'rating_value' must be equal to 5")
        self.assertEqual(response.data['comment'], 'perfect', "'comment' must be 'perfect'")
