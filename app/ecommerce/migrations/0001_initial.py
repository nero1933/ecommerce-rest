# Generated by Django 4.1.6 on 2023-02-01 13:43

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
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('product_image', models.CharField(max_length=255)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.category')),
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
            name='ProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('SKU', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('product_image', models.CharField(max_length=255)),
                ('size', models.CharField(choices=[('Clothes', (('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', '2Extra Large'))), ('Shoes', (('34.5', 'EU 34.5'), ('35', 'EU 35'), ('35.5', 'EU 35.5'), ('36', 'EU 36'), ('36.5', 'EU 36.5'), ('37', 'EU 37'), ('37.5', 'EU 37.5'), ('38', 'EU 38'), ('38.5', 'EU 38.5'), ('39', 'EU 39'), ('39.5', 'EU 39.5'), ('40', 'EU 40'), ('40.5', 'EU 40.5'), ('41', 'EU 41'), ('41.5', 'EU 41.5'), ('42', 'EU 42'), ('42.5', 'EU 42.5'), ('43', 'EU 43'), ('43.5', 'EU 43.5'), ('44', 'EU 44'), ('44.5', 'EU 44.5'), ('45', 'EU 45'), ('45.5', 'EU 45.5'), ('46', 'EU 46'), ('46.5', 'EU 46.5'), ('47', 'EU 47'), ('47.5', 'EU 47.5'), ('48', 'EU 48'), ('48.5', 'EU 48.5'), ('49', 'EU 49'), ('49.5', 'EU 49.5'), ('50', 'EU 50'))), ('unknown', 'Unknown')], max_length=15)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='style',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.style'),
        ),
    ]
