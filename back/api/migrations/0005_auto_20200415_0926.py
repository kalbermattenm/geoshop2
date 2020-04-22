# Generated by Django 3.0.5 on 2020-04-15 07:26

import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200407_1615'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=django.contrib.postgres.indexes.GinIndex(fields=['ts'], name='product_ts_96c462_gin'),
        ),
    ]
