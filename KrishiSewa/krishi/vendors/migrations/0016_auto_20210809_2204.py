# Generated by Django 3.1.6 on 2021-08-09 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0015_equipmenttodisplay_to_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='buydetails',
            name='seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rentdetails',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]
