# Generated by Django 5.1.3 on 2024-11-21 14:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0025_dayoffrequest"),
    ]

    operations = [
        migrations.AddField(
            model_name="dayoffrequest",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="uploads/"),
        ),
    ]