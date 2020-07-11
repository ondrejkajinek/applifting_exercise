# Generated by Django 3.0.8 on 2020-07-08 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, unique=True, verbose_name='Key')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
            ],
        ),
    ]
