# Generated by Django 4.0.4 on 2023-01-29 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0079_delete_distancematrix'),
    ]

    operations = [
        migrations.AddField(
            model_name='distancematrixmodel',
            name='transit_travel',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, null=True),
        ),
    ]