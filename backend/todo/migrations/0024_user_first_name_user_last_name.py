# Generated by Django 4.0.3 on 2022-03-06 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0023_address_lat_address_long_review_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
