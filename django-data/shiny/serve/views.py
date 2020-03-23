#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:34:27 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.shortcuts import render
from django.http import HttpResponse


def shiny(request):
    return render(request, 'serve/shiny.html')


def auth(request):
    if request.user.is_authenticated:
        print("user is authenticated")
        return HttpResponse(status=200)

    print("user is not authenticated")
    return HttpResponse(status=403)
