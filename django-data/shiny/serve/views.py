#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:34:27 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, TemplateView

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

        if shinyapp.is_public:
            return True

        if self.request.user in shinyapp.users.all():
            return True

        return False

    def get_permission_denied_message(self):
        return "access denied for user '%s'" % (self.request.user.username)


class ShinyAppListView(ListView):
    model = ShinyApp
    template_name = 'serve/shinyapp_list.html'

    def get_queryset(self):
        """Filter objects by ownership or by public applications"""

        # call base method
        queryset = super().get_queryset()

        if not self.request.user.is_authenticated:
            # filter only public applications
            queryset = queryset.filter(is_public=True)

        else:
            # return queryset if I'm the admin
            if self.request.user.is_superuser:
                return queryset

            # get only public and my applications
            queryset = queryset.filter(
                Q(is_public=True) | Q(users__in=[self.request.user]))

        return queryset


def auth(request):
    # print(f"Headers: {request.headers}")
    # print(f"META: {request.META}")
    # check 1: user is admin, access granted
    if request.user.is_superuser:
        return HttpResponse(status=200)

    # get a request uri like: /shiny/001-hello/__sockjs__/...
    # HTTP_X_ORIGINAL_URI is defined in NGINX configuration
    request_uri = request.META['HTTP_X_ORIGINAL_URI']

    print(f"request_uri: {request_uri}")

    # split path and get a location from the first two items
    path = request_uri.split("/")
    location = "/".join(path[:3]) + "/"

    # get an object model by location (if exists)
    shiny_app_qs = ShinyApp.objects.filter(location=location)

    # location is supposed to be unique by model definition
    if shiny_app_qs.count() == 1:
        shinyapp = ShinyApp.objects.get(location=location)

        print(f"Got model {shinyapp}")

        # check 2: is this app public available?
        if shinyapp.is_public:
            print(f"{request_uri} is public")
            return HttpResponse(status=200)

        # check 3: ensure authentication
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        # check 4: user owns the application
        if request.user in shinyapp.users.all():
            print(f"{request_uri} allowed to {request.user.username}")
            return HttpResponse(status=200)

    # this will return if a model doesn't exists or I don't have permissions
    print(f"{request_uri} denied to {request.user.username}")
    return HttpResponse(status=403)
