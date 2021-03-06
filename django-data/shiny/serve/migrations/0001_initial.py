# Generated by Django 2.2.11 on 2020-03-24 15:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShinyApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, default='')),
                ('users', models.ManyToManyField(related_name='shinyapps', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
