# Generated by Django 4.1.4 on 2023-11-09 21:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_category_name_alter_task_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 8, 21, 14, 45, 806512, tzinfo=datetime.timezone.utc)),
        ),
    ]
