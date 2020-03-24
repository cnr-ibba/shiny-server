#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:34:27 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.views.generic import DetailView, ListView
from django.http import HttpResponse

from .models import ShinyApp


class ShinyAppView(DetailView):
    model = ShinyApp
    template_name = 'serve/shinyapp_detail.html'


class ShinyAppListView(ListView):
    model = ShinyApp
    template_name = 'serve/shinyapp_list.html'


def auth(request):
    if request.user.is_authenticated:
        print("user is authenticated")
        return HttpResponse(status=200)

    print("user is not authenticated")
    return HttpResponse(status=401)
