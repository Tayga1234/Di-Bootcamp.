# Generated by Django 4.1.4 on 2022-12-27 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_animal_nom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='famille',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='info.famille'),
        ),
    ]
