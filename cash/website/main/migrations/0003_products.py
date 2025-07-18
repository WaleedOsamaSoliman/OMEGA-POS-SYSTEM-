# Generated by Django 5.0.3 on 2024-04-03 07:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_alter_accounts_options_accounts_state"),
    ]

    operations = [
        migrations.CreateModel(
            name="Products",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Product Name")),
                ("price", models.IntegerField(verbose_name="Price")),
                ("amount", models.IntegerField(verbose_name="Price")),
                (
                    "type",
                    models.CharField(
                        choices=[("manfz", "1"), ("foram", "2")],
                        default="manfz",
                        max_length=9,
                    ),
                ),
            ],
        ),
    ]
