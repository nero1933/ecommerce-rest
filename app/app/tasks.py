from datetime import timedelta

from django.utils import timezone

from celery import shared_task


@shared_task(name='tasks.del_guests')
def delete_guests():
    from ecommerce.models.models_users import UserProfile
    try:
        users_ids = UserProfile.objects.filter(
           last_login__lt=timezone.localtime(timezone.now()) - timedelta(days=1),
           is_guest=True
        )
        users_ids.delete()
    except UserProfile.DoesNotExist:
        return 0
