# Generated by Django 3.0.8 on 2020-07-12 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20200711_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Price'),
        ),
    ]