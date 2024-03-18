# Generated by Django 2.2.28 on 2024-03-18 13:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('CheeseBoardSite', '0016_auto_20240318_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='accountCreationDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 18, 13, 30, 23, 898919, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='account',
            name='dateLastLoggedIn',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 18, 13, 30, 23, 898919, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='account',
            name='dateOfBirth',
            field=models.DateField(default=datetime.datetime(2024, 3, 18, 13, 30, 23, 898920)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='timeDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 18, 13, 30, 23, 898919, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='timeDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 18, 13, 30, 23, 898919, tzinfo=utc)),
        ),
    ]
