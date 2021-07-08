# Generated by Django 3.1.6 on 2021-07-07 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vendors', '0005_auto_20210703_1925'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('total_price', models.FloatField()),
                ('sold_date', models.DateTimeField(auto_now_add=True)),
                ('remarks', models.CharField(max_length=150, null=True)),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentToDisplay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modal', models.CharField(max_length=75)),
                ('available_for_rent', models.BooleanField(default=True, null=True)),
                ('available_to_buy', models.BooleanField(default=True, null=True)),
                ('price_to_buy_per_item', models.FloatField(null=True)),
                ('price_per_hour', models.FloatField(null=True)),
                ('Duration', models.FloatField(null=True)),
                ('details', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('eqp_img', models.ImageField(null=True, upload_to='static/equipment_images')),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RentDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rented_quantity', models.FloatField()),
                ('rented_duration', models.FloatField()),
                ('total_price', models.FloatField()),
                ('rented_date', models.DateTimeField(auto_now_add=True)),
                ('remarks', models.CharField(max_length=150, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('equipment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendors.equipmenttodisplay')),
                ('rented_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rented_by', to=settings.AUTH_USER_MODEL)),
                ('rented_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rented_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='added_by',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='available_for_rent',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='available_to_buy',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='date',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='details',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='eqp_img',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='modal',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='price_to_buy',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='price_to_rent',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='reports',
        ),
        migrations.AlterField(
            model_name='equipment',
            name='name',
            field=models.CharField(max_length=70, unique=True),
        ),
        migrations.DeleteModel(
            name='EquipmentComment',
        ),
        migrations.AddField(
            model_name='equipmenttodisplay',
            name='equipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendors.equipment'),
        ),
        migrations.AddField(
            model_name='equipmenttodisplay',
            name='reports',
            field=models.ManyToManyField(related_name='eqp_reports', through='vendors.EquipmentReport', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='buydetails',
            name='equipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendors.equipmenttodisplay'),
        ),
        migrations.AddField(
            model_name='buydetails',
            name='sold_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sold_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='buydetails',
            name='sold_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sold_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='equipmentreport',
            name='reported_equipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendors.equipmenttodisplay'),
        ),
    ]
