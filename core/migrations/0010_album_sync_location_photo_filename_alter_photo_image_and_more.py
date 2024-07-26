# Generated by Django 4.2.6 on 2023-10-12 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_album_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='sync_location',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='filename',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='temp/'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.location'),
        ),
    ]
