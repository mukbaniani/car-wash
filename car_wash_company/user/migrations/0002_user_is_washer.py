# Generated by Django 3.2.4 on 2021-06-24 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_washer',
            field=models.BooleanField(default=False),
        ),
    ]
