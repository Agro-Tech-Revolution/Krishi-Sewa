# Generated by Django 3.1.6 on 2021-07-01 15:38

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
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('modal', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('Tractor', 'Tractor'), ('Harvester', 'Harvester'), ('ATV or UTV', 'ATV or UTV'), ('Plows', 'Plows'), ('Harrows', 'Harrows'), ('Fertilizer Spreaders', 'Fertilizer Spreaders'), ('Seeders', 'Seeders'), ('Balers', 'Balers'), ('Other', 'Other')], default='Tractor', max_length=25)),
                ('available_For_Rent', models.BooleanField(default=True, null=True)),
                ('available_To_Buy', models.BooleanField(default=True, null=True)),
                ('price_To_Buy', models.FloatField(null=True)),
                ('price_To_Rent', models.FloatField(null=True)),
                ('details', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]