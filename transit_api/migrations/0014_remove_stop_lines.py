# Generated by Django 4.1.1 on 2022-10-23 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transit_api', '0013_train_last_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stop',
            name='lines',
        ),
    ]
