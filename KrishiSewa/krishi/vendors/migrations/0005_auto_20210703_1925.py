# Generated by Django 3.1.6 on 2021-07-03 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0004_auto_20210703_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentreport',
            name='report_category',
            field=models.CharField(choices=[('False Information', 'False Information'), ('Fake Equipments', 'Fake Equipments'), ('Misinformation', 'Misinformation'), ('Something Else', 'Something Else')], default='Misinformation', max_length=50),
        ),
    ]
