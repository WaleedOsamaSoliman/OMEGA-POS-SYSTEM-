# Generated by Django 5.0.3 on 2024-04-03 11:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0008_accounts_nickname_alter_accounts_username_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Shift_Finishing",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                ("totalMoney", models.FloatField(verbose_name="Total Money")),
                ("user", models.CharField(max_length=50, verbose_name="User")),
                ("ReceitsCount", models.IntegerField(verbose_name="No of Receits ")),
            ],
            options={
                "verbose_name_plural": "Shift Finishing",
            },
        ),
        migrations.AlterField(
            model_name="receits",
            name="time",
            field=models.TimeField(default="13:19:38", verbose_name="Time"),
        ),
    ]
