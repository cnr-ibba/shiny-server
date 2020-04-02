#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 16:40:39 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.test import TestCase, Client
from django.urls import resolve, reverse

from ..views import IndexView, ShinyAppView


class BaseMixin():

    fixtures = [
        "serve/shinyapp",
        "serve/user",
    ]


class IndexViewTestCase(BaseMixin, TestCase):

    def setUp(self):
        # call base method
        super().setUp()

        # test page
        self.url = reverse('home')
        self.response = self.client.get(self.url)

    def test_url_resolves_view(self):
        view = resolve('/')
        self.assertIsInstance(view.func.view_class(), IndexView)


class ShinyAppViewTestCase(BaseMixin, TestCase):

    def setUp(self):
        # call base method
        super().setUp()

        self.client = Client()
        self.client.login(username='test', password='test')

    def test_url_resolves_view(self):
        view = resolve('/applications/hello-shiny/')
        self.assertIsInstance(view.func.view_class(), ShinyAppView)

    def test_get_my_app(self):
        url = reverse('shinyapp', kwargs={'slug': 'hello-shiny'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_not_my_app(self):
        url = reverse('shinyapp', kwargs={'slug': 'shiny-text'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_get_public_app(self):
        url = reverse('shinyapp', kwargs={'slug': 'reactivity'})

        # I can get a public app whitout logging
        client = Client()
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
