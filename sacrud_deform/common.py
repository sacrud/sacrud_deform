#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Common
"""
from gettext import gettext as _

import colander
import json
import deform
from sqlalchemy import types as sa_types

from sacrud.common import pk_to_list
from sacrud.exttype import ChoiceType

from .types import _TYPES, _WIDGETS


class HTMLText(object):
    def __init__(self, text):
        self.text = text

    def __html__(self):
        try:
            return unicode(self.text)
        except NameError:           # pragma: no cover
            return str(self.text)   # pragma: no cover


def get_pk(obj):
    return json.dumps(pk_to_list(obj))


def _sa_row_to_choises(rows):
    return [(get_pk(ch), ch.__repr__()) for ch in rows]


def _get_column_type_by_sa_type(sa_type):
    """
    Returns the colander type that correspondents to the sqlalchemy type
    'sa_type'.
    """
    return _TYPES.get(sa_type) or colander.String


def _get_widget_type_by_sa_type(sa_type):
    """
    Returns the deform widget that correspondents to the sqlalchemy type
    'sa_type'.
    """
    return _WIDGETS.get(sa_type) or deform.widget.TextInputWidget


def get_validator(widget):
    return colander.All()


def get_column_title(col, translate=_):
    if 'verbose_name' in col.info:
        name = col.info['verbose_name']
    else:
        name = getattr(col, 'name', col.key)
    if 'sacrud_position' in col.info:
        if col.info['sacrud_position'] == 'inline':
            if 'verbose_name' in col.info:
                name = col.info['verbose_name']
            else:
                name = col.sacrud_name
    return translate(name)


def get_column_type(col):
    if hasattr(col, 'type'):
        return col.type.__class__
    return None


def get_column_description(col):
    if 'description' in col.info:
        return HTMLText(col.info['description'])
    return None


def get_column_default_value(col, obj):
    value = None
    col_type = get_column_type(col)
    if obj and hasattr(col, 'instance_name'):
        value = getattr(obj, col.instance_name)
    elif obj and hasattr(col, 'name'):
        try:
            value = getattr(obj, col.name, colander.null)
        except UnicodeEncodeError:
            value = colander.null
    if value is None:
        value = colander.null
    elif col_type == ChoiceType:
        value = value[0]
    if col_type == sa_types.Boolean:
        value = bool(value)
    return value


class MemoryTmpStore(dict):
    """ Instances of this class implement the
    :class:`deform.interfaces.FileUploadTempStore` interface"""
    def preview_url(self, uid):
        return None


def get_widget(widget_type, values, mask, css_class, col):
    if widget_type == deform.widget.FileUploadWidget:
        tmpstore = MemoryTmpStore()
        return widget_type(tmpstore)
    return widget_type(values=values,
                       mask=mask,
                       col=col,
                       mask_placeholder='_',
                       css_class=css_class,
                       )
