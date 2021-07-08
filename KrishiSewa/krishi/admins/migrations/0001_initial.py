# Generated by Django 3.1.6 on 2021-07-04 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_name', models.CharField(max_length=100)),
                ('prod_category', models.CharField(choices=[('Cereals', 'Cereals'), ('Pulses', 'Pulses'), ('Vegetables', 'Vegetables'), ('Fruits', 'Fruits'), ('Nuts', 'Nuts'), ('Oilseeds', 'Oilseeds'), ('Sugars and Starches', 'Sugars and Starches'), ('Fibres', 'Fibres'), ('Beverages', 'Beverages'), ('Narcotics', 'Narcotics'), ('Spices', 'Spices'), ('Condiments', 'Condiments'), ('Others', 'Others')], default='Cereals', max_length=25)),
                ('prod_img', models.ImageField(null=True, upload_to='static/product_images')),
            ],
        ),
    ]
