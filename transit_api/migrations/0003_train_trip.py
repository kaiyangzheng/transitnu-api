# Generated by Django 4.1.1 on 2022-11-12 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transit_api', '0002_train_direction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='train',
            name='trip',
            field=models.CharField(max_length=255, null=True),
        ),
    ]