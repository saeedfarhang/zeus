# Generated by Django 3.0 on 2022-08-26 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Province",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=True)),
                ("fa_name", models.CharField(max_length=225)),
                ("en_name", models.CharField(blank=True, max_length=225, null=True)),
                (
                    "latitude",
                    models.DecimalField(decimal_places=6, default=0, max_digits=8),
                ),
                (
                    "longitude",
                    models.DecimalField(decimal_places=6, default=0, max_digits=8),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=True)),
                ("fa_name", models.CharField(max_length=225)),
                ("en_name", models.CharField(blank=True, max_length=225, null=True)),
                (
                    "latitude",
                    models.DecimalField(decimal_places=6, default=0, max_digits=8),
                ),
                (
                    "longitude",
                    models.DecimalField(decimal_places=6, default=0, max_digits=8),
                ),
                (
                    "province",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cities",
                        to="location.Province",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=True)),
                ("title", models.CharField(max_length=180)),
                ("address", models.TextField(max_length=1000)),
                ("phone_number", models.CharField(max_length=11)),
                ("landline_number", models.CharField(max_length=11)),
                (
                    "latitude",
                    models.DecimalField(decimal_places=6, default=0, max_digits=8),
                ),
                (
                    "longitude",
                    models.DecimalField(decimal_places=6, default=0, max_digits=8),
                ),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="addresses",
                        to="location.City",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterUniqueTogether(
            name="city",
            unique_together={("fa_name", "en_name", "province")},
        ),
        migrations.AlterUniqueTogether(
            name="province",
            unique_together={("fa_name", "en_name")},
        ),
    ]
