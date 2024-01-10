# Generated by Django 4.2.9 on 2024-01-10 08:47

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('klachtsysteem', '0002_alter_invitation_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waarde', models.CharField(max_length=255)),
                ('beschrijving', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Klacht',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=50)),
                ('omschrijving', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('GPS_locatie', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('datum_melding', models.DateTimeField()),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='klachtsysteem.status')),
            ],
        ),
        migrations.CreateModel(
            name='Afbeelding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to='afbeeldingen/')),
                ('klacht', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='afbeeldingen', to='klachtsysteem.klacht')),
            ],
        ),
    ]
