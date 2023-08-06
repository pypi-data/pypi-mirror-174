from rest_framework import serializers
from rest_framework.fields import Field
from erptools.erpmodel import ERPModels
from django.db import models
from django.contrib.auth.models import AbstractUser


class ERPSerializerContextField(Field):
    """
    A read-only field that get its representation from calling a method on the
    parent serializer class. The method called will be of the form
    "get_{field_name}", and should take a single argument, which is the
    object being serialized.

    For example:

    class ExampleSerializer(self):
        extra_info = SerializerMethodField()

        def get_extra_info(self, obj):
            return ...  # Calculate some data to return.
    """

    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        super().__init__(**kwargs)

    def bind(self, field_name, parent):

        def jsonify(value):
            """Checks if the value is a Django Model, anf if so it converts to a dict."""
            exclude_list = {"password"}

            # for models
            if ERPModels in value.__class__.__bases__ or models.Model in value.__class__.__bases__ or AbstractUser in value.__class__.__bases__:
                class SimpleBaseSerializer(serializers.ModelSerializer):
                    class Meta:
                        model = value.__class__
                        fields = "__all__"

                SimpleBaseSerializer.Meta.exclude = [field for field in exclude_list if hasattr( SimpleBaseSerializer.Meta.model, field)]
                # remove private info
                if  SimpleBaseSerializer.Meta.exclude:
                    SimpleBaseSerializer.Meta.fields = None
                return SimpleBaseSerializer(value).data

            # for query sets
            elif isinstance(value, models.query.QuerySet):
                class SimpleBaseSerializer(serializers.ModelSerializer):
                    class Meta:
                        model =  value.first().__class__
                        fields = "__all__"
                # remove private info
                SimpleBaseSerializer.Meta.exclude = [field for field in exclude_list if hasattr( SimpleBaseSerializer.Meta.model, field)]
                if  SimpleBaseSerializer.Meta.exclude:
                    SimpleBaseSerializer.Meta.fields = None
                return SimpleBaseSerializer(value, many=True).data


            return value

        # The method name defaults to `get_{field_name}`.
        if self.method_name is None:
            self.method_name = 'get_context_{field_name}'.format(field_name=field_name)
        # Creates a method returning the get_context_value
        setattr(parent, self.method_name, lambda x: jsonify(x.get_context_value(field_name)))
        super().bind(field_name, parent)

    def to_representation(self, value):
        method = getattr(self.parent, self.method_name)
        return method(value)


class EmailSerializer(serializers.Serializer):
    recipients = serializers.ListField()
    sender = serializers.EmailField()
