# Generated by Django 4.1.6 on 2023-02-02 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_alter_product_created_alter_productitem_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productitem',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ecommerce.discount'),
        ),
    ]
