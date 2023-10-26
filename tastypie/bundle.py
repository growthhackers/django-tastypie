from __future__ import unicode_literals
from django.http import HttpRequest
from django.utils import six

def exploder(selected_fields):
    result = {}
    for field in selected_fields:
        current_dict = result
        for item in field.split('__'):
            if item not in current_dict.keys():
                current_dict[item] = {}
            current_dict = current_dict[item]
    return result

# In a separate file to avoid circular imports...
class Bundle(object):
    """
    A small container for instances and converted data for the
    ``dehydrate/hydrate`` cycle.

    Necessary because the ``dehydrate/hydrate`` cycle needs to access data at
    different points.
    """
    def __init__(self,
                 obj=None,
                 data=None,
                 request=None,
                 related_obj=None,
                 related_name=None,
                 objects_saved=None,
                 related_objects_to_save=None,
                 via_uri=False,
                 selected_fields=None
                 ):
        self.obj = obj
        self.data = data or {}
        self.request = request or HttpRequest()
        self.related_obj = related_obj
        self.related_name = related_name
        self.errors = {}
        self.objects_saved = objects_saved or set()
        self.related_objects_to_save = related_objects_to_save or {}
        self.via_uri = via_uri
        self.selected_fields = {}
        if selected_fields:
            self.selected_fields = exploder(selected_fields)

    def __repr__(self):
        repr_string = "<Bundle for obj: '%r' and with data: '%r'>"
        if six.PY2:
            repr_string = repr_string.encode('utf-8')
        return repr_string % (self.obj, self.data)

    def is_selected(self, field):
        if self.selected_fields == {}:
            return True
        if field in self.selected_fields.keys():
            return True
        return False
