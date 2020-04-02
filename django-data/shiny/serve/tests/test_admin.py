#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:50:03 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.test import Client, TestCase
from django.urls import reverse


class AdminTestCase(TestCase):
    fixtures = [
        "serve/shinyapp",
        "serve/user",
    ]

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='test')

    def test_dictbreedadmin(self):
        url = reverse('admin:serve_shinyapp_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
