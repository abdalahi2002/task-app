# Generated by Django 5.0.7 on 2024-08-09 12:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_delete_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projet',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
