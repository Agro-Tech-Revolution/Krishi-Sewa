# Generated by Django 3.1.6 on 2021-07-08 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmers', '0015_auto_20210708_1542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homeexpenses',
            old_name='amount',
            new_name='quantity',
        ),
    ]
