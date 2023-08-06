import sys

from django.db import models

from erptools.creator import DocumentCreator
from erptools.storage import MediaStorage


class ERPModels(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, help_text="Date  created")
    modified_date = models.DateTimeField(auto_now=True, help_text="latest time modified")
    context_object = None

    def __init__(self, *args,**kwargs ):
        self.context_instance = None
        super(ERPModels, self).__init__(*args, **kwargs)

    def get_context_instance(self):
        if self.context_object is None:
            raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)
        if self.context_instance is None:
            obj = self.context_object(self.pk)
            obj.set_base(self)
            self.context_instance = obj
        return self.context_instance

    def get_context(self, values, context={}):
        return self.get_context_instance().get_context(values, context)

    def creator(self):
        return DocumentCreator(self, MediaStorage)

    def get_context_value(self, value):
        return self.get_context([value]).get(value)

    class Meta:
        abstract = True
