# Generated by Django 4.2.6 on 2023-10-09 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_notemodel_show'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='note',
        ),
        migrations.AddField(
            model_name='category',
            name='note',
            field=models.ManyToManyField(to='app.notemodel'),
        ),
    ]
