# Generated by Django 4.0.3 on 2022-04-17 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0059_remove_review_review_text_review_review_text_val'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='review_text_val',
            new_name='review_text',
        ),
    ]
