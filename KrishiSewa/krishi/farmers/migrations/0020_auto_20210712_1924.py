# Generated by Django 3.1.6 on 2021-07-12 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmers', '0019_expenses'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsold',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='products',
            name='prod_name',
            field=models.CharField(max_length=100),
        ),
    ]