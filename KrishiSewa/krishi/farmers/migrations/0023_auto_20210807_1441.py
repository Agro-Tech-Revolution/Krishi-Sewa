# Generated by Django 3.1.6 on 2021-08-07 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmers', '0022_remove_productsold_sold_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='prod_img',
            field=models.CharField(default='static/product_images/no_image.png', max_length=1200, null=True),
        ),
    ]