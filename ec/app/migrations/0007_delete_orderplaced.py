# Generated by Django 5.1.1 on 2024-12-10 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_payment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderPlaced',
        ),
    ]
