# Generated by Django 4.0.3 on 2022-04-17 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0061_alter_review_review_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='review_text',
        ),
    ]
