# Generated by Django 5.0.3 on 2024-04-03 13:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0012_alter_employees_money_alter_employees_nickname_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="employees",
            name="Money",
        ),
        migrations.AddField(
            model_name="employees",
            name="MoneyMinus",
            field=models.FloatField(default=0, verbose_name="Money (-)"),
        ),
        migrations.AddField(
            model_name="employees",
            name="MoneyPlus",
            field=models.FloatField(default=0, verbose_name="Money (+)"),
        ),
        migrations.AlterField(
            model_name="receits",
            name="time",
            field=models.TimeField(default="15:34:48", verbose_name="Time"),
        ),
    ]
