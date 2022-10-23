# Generated by Django 4.1.1 on 2022-10-09 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transit_api', '0002_alter_train_stop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('bearing', models.FloatField()),
            ],
        ),
    ]
