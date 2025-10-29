# 0009_update_showcase_apps.py
from django.db import migrations


hello_shiny_description = """
A simple "Hello World" Shiny application from https://github.com/rstudio/shiny-examples

This is an example of *public* Shiny application that demonstrates
the capabilities of the Django-Shiny integration. This application should
be visible to all users. No special setup is required to run this app.
"""


wordcloud_description = """
A Shiny application that generates word clouds from text input

This is an example of *private* Shiny application used to demonstrate
the capabilities of the Django-Shiny integration. This application should
be visible only to admin and authorized users.

## Setting up

Use docker compose to start the proper R environment:

```bash
docker-compose run --rm -ti shiny-4.5 bash
```

After that, navigate to the application directory and start an R session:

```bash
cd /srv/shiny-server/082-word-cloud
R
```

Inside R, install the required packages using renv:

```R
renv::restore()
```

Close R and terminate the docker container. Your application is now ready
to be used
"""


def update_helloshiny_app(apps, schema_editor):
    """Update HelloShiny application description"""
    ShinyApp = apps.get_model('serve', 'ShinyApp')

    app = ShinyApp.objects.get(slug='hello-shiny')
    app.description = hello_shiny_description
    app.thumbnail = 'thumbnails/001-hello-shiny.png'
    app.save()


def revert_helloshiny_app(apps, schema_editor):
    """Revert HelloShiny to old description"""
    ShinyApp = apps.get_model('serve', 'ShinyApp')

    app = ShinyApp.objects.get(slug='hello-shiny')
    app.description = 'A simple "Hello World" Shiny application from https://github.com/rstudio/shiny-examples'
    app.thumbnail = 'default.png'
    app.save()


def update_wordcloud_app(apps, schema_editor):
    """Update WordCloud application description"""
    ShinyApp = apps.get_model('serve', 'ShinyApp')

    app = ShinyApp.objects.get(slug='wordcloud')
    app.description = wordcloud_description
    app.thumbnail = 'thumbnails/082-word-cloud.png'
    app.save()


def revert_wordcloud_app(apps, schema_editor):
    """Revert to old description"""
    ShinyApp = apps.get_model('serve', 'ShinyApp')

    app = ShinyApp.objects.get(slug='wordcloud')
    app.description = 'A Shiny application that generates word clouds from text input'
    app.thumbnail = 'default.png'
    app.save()


class Migration(migrations.Migration):
    dependencies = [
        ('serve', '0007_add_hello_shiny_app'),
        ('serve', '0008_add_wordcloud_app'),
    ]

    operations = [
        migrations.RunPython(update_helloshiny_app, revert_helloshiny_app),
        migrations.RunPython(update_wordcloud_app, revert_wordcloud_app),
    ]
