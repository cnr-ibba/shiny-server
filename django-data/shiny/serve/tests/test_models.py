#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:56:53 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import ShinyApp

User = get_user_model()


class ShinyAppTestCase(TestCase):
    fixtures = [
        "serve/user",
    ]

    def setUp(self):
        # get a user
        self.user = User.objects.get(username="test")

        # create a shiny app module with R 4.5 (default)
        self.test_app = ShinyApp(
            location="/shiny-4.5/a/path/",
            title="Title",
            description="A description")

    def test_save(self):
        self.test_app.save()

        # add object to many to many relationship
        self.test_app.users.add(self.user)
        self.test_app.save()
        self.test_app.refresh_from_db()

        # assert a slug
        self.assertEqual("title", self.test_app.slug)
        # assert r_version default
        self.assertEqual("4.5", self.test_app.r_version)

    def test_str(self):
        test = str(self.test_app)
        reference = "<Title> at '/shiny-4.5/a/path/' (R 4.5)"

        self.assertEqual(reference, test)

    def test_r_version_validation(self):
        """Test that location must match r_version"""
        from django.core.exceptions import ValidationError

        # Test R 4.0 with correct prefix
        app_40 = ShinyApp(
            location="/shiny-4.0/test/",
            title="Test R 4.0",
            r_version="4.0"
        )
        app_40.save()  # Should work
        self.assertEqual("4.0", app_40.r_version)

        # Test R 4.5 with wrong prefix
        app_wrong = ShinyApp(
            location="/shiny-4.0/test/",
            title="Test Wrong",
            r_version="4.5"
        )
        with self.assertRaises(ValidationError):
            app_wrong.save()  # Should fail
