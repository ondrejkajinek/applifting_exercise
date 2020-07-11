# Generated by Django 3.0.8 on 2020-07-08 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='price',
            options={'ordering': ['-timestamp_from']},
        ),
        migrations.AddField(
            model_name='offer',
            name='external_id',
            field=models.IntegerField(default=None, unique=True, verbose_name='Offer microservice ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='price',
            name='timestamp_to',
            field=models.PositiveIntegerField(null=True, verbose_name='Timestamp to, exclusive'),
        ),
    ]