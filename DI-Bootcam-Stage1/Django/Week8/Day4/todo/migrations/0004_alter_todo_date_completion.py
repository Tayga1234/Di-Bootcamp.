# Generated by Django 4.1.5 on 2023-01-10 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_alter_todo_date_completion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='date_completion',
            field=models.DateTimeField(null=True),
        ),
    ]
