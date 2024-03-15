# Generated by Django 2.2.28 on 2024-03-15 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CheeseBoardSite', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='id',
        ),
        migrations.RemoveField(
            model_name='stats',
            name='id',
        ),
        migrations.AddField(
            model_name='comment',
            name='ID',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='stats',
            name='ID',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='dateOfBirth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='ID',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
