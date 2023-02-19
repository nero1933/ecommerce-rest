# Generated by Django 4.1.7 on 2023-02-18 13:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('discount_rate', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99.9)])),
                ('is_active', models.BooleanField(default=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('product_image', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('M', 'Men'), ('W', 'Women')], max_length=15)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='ecommerce.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SKU', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.1)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_color', to='ecommerce.color')),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ecommerce.discount')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_item', to='ecommerce.products')),
                ('product_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image', to='ecommerce.image')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Clothes', (('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', '2Extra Large'))), ('Shoes', (('34.5', 'EU 34.5'), ('35', 'EU 35'), ('35.5', 'EU 35.5'), ('36', 'EU 36'), ('36.5', 'EU 36.5'), ('37', 'EU 37'), ('37.5', 'EU 37.5'), ('38', 'EU 38'), ('38.5', 'EU 38.5'), ('39', 'EU 39'), ('39.5', 'EU 39.5'), ('40', 'EU 40'), ('40.5', 'EU 40.5'), ('41', 'EU 41'), ('41.5', 'EU 41.5'), ('42', 'EU 42'), ('42.5', 'EU 42.5'), ('43', 'EU 43'), ('43.5', 'EU 43.5'), ('44', 'EU 44'), ('44.5', 'EU 44.5'), ('45', 'EU 45'), ('45.5', 'EU 45.5'), ('46', 'EU 46'), ('46.5', 'EU 46.5'), ('47', 'EU 47'), ('47.5', 'EU 47.5'), ('48', 'EU 48'), ('48.5', 'EU 48.5'), ('49', 'EU 49'), ('49.5', 'EU 49.5'), ('50', 'EU 50'))), ('unknown', 'Unknown')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductItemSizeQuantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('productitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.productitem')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.size')),
            ],
        ),
        migrations.AddField(
            model_name='productitem',
            name='sizes',
            field=models.ManyToManyField(related_name='product_size', through='ecommerce.ProductItemSizeQuantity', to='ecommerce.size'),
        ),
        migrations.AddField(
            model_name='products',
            name='style',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.style'),
        ),
        migrations.AddField(
            model_name='image',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.productitem'),
        ),
    ]
