# Generated by Django 4.0.3 on 2022-04-28 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0072_apartment_overall_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='review_count',
            field=models.IntegerField(default=0),
        ),
    ]
