# Generated by Django 3.0.8 on 2020-07-21 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0003_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='error',
            options={'ordering': ['-timestamp']},
        ),
    ]