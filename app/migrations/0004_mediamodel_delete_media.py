# Generated by Django 4.2.6 on 2023-10-09 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_category_note_category_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaModel',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.basemodel')),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('image', 'image'), ('voice', 'voice'), ('video', 'video')], default='image', max_length=20)),
                ('media', models.ImageField(upload_to='media/')),
                ('size', models.CharField(blank=True, max_length=20)),
                ('note', models.ManyToManyField(to='app.notemodel')),
            ],
            bases=('app.basemodel',),
        ),
        migrations.DeleteModel(
            name='Media',
        ),
    ]