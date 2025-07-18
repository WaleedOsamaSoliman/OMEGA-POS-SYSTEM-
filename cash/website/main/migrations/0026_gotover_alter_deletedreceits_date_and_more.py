# Generated by Django 5.0.3 on 2024-04-22 18:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_tarabeza_users_alter_deletedreceits_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='gotOver',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(default='default', max_length=45, verbose_name='Tarbeza User')),
                ('over', models.FloatField(default=0, verbose_name='Over Money')),
                ('Date', models.DateField(default=datetime.date(2024, 4, 22), verbose_name='Date')),
                ('time', models.TimeField(default='20:40:06', verbose_name='Time')),
            ],
            options={
                'verbose_name_plural': 'Over Hitsory',
            },
        ),
        migrations.AlterField(
            model_name='deletedreceits',
            name='Date',
            field=models.DateField(default=datetime.date(2024, 4, 22), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='deletedreceits',
            name='time',
            field=models.TimeField(default='20:40:06', verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='finishinghistory',
            name='Date',
            field=models.DateField(default=datetime.date(2024, 4, 22), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='finishinghistory',
            name='time',
            field=models.TimeField(default='20:40:06', verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='gavedmoney',
            name='Date',
            field=models.DateField(default=datetime.date(2024, 4, 22), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='gavedmoney',
            name='time',
            field=models.TimeField(default='20:40:06', verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='inoutemployeehistory',
            name='Date',
            field=models.DateField(default=datetime.date(2024, 4, 22), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='inoutemployeehistory',
            name='time',
            field=models.TimeField(default='20:40:06', verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='receits',
            name='Date',
            field=models.DateField(default=datetime.date(2024, 4, 22), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='receits',
            name='time',
            field=models.TimeField(default='20:40:06', verbose_name='Time'),
        ),
    ]
