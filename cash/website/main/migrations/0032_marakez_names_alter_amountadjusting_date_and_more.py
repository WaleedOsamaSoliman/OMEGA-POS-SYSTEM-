# Generated by Django 5.0.3 on 2024-05-02 18:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_marakez_receits_alter_marakez_products_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='marakez_names',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(max_length=50, verbose_name='Products')),
            ],
            options={
                'verbose_name_plural': 'Marakez Names',
            },
        ),
        migrations.AlterField(
            model_name='amountadjusting',
            name='Date',
            field=models.DateField(default=datetime.datetime(2024, 5, 2, 21, 44, 31, 364402), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='amountadjusting',
            name='time',
            field=models.TimeField(default='21:44:31', verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='deletedreceits',
            name='Date',
            field=models.DateField(default=datetime.datetime(2024, 5, 2, 21, 44, 31, 364402), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='deletedreceits',
            name='time',
            field=models.TimeField(default='21:44:31', verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='finishinghistory',
            name='Date',
            field=models.DateField(default=datetime.datetime(2024, 5, 2, 21, 44, 31, 364402), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='finishinghistory',
            name='time',
            field=models.TimeField(default='21:44:31', verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='gavedmoney',
            name='Date',
            field=models.DateField(default=datetime.datetime(2024, 5, 2, 21, 44, 31, 364402), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='gavedmoney',
            name='time',
            field=models.TimeField(default='21:44:31', verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='gotover',
            name='Date',
            field=models.DateField(default=datetime.datetime(2024, 5, 2, 21, 44, 31, 364402), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='gotover',
            name='time',
            field=models.TimeField(default='21:44:31', verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='inoutemployeehistory',
            name='Date',
            field=models.DateField(default=datetime.datetime(2024, 5, 2, 21, 44, 31, 364402), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='inoutemployeehistory',
            name='time',
            field=models.TimeField(default='21:44:31', verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='marakez_receits',
            name='Date',
            field=models.DateField(default=datetime.datetime(2024, 5, 2, 21, 44, 31, 364402), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='marakez_receits',
            name='time',
            field=models.TimeField(default='21:44:31', verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='receits',
            name='Date',
            field=models.DateField(default=datetime.datetime(2024, 5, 2, 21, 44, 31, 364402), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='receits',
            name='time',
            field=models.TimeField(default='21:44:31', verbose_name='Time'),
        ),
    ]
