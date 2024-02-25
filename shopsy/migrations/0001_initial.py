# Generated by Django 4.2.5 on 2023-10-09 05:44

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="signup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=100, null=True)),
                ("last_name", models.CharField(blank=True, max_length=100, null=True)),
                ("email", models.CharField(blank=True, max_length=100, null=True)),
                ("password", models.CharField(blank=True, max_length=255, null=True)),
                ("gender", models.CharField(blank=True, max_length=100, null=True)),
                ("Mobile", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]