# Generated by Django 4.0.1 on 2022-01-28 07:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facedectapi', '0002_alter_log_logtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='logtime',
            field=models.DateTimeField(primary_key=True, serialize=False, verbose_name=datetime.datetime(2022, 1, 28, 13, 6, 55, 288900)),
        ),
    ]
