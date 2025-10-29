#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 15:45:40 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.module_loading import import_string
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError

from markdownx.models import MarkdownxField

# define user model
User = get_user_model()

# set markdownify function from settings
markdownify = import_string(settings.MARKDOWNX_MARKDOWNIFY_FUNCTION)


# Create your models here.
class ShinyApp(models.Model):
    class RVersion(models.TextChoices):
        R_4_0 = '4.0', 'R 4.0'
        R_4_5 = '4.5', 'R 4.5'

    location = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = MarkdownxField(blank=True, default='')
    thumbnail = models.ImageField(
        upload_to='thumbnails',
        default='default.png')
    users = models.ManyToManyField(User, related_name="shinyapps", blank=True)
    is_public = models.BooleanField(default=False)
    r_version = models.CharField(
        max_length=3,
        choices=RVersion.choices,
        default=RVersion.R_4_5,
        verbose_name='R Version'
    )

    def clean(self):
        """Validate that location starts with correct R version prefix"""
        super().clean()

        expected_prefix = f"/shiny-{self.r_version}/"

        if not self.location.startswith(expected_prefix):
            raise ValidationError({
                'location': f"Location must start with '{expected_prefix}' for R version {self.r_version}"
            })

    def save(self, *args, **kwargs):
        # slugify title if not provided
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.title)

        # Validate before saving
        self.full_clean()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shinyapp', kwargs={'slug': self.slug})

    def formatted_markdown(self):
        """Return a formatted markdown text"""

        return markdownify(self.description)

    def __str__(self):
        return f"<{self.title}> at '{self.location}' (R {self.r_version})"
