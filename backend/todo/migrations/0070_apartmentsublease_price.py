# Generated by Django 4.0.3 on 2022-04-22 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0069_apartmentreview_delete_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartmentsublease',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
