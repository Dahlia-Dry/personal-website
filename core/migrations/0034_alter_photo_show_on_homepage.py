# Generated by Django 4.2.6 on 2024-03-04 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_album_show_on_homepage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='show_on_homepage',
            field=models.BooleanField(default=False),
        ),
    ]
