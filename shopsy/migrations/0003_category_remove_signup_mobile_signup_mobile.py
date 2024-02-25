# Generated by Django 4.2.5 on 2023-10-09 13:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shopsy", "0002_remove_signup_gender"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("cat_image", models.ImageField(upload_to="uploads/category/")),
                ("cat_name", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="signup",
            name="Mobile",
        ),
        migrations.AddField(
            model_name="signup",
            name="mobile",
            field=models.BigIntegerField(blank=True, max_length=100, null=True),
        ),
    ]