#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:50:03 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from serve.admin import ShinyAppAdmin, ShinyAppAdminForm
from serve.models import ShinyApp


class AdminTestCase(TestCase):
    fixtures = [
        "serve/shinyapp",
        "serve/user",
    ]

    def setUp(self):
        self.client = Client()
        self.client.login(username="admin", password="test")

    def test_shinyapp_admin_changelist(self):
        url = reverse("admin:serve_shinyapp_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ShinyAppAdminFormTestCase(TestCase):
    """Test cases for ShinyAppAdminForm.clean() method"""

    fixtures = [
        "serve/shinyapp",
        "serve/user",
    ]

    def test_clean_adds_correct_prefix_when_missing(self):
        """Test that the form auto-adds the correct /shiny-X.X/ prefix"""
        form = ShinyAppAdminForm(
            data={
                "title": "Test App 1",
                "slug": "test-app-form-1",
                "r_version": "4.5",
                "location": "test-app-1/",
                "is_public": True,
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["location"], "/shiny-4.5/test-app-1/")

    def test_clean_replaces_incorrect_version_prefix(self):
        """Test that the form replaces wrong version prefix with correct one"""
        form = ShinyAppAdminForm(
            data={
                "title": "Test App 2",
                "slug": "test-app-form-2",
                "r_version": "4.5",
                "location": "/shiny-4.0/test-app-2/",
                "is_public": True,
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["location"], "/shiny-4.5/test-app-2/")

    def test_clean_keeps_correct_prefix_unchanged(self):
        """Test that correct prefix is not modified"""
        form = ShinyAppAdminForm(
            data={
                "title": "Test App 3",
                "slug": "test-app-form-3",
                "r_version": "4.5",
                "location": "/shiny-4.5/test-app-3/",
                "is_public": True,
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["location"], "/shiny-4.5/test-app-3/")

    def test_clean_adds_trailing_slash_if_missing(self):
        """Test that trailing slash is added if missing"""
        form = ShinyAppAdminForm(
            data={
                "title": "Test App 4",
                "slug": "test-app-form-4",
                "r_version": "4.5",
                "location": "/shiny-4.5/test-app-4",
                "is_public": True,
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["location"], "/shiny-4.5/test-app-4/")

    def test_clean_with_r40_version(self):
        """Test prefix correction with R 4.0 version"""
        form = ShinyAppAdminForm(
            data={
                "title": "Test App 5",
                "slug": "test-app-form-5",
                "r_version": "4.0",
                "location": "test-app-5/",
                "is_public": True,
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["location"], "/shiny-4.0/test-app-5/")

    def test_clean_with_leading_slash_no_prefix(self):
        """Test location with leading slash but no shiny prefix"""
        form = ShinyAppAdminForm(
            data={
                "title": "Test App 6",
                "slug": "test-app-form-6",
                "r_version": "4.5",
                "location": "/test-app-6/",
                "is_public": True,
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["location"], "/shiny-4.5/test-app-6/")

    def test_clean_handles_nested_paths(self):
        """Test location with nested directory structure"""
        form = ShinyAppAdminForm(
            data={
                "title": "Test App 7",
                "slug": "test-app-form-7",
                "r_version": "4.5",
                "location": "apps/subdir/myapp/",
                "is_public": True,
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["location"], "/shiny-4.5/apps/subdir/myapp/")

    def test_clean_replaces_and_adds_trailing_slash(self):
        """Test that both prefix replacement and trailing slash
        addition work together"""

        form = ShinyAppAdminForm(
            data={
                "title": "Test App 8",
                "slug": "test-app-form-8",
                "r_version": "4.5",
                "location": "/shiny-4.0/test-app-8",
                "is_public": True,
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["location"], "/shiny-4.5/test-app-8/")


class ShinyAppAdminSaveModelTestCase(TestCase):
    """Test cases for ShinyAppAdmin.save_model() method"""

    fixtures = [
        "serve/user",
    ]

    def setUp(self):
        self.site = AdminSite()
        self.admin = ShinyAppAdmin(ShinyApp, self.site)

        # Create a mock request with user
        User = get_user_model()
        self.user = User.objects.filter(username="admin").first()
        if not self.user:
            self.user = User.objects.create_superuser("admin", "admin@test.com", "test")

        self.factory = RequestFactory()
        self.request = self.factory.get("/admin/")
        self.request.user = self.user

    def test_save_model_adds_correct_prefix_when_missing(self):
        """Test that save_model auto-adds the correct /shiny-X.X/ prefix"""
        app = ShinyApp(
            title="Test App Save 1",
            slug="test-app-save-1",
            r_version="4.5",
            location="app1/",
            is_public=True,
        )

        # Create a form instance
        form = ShinyAppAdminForm(instance=app)

        self.admin.save_model(self.request, app, form, change=False)

        # Reload from database
        saved_app = ShinyApp.objects.get(slug="test-app-save-1")
        self.assertEqual(saved_app.location, "/shiny-4.5/app1/")

    def test_save_model_replaces_incorrect_version_prefix(self):
        """Test that save_model replaces wrong version prefix with correct one"""
        app = ShinyApp(
            title="Test App Save 2",
            slug="test-app-save-2",
            r_version="4.5",
            location="/shiny-4.0/app2/",
            is_public=True,
        )

        # Create a form instance
        form = ShinyAppAdminForm(instance=app)

        self.admin.save_model(self.request, app, form, change=False)

        saved_app = ShinyApp.objects.get(slug="test-app-save-2")
        self.assertEqual(saved_app.location, "/shiny-4.5/app2/")

    def test_save_model_keeps_correct_prefix_unchanged(self):
        """Test that save_model doesn't modify correct prefix"""
        app = ShinyApp(
            title="Test App Save 3",
            slug="test-app-save-3",
            r_version="4.0",
            location="/shiny-4.0/app3/",
            is_public=True,
        )

        # Create a form instance
        form = ShinyAppAdminForm(instance=app)

        self.admin.save_model(self.request, app, form, change=False)

        saved_app = ShinyApp.objects.get(slug="test-app-save-3")
        self.assertEqual(saved_app.location, "/shiny-4.0/app3/")

    def test_save_model_handles_location_with_leading_slash(self):
        """Test save_model with location starting with / but no shiny prefix"""
        app = ShinyApp(
            title="Test App Save 4",
            slug="test-app-save-4",
            r_version="4.5",
            location="/app4/",
            is_public=True,
        )

        # Create a form instance
        form = ShinyAppAdminForm(instance=app)

        self.admin.save_model(self.request, app, form, change=False)

        saved_app = ShinyApp.objects.get(slug="test-app-save-4")
        self.assertEqual(saved_app.location, "/shiny-4.5/app4/")

    def test_save_model_on_update(self):
        """Test save_model works correctly when updating existing instance"""
        # Create initial app with correct location
        app = ShinyApp.objects.create(
            title="Original App",
            slug="original-app",
            r_version="4.0",
            location="/shiny-4.0/original/",
            is_public=True,
        )

        # Now update it with different r_version
        app.r_version = "4.5"
        # Location doesn't match new version

        # Create a form instance
        form = ShinyAppAdminForm(instance=app)

        self.admin.save_model(self.request, app, form, change=True)

        # Reload from database
        updated_app = ShinyApp.objects.get(slug="original-app")
        self.assertEqual(updated_app.location, "/shiny-4.5/original/")
        self.assertEqual(updated_app.r_version, "4.5")

    def test_save_model_with_nested_path(self):
        """Test save_model with deeply nested application path"""
        app = ShinyApp(
            title="Nested App",
            slug="nested-app",
            r_version="4.5",
            location="apps/category/subdir/myapp/",
            is_public=True,
        )

        # Create a form instance
        form = ShinyAppAdminForm(instance=app)

        self.admin.save_model(self.request, app, form, change=False)

        saved_app = ShinyApp.objects.get(slug="nested-app")
        self.assertEqual(saved_app.location, "/shiny-4.5/apps/category/subdir/myapp/")
