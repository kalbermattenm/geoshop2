# Generated by Django 3.0.5 on 2020-04-09 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('api', '0005_auto_20200407_1706'), ('api', '0006_auto_20200407_1709'), ('api', '0007_auto_20200409_1733')]

    dependencies = [
        ('api', '0003_auto_20200407_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identity',
            name='postcode',
            field=models.CharField(blank=True, default=0, max_length=10, verbose_name='postcode'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='identity',
            name='company_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='company_name'),
        ),
        migrations.AlterField(
            model_name='identity',
            name='contract_accepted',
            field=models.DateField(null=True, verbose_name='contract_accepted'),
        ),
        migrations.AlterField(
            model_name='identity',
            name='sap_id',
            field=models.BigIntegerField(null=True, verbose_name='sap_id'),
        ),
    ]
