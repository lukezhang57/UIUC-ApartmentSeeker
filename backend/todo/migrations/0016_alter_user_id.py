# Generated by Django 3.2 on 2022-03-01 16:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0015_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('7765486e-0416-4380-803d-e65463a6fa73'), editable=False, primary_key=True, serialize=False),
        ),
    ]
