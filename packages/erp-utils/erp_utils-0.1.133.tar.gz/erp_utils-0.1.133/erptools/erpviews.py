import re

from django.apps import apps
from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from erptools.serializers import EmailSerializer


class ERPViewSet(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):

    def send_email(self, request, pk, title, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_sender = serializer.data['sender']
        instance = self.queryset.get(pk=pk)
        recipients = serializer.data['recipients']
        return Response(instance.creator().email(title, email_sender, recipients, context=None))


class DocViewerViewSet(viewsets.GenericViewSet):
    basename = 'doc-viewer'

    @action(detail=False, methods=['GET'], name='pdf_viewer',
            url_path='pdf/(?P<model>\w+)/(?P<pk>\w+)/(?P<template_type>\w+)')
    def pdf_viewer(self, request, model, pk, template_type, *args, **kwargs):
        # The full function path contains the appname
        function_name = str(request.resolver_match.func.cls)
        app_name = re.findall("'api.(.*?).views.", function_name)[0]
        # get requested model
        obj = apps.get_model(app_name, model.lower())
        instance = obj.objects.get(pk=pk)
        return instance.creator().view_pdf(request, template_type)

    @action(detail=False, methods=['GET'], name='html_viewer',
            url_path='html/(?P<model>\w+)/(?P<pk>\w+)/(?P<template_type>\w+)')
    def html_viewer(self, request, model, pk, template_type, *args, **kwargs):
        # The full function path contains the appname
        function_name = str(request.resolver_match.func.cls)
        app_name = re.findall("'api.(.*?).views.", function_name)[0]
        # get requested model
        obj = apps.get_model(app_name, model.lower())
        instance = obj.objects.get(pk=pk)
        return instance.creator().view_html(request, template_type)
