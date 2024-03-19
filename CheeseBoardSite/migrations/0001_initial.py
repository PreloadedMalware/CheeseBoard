# Generated by Django 2.2.28 on 2024-03-19 18:51

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Cheese',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(default='slug', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('ID', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=64)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('caption', models.CharField(default='', max_length=265)),
                ('body', models.CharField(default='', max_length=4096)),
                ('likes', models.IntegerField(default=0)),
                ('timeDate', models.DateTimeField(default=datetime.datetime(2024, 3, 19, 18, 51, 56, 75337, tzinfo=utc))),
                ('slug', models.SlugField(unique=True)),
                ('cheeses', models.ManyToManyField(blank=True, null=True, to='CheeseBoardSite.Cheese')),
            ],
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('ID', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('timeOnCheeseBoard', models.IntegerField(default=0)),
                ('posts', models.IntegerField(default=0)),
                ('likesTaken', models.IntegerField(default=0)),
                ('likesGiven', models.IntegerField(default=0)),
                ('commentsTaken', models.IntegerField(default=0)),
                ('commentsGiven', models.IntegerField(default=0)),
                ('cheesesReferenced', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('dateOfBirth', models.DateField(default=datetime.datetime(2024, 3, 19, 18, 51, 56, 73838))),
                ('accountCreationDate', models.DateTimeField(default=datetime.datetime(2024, 3, 19, 18, 51, 56, 73838, tzinfo=utc))),
                ('dateLastLoggedIn', models.DateTimeField(default=datetime.datetime(2024, 3, 19, 18, 51, 56, 73838, tzinfo=utc))),
                ('profilePic', models.ImageField(blank=True, upload_to='profile_images')),
                ('cheese_points', models.IntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
                ('stats', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='CheeseBoardSite.Stats')),
                ('badges', models.ManyToManyField(blank=True, null=True, to='CheeseBoardSite.Badge')),
                ('faveCheese', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='CheeseBoardSite.Cheese')),
                ('followers', models.ManyToManyField(blank=True, null=True, related_name='_account_followers_+', to='CheeseBoardSite.Account')),
                ('following', models.ManyToManyField(blank=True, null=True, related_name='_account_following_+', to='CheeseBoardSite.Account')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Saved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('posts', models.ManyToManyField(blank=True, null=True, to='CheeseBoardSite.Post')),
                ('account', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='CheeseBoardSite.Account')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='account',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='CheeseBoardSite.Account'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('ID', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('likes', models.IntegerField(default=0)),
                ('body', models.CharField(max_length=64)),
                ('timeDate', models.DateTimeField(default=datetime.datetime(2024, 3, 19, 18, 51, 56, 76837, tzinfo=utc))),
                ('post', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='CheeseBoardSite.Post')),
                ('account', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='CheeseBoardSite.Account')),
            ],
        ),
    ]
