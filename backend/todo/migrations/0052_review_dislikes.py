# Generated by Django 4.0.3 on 2022-04-04 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0051_remove_user_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='dislikes', to='todo.user'),
        ),
    ]
