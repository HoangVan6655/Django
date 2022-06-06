# Generated by Django 4.0.5 on 2022-06-05 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo1', '0002_alter_course_options_course_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='demo1.tag'),
        ),
    ]