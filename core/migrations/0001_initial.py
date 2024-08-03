# Generated by Django 5.0.7 on 2024-07-29 11:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('sync_location', models.BooleanField(default=True)),
                ('show_on_homepage', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('caption', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='temp/')),
                ('created_on', models.DateField()),
                ('filename', models.CharField(blank=True, max_length=200, null=True)),
                ('show_on_homepage', models.BooleanField(default=False)),
                ('link', models.CharField(blank=True, default='https://www.dahlia.is/here', max_length=200, null=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.album')),
            ],
            options={
                'ordering': ['album', '-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('name_short', models.CharField(blank=True, max_length=200, null=True)),
                ('link', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='AstroPhoto',
            fields=[
                ('photo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.photo')),
                ('catalog_name', models.TextField(blank=True)),
                ('info_link', models.TextField(blank=True)),
                ('inst_caption', models.TextField(blank=True, default='', null=True)),
            ],
            bases=('core.photo',),
        ),
        migrations.AddField(
            model_name='photo',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.location'),
        ),
        migrations.AddField(
            model_name='album',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.location'),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('content', models.FilePathField(path='content/', recursive=True)),
                ('post_type', models.CharField(max_length=200)),
                ('created_on', models.DateField()),
                ('current', models.BooleanField(default=False)),
                ('html', models.FilePathField(default='core/templates/building_blocks/post-detail.html', max_length=200, path='core/templates/', recursive=True)),
                ('cover_photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.photo')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.location')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]