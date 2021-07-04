# Generated by Django 3.1.6 on 2021-07-03 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vendors', '0003_auto_20210701_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='eqp_img',
            field=models.ImageField(null=True, upload_to='static/equipment_images'),
        ),
        migrations.CreateModel(
            name='EquipmentReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_category', models.CharField(choices=[('False Information', 'False Information'), ('Fake Products', 'Fake Products'), ('Misinformation', 'Misinformation'), ('Something Else', 'Something Else')], default='Misinformation', max_length=50)),
                ('report_description', models.CharField(max_length=200)),
                ('reported_date', models.DateTimeField(auto_now_add=True)),
                ('reported_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reported_equipment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendors.equipment')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200)),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('comment_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('equipment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendors.equipment')),
            ],
        ),
        migrations.AddField(
            model_name='equipment',
            name='comments',
            field=models.ManyToManyField(related_name='eqp_comments', through='vendors.EquipmentComment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='equipment',
            name='reports',
            field=models.ManyToManyField(related_name='eqp_reports', through='vendors.EquipmentReport', to=settings.AUTH_USER_MODEL),
        ),
    ]
