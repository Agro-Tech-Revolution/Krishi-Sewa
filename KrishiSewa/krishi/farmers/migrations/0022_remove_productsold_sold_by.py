# Generated by Django 3.1.6 on 2021-07-28 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmers', '0021_productsold_seen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productsold',
            name='sold_by',
        ),
    ]