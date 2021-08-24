# Generated by Django 3.1.6 on 2021-08-22 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20210814_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('Farmers', 'Farmers'), ('Vendors', 'Vendors'), ('Buyers', 'Buyers'), ('Admins', 'Admins')], max_length=50),
        ),
    ]