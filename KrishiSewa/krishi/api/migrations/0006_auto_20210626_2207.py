# Generated by Django 3.1.6 on 2021-06-26 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210626_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='category',
            field=models.CharField(choices=[('Tractor', 'Tractor'), ('Harvester', 'Harvester'), ('ATV or UTV', 'ATV or UTV'), ('Plows', 'Plows'), ('Harrows', 'Harrows'), ('Fertilizer Spreaders', 'Fertilizer Spreaders'), ('Seeders', 'Seeders'), ('Balers', 'Balers'), ('Other', 'Other')], default='Tractor', max_length=25),
        ),
    ]
