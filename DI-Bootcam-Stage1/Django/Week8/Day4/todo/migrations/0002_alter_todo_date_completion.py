# Generated by Django 4.1.5 on 2023-01-10 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='date_completion',
            field=models.DateTimeField(default=None),
        ),
    ]