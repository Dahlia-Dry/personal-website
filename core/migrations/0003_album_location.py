# Generated by Django 4.2.6 on 2023-10-10 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='location',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='core.location'),
            preserve_default=False,
        ),
    ]
