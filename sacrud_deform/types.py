#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
types
"""
import colander
import deform
import sqlalchemy
from sqlalchemy import types as sa_types
from sqlalchemy.dialects.postgresql import HSTORE, JSON

from sacrud.exttype import ChoiceType, FileStore, SlugType

from .widgets import ElfinderWidget, HstoreWidget, SlugWidget

try:
    from pyramid_elfinder.models import ElfinderString
except ImportError:
    ElfinderString = 'ElfinderString'

# Map sqlalchemy types to colander types.
_TYPES = {
    sa_types.BigInteger: colander.Integer,
    sa_types.Boolean: colander.Boolean,
    sa_types.Date: colander.Date,
    sa_types.DateTime: colander.DateTime,
    sa_types.Enum: colander.String,
    sa_types.Float: colander.Float,
    sa_types.Integer: colander.Integer,
    sa_types.Numeric: colander.Decimal,
    sa_types.SmallInteger: colander.Integer,
    sa_types.String: colander.String,
    sa_types.Text: colander.String,
    sa_types.Time: colander.Time,
    sa_types.Unicode: colander.String,
    sa_types.UnicodeText: colander.String,
    JSON: colander.String,
    HSTORE: colander.String,
    sqlalchemy.ForeignKey: colander.String,
    ChoiceType: colander.String,
    FileStore: deform.FileData,
    SlugType: colander.String,
}

# Map sqlalchemy types to deform widgets.
_WIDGETS = {
    sa_types.BigInteger: deform.widget.TextInputWidget,
    sa_types.Boolean: deform.widget.CheckboxWidget,
    sa_types.Date: deform.widget.DateInputWidget,
    sa_types.DateTime: deform.widget.DateTimeInputWidget,
    sa_types.Enum: deform.widget.SelectWidget,
    sa_types.Float: deform.widget.TextInputWidget,
    sa_types.Integer: deform.widget.TextInputWidget,
    sa_types.Numeric: deform.widget.TextInputWidget,
    sa_types.SmallInteger: deform.widget.TextInputWidget,
    sa_types.String: deform.widget.TextInputWidget,
    sa_types.Text: deform.widget.TextAreaWidget,
    sa_types.Time: deform.widget.TextInputWidget,
    sa_types.Unicode: deform.widget.TextInputWidget,
    sa_types.UnicodeText: deform.widget.TextAreaWidget,
    JSON: deform.widget.TextAreaWidget,
    HSTORE: HstoreWidget,
    sqlalchemy.ForeignKey: deform.widget.SelectWidget,
    ChoiceType: deform.widget.SelectWidget,
    FileStore: deform.widget.FileUploadWidget,
    ElfinderString: ElfinderWidget,
    SlugType: SlugWidget,
}
