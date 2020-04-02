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

        # create a shiny app module
        self.test_app = ShinyApp(
            location="/a/path/",
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

    def test_str(self):
        test = str(self.test_app)
        reference = "<Title> at '/a/path/'"

        self.assertEqual(reference, test)
