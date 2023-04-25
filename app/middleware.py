from django.shortcuts import reverse, redirect
from django.http import Http404
from nexis.settings import MAINTENANCE_BYPASS_QUERY, MAINTENANCE_MODE
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.cache import cache
from django.utils.cache import get_cache_key, learn_cache_key
from django.conf import settings
from .models import Testimonial
from datetime import datetime
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
import time
import logging

from django.contrib.auth.decorators import user_passes_test

def superuser_check(user):
    return user.is_superuser

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.META.get('PATH_INFO', "")
        query = request.META.get('QUERY_STRING', "")
        user = request.user

        if query and MAINTENANCE_BYPASS_QUERY in query:
            request.session['bypass_maintenance'] = True

        if MAINTENANCE_MODE and not superuser_check(user):
            if not request.session.get('bypass_maintenance', False) and path != reverse("maintenance"):
                response = redirect(reverse("maintenance"))
                return response
        else:
            if path == reverse("maintenance"):
                raise Http404("La pagina richiesta non è stata trovata.")
            
        response = self.get_response(request)

        return response

class TestimonialsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path == reverse('testimonials'):
            if request.user.is_authenticated and request.user.is_staff:
                return self.get_response(request)
            else:
                return HttpResponseRedirect(reverse('index'))
        else:
            return self.get_response(request)
        

class SecurityMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['X-XSS-Protection'] = '1; mode=block'

        csp = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.example.com",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self'",
            "font-src 'self'",
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'"
        ]
        response['Content-Security-Policy'] = "; ".join(csp)

        hsts = "max-age=31536000; includeSubDomains; preload"
        response['Strict-Transport-Security'] = hsts

        return response
