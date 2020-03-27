#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:34:27 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView, ListView, TemplateView
from django.http import HttpResponse

from .models import ShinyApp


class IndexView(TemplateView):
    """Home page"""

    template_name = "serve/index.html"


class ShinyAppView(UserPassesTestMixin, DetailView):
    model = ShinyApp
    template_name = 'serve/shinyapp_detail.html'
    permission_denied_message = 'access denied'

    def test_func(self):
        # check ownership of such object
        shinyapp = self.get_object()

        if self.request.user in shinyapp.users.all():
            return True

        return False

    def get_permission_denied_message(self):
        return "access denied for user '%s'" % (self.request.user.username)


class ShinyAppListView(ListView):
    model = ShinyApp
    template_name = 'serve/shinyapp_list.html'


def auth(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    # get a request uri like: /shiny/001-hello/__sockjs__/...
    request_uri = request.META['REQUEST_URI']

    # check a specific path
    # HINT: hide the /shiny/ location?
    if request_uri == "/shiny/":
        print(f"{request_uri} allowed to {request.user.username}")
        return HttpResponse(status=200)

    # split path and get a location from the first two items
    path = request_uri.split("/")
    location = "/".join(path[:3]) + "/"

    # get an object model by location (if exists)
    shiny_app_qs = ShinyApp.objects.filter(location=location)

    # location is supposed to be unique by model definition
    if shiny_app_qs.count() == 1:
        shinyapp = ShinyApp.objects.get(location=location)

        print(f"Got model {shinyapp}")

        # TODO: is this app public available?

        # check permissions
        if request.user in shinyapp.users.all():
            print(f"{request_uri} allowed to {request.user.username}")
            return HttpResponse(status=200)

    # this will return if a model doesn't exists or I don't have permissions
    print(f"{request_uri} denied to {request.user.username}")
    return HttpResponse(status=403)
