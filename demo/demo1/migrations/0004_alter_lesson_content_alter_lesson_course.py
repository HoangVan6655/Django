# Generated by Django 4.0.5 on 2022-06-11 14:02

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demo1', '0003_tag_lesson_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='courses',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='demo1.courses'),
        ),
    ]
