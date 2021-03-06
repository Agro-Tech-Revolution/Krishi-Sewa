# Generated by Django 3.1.6 on 2021-07-08 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmers', '0012_auto_20210707_2039'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeExpenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Consumed', 'Consumed'), ('Wastes', 'Wastes')], default='Consumed', max_length=50)),
                ('amount', models.FloatField()),
                ('estimated_price', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
