#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:34:27 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView, ListView
from django.http import HttpResponse

from .models import ShinyApp


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

    # split path and get a location from the first two items
    path = request_uri.split("/")

    print(path)

    # check path lenght (ie /shiny/")
    if len(path) < 3 or path[2] == '':
        print(f"{request_uri} allowed to {request.user.username}")
        return HttpResponse(status=200)

    location = "/".join(path[:3]) + "/"

    # get an object model by location
    shinyapp = ShinyApp.objects.get(location=location)

    print(f"Got model {shinyapp}")

    # check permissions
    if request.user in shinyapp.users.all():
        print(f"{request_uri} allowed to {request.user.username}")
        return HttpResponse(status=200)

    print(f"{request_uri} denied to {request.user.username}")
    return HttpResponse(status=403)
