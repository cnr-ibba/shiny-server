# Generated by Django 2.2.12 on 2020-04-10 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serve', '0002_shinyapp_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='shinyapp',
            name='thumbnail',
            field=models.ImageField(default='default.png', upload_to='thumbnails'),
        ),
    ]