# Generated by Django 5.1.1 on 2024-12-22 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_orderplaced'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default='default@example.com', max_length=254),
        ),
    ]