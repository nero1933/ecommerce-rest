# Generated by Django 4.1.6 on 2023-02-01 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_alter_productitem_price_alter_promotion_description_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Promotion',
            new_name='Discount',
        ),
        migrations.RenameField(
            model_name='productitem',
            old_name='promotion',
            new_name='discount',
        ),
    ]
