#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 16:40:39 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.test import TestCase, Client
from django.urls import resolve, reverse

from ..views import IndexView, ShinyAppView, ShinyAppListView


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
        view = resolve('/applications/reactivity/')
        self.assertIsInstance(view.func.view_class(), ShinyAppView)

    def test_get_my_app(self):
        url = reverse('shinyapp', kwargs={'slug': 'hello-shiny'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_get_not_my_app(self):
        url = reverse('shinyapp', kwargs={'slug': 'shiny-text'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_app_for_admin(self):
        url = reverse('shinyapp', kwargs={'slug': 'shiny-text'})

        # login as admin
        client = Client()
        client.login(username='admin', password='test')
        response = client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_get_public_app(self):
        url = reverse('shinyapp', kwargs={'slug': 'reactivity'})

        # I can get a public app whitout logging
        client = Client()
        response = client.get(url)

        self.assertEqual(response.status_code, 200)


class ShinyAppListViewTestCase(BaseMixin, TestCase):
    def setUp(self):
        # call base method
        super().setUp()

        # set the base url
        self.url = reverse('applications')

    def test_url_resolves_view(self):
        view = resolve('/applications/')
        self.assertIsInstance(view.func.view_class(), ShinyAppListView)

    def test_get_public_app(self):
        # I can get a public app whitout logging
        client = Client()
        response = client.get(self.url)

        self.assertEqual(response.status_code, 200)

        # ok get queryset from response.context and test for the public app
        qs = response.context['shinyapp_list']
        self.assertEqual(qs.count(), 1)

        public = qs.first()
        self.assertEqual(public.slug, 'reactivity')

    def test_get_admin_app(self):
        # login as admin
        client = Client()
        client.login(username='admin', password='test')
        response = client.get(self.url)

        # ok get all app for the admin
        qs = response.context['shinyapp_list']
        self.assertEqual(qs.count(), 3)

    def test_my_app(self):
        # login as a normal user
        client = Client()
        client.login(username='test', password='test')
        response = client.get(self.url)

        # get only my app and the public app
        qs = response.context['shinyapp_list']
        self.assertEqual(qs.count(), 2)

        reference = ['reactivity', 'shiny-text']
        test = sorted([app.slug for app in qs])

        # test for expected slugs
        self.assertEqual(reference, test)


class AuthURLTestCase(BaseMixin, TestCase):
    def setUp(self):
        # call base method
        super().setUp()

    def test_anonymous_user(self):
        client = Client()

        # test not an app
        response = client.get("/auth/", HTTP_X_ORIGINAL_URI='/shiny/')
        self.assertEqual(response.status_code, 403)

        # test public app (got access)
        response = client.get(
            "/auth/", HTTP_X_ORIGINAL_URI='/shiny-4.5/003-reactivity/')
        self.assertEqual(response.status_code, 200)

        # a private app need a login
        response = client.get(
            "/auth/", HTTP_X_ORIGINAL_URI='/shiny-4.5/002-text/')
        self.assertEqual(response.status_code, 401)

    def test_user(self):
        # authenticate user
        client = Client()
        client.login(username='test', password='test')

        # test not an app
        response = client.get("/auth/", HTTP_X_ORIGINAL_URI='/shiny/')
        self.assertEqual(response.status_code, 403)

        # test public app (got access)
        response = client.get(
            "/auth/", HTTP_X_ORIGINAL_URI='/shiny-4.5/003-reactivity/')
        self.assertEqual(response.status_code, 200)

        # can access to my private app
        response = client.get(
            "/auth/", HTTP_X_ORIGINAL_URI='/shiny-4.5/002-text/')
        self.assertEqual(response.status_code, 200)

        # can't access to others application
        response = client.get(
            "/auth/", HTTP_X_ORIGINAL_URI='/shiny-4.5/001-hello/')
        self.assertEqual(response.status_code, 403)

    def test_superuser(self):
        # authenticate as superuser
        client = Client()
        client.login(username='admin', password='test')

        # test for auth without HTTP_X_ORIGINAL_URI
        response = client.get("/auth/")
        self.assertEqual(response.status_code, 403)

        # test not an app: even for admin this is forbidden
        response = client.get("/auth/", HTTP_X_ORIGINAL_URI='/shiny/')
        self.assertEqual(response.status_code, 403)

        # test public app (got access)
        response = client.get(
            "/auth/", HTTP_X_ORIGINAL_URI='/shiny-4.5/003-reactivity/')
        self.assertEqual(response.status_code, 200)

        # can access to others applications
        response = client.get(
            "/auth/", HTTP_X_ORIGINAL_URI='/shiny-4.5/002-text/')
        self.assertEqual(response.status_code, 200)

        # can access to my private app
        response = client.get(
            "/auth/", HTTP_X_ORIGINAL_URI='/shiny-4.5/001-hello/')
        self.assertEqual(response.status_code, 200)
