# Generated by Django 3.1.6 on 2021-06-26 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_name', models.CharField(max_length=100)),
                ('quantity_in_kg', models.FloatField()),
                ('prod_category', models.CharField(choices=[('Cereals', 'Cereals'), ('Pulses', 'Pulses'), ('Vegetables', 'Vegetables'), ('Fruits', 'Fruits'), ('Nuts', 'Nuts'), ('Oilseeds', 'Oilseeds'), ('Sugars and Starches', 'Sugars and Starches'), ('Fibres', 'Fibres'), ('Beverages', 'Beverages'), ('Narcotics', 'Narcotics'), ('Spices', 'Spices'), ('Condiments', 'Condiments'), ('Others', 'Others')], default='Cereals', max_length=25)),
                ('prod_price', models.FloatField()),
                ('prod_added_on', models.DateTimeField(auto_now_add=True)),
                ('prod_added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('posted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]