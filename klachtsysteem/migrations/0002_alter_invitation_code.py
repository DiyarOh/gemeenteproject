# Generated by Django 4.2.8 on 2023-12-07 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('klachtsysteem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
