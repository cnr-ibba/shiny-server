#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:13:40 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.contrib import admin
from django.forms import ModelForm

from markdownx.admin import MarkdownxModelAdmin

from .models import ShinyApp


class ShinyAppAdminForm(ModelForm):
    class Meta:
        model = ShinyApp
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        r_version = cleaned_data.get('r_version')
        location = cleaned_data.get('location')

        if r_version and location:
            expected_prefix = f"/shiny-{r_version}/"
            if not location.startswith(expected_prefix):
                # Auto-correct the location prefix
                # remove /shiny-X.X/ prefix if present
                parts = location.split('/', 3)
                if len(parts) > 2 and parts[1].startswith('shiny-'):
                    # Already has shiny prefix, replace it
                    app_path = parts[2] if len(parts) > 2 else ''
                    cleaned_data['location'] = f"{expected_prefix}{app_path}"
                elif not location.startswith('/shiny-'):
                    # Does not have shiny prefix, add it
                    location_stripped = location.lstrip('/')
                    cleaned_data['location'] = f"{expected_prefix}{location_stripped}"

        return cleaned_data


class ShinyAppAdmin(MarkdownxModelAdmin):
    form = ShinyAppAdminForm
    list_display = (
        'title', 'location', 'r_version', 'is_public', 'slug',
        'users_display')
    list_filter = ('r_version', 'is_public')
    search_fields = ('title', 'location', 'slug')

    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('users',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'r_version')
        }),
        ('Application Details', {
            'fields': ('location', 'description', 'thumbnail')
        }),
        ('Access Control', {
            'fields': ('is_public', 'users')
        }),
    )

    def users_display(self, obj):
        return ", ".join([
            user.username for user in obj.users.all()
        ])
    users_display.short_description = "users"

    def save_model(self, request, obj, form, change):
        """Ensure location has correct prefix before saving"""
        expected_prefix = f"/shiny-{obj.r_version}/"
        if not obj.location.startswith(expected_prefix):
            # Auto-correct if necessary
            parts = obj.location.split('/', 3)
            if len(parts) > 2 and parts[1].startswith('shiny-'):
                app_path = parts[2] if len(parts) > 2 else ''
                obj.location = f"{expected_prefix}{app_path}"
            else:
                location_stripped = obj.location.lstrip('/')
                obj.location = f"{expected_prefix}{location_stripped}"

        super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(ShinyApp, ShinyAppAdmin)
