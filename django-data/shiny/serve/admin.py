#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:13:40 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.contrib import admin

from .models import ShinyApp


class ShinyAppAdmin(admin.ModelAdmin):
    list_display = (
        'location', 'title', 'slug', 'description', 'is_public',
        'users_display')

    prepopulated_fields = {'slug': ('title',)}

    def users_display(self, obj):
        return ", ".join([
            user.username for user in obj.users.all()
        ])
    users_display.short_description = "users"


# Register your models here.
admin.site.register(ShinyApp, ShinyAppAdmin)
