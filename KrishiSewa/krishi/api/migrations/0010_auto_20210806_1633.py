# Generated by Django 3.1.6 on 2021-08-06 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20210806_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(max_length=50),
        ),
    ]