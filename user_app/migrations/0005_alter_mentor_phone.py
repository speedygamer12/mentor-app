# Generated by Django 3.2.13 on 2022-05-12 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0004_auto_20220512_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='phone',
            field=models.IntegerField(blank=True),
        ),
    ]
