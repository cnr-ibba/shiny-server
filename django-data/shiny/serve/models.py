#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 15:45:40 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.
class ShinyApp(models.Model):
    location = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, default='')
    users = models.ManyToManyField(User, related_name="shinyapps")

    def save(self, *args, **kwargs):
        # slugify title if not provided
        if self.slug is None:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shinyapp', kwargs={'slug': self.slug})

    def __str__(self):
        return f"<{self.title}> at '{self.location}'"
