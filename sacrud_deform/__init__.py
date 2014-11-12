#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
from gettext import gettext as _

import colander
import deform
import sqlalchemy
from deform import Form
from sqlalchemy import types as sa_types

from sacrud.common import get_relationship
from sacrud.exttype import ChoiceType, GUID, SlugType

from .common import (_get_column_type_by_sa_type, _get_widget_type_by_sa_type,
                     _sa_row_to_choises, get_column_default_value,
                     get_column_description, get_column_title, get_column_type,
                     get_pk, get_validator, get_widget)


class GroupShema(object):
    def __init__(self, group, table, obj, dbsession, columns, translate=_):
        self.obj = obj
        self.table = table
        self.relationships = get_relationship(table)
        self.dbsession = dbsession
        self.js_list = []
        self.translate = translate
        self.schema = colander.Schema(name=translate(group))
        self.build(columns)

    def get_column_css_styles(self, col):
        css_class = ['sacrud_deform', ]
        if hasattr(self.table, 'sacrud_css_class'):
            for key, value in self.table.sacrud_css_class.items():
                if col in value:
                    css_class.append(key)
            return ' '.join(css_class)
        return None

    def get_node(self, values=None, mask=None, validator=None,
                 node_kwargs={}, **kwargs):
        col_name = kwargs['col'].name
        column_type = _get_column_type_by_sa_type(kwargs['sa_type'])
        widget_type = _get_widget_type_by_sa_type(kwargs['sa_type'])
        if 'col_name' in kwargs:
            col_name = kwargs['col_name']
        if kwargs['sa_type'] == sa_types.Enum and not values:
            values = [(x, x) for x in kwargs['col'].type.enums]
        if kwargs['sa_type'] == GUID and not mask:
            mask = 'hhhhhhhh-hhhh-hhhh-hhhh-hhhhhhhhhhhh'
        if kwargs['sa_type'] == ChoiceType and not values:
            values = [(v, k) for k, v in kwargs['col'].type.choices.items()]
        if kwargs['sa_type'].__name__ == 'ElfinderString':
            self.js_list.append('pyramid_elfinder:static/js/elfinder.min.js')
            self.js_list.append('pyramid_elfinder:'
                                'static/js/proxy/elFinderSupportVer1.js')
        if kwargs['sa_type'] == SlugType:
            self.js_list.append('pyramid_sacrud:'
                                'static/js/lib/speakingurl.min.js')
        widget = get_widget(widget_type, values, mask, kwargs['css_class'],
                            kwargs['col'])
        validator = get_validator(widget)
        if widget_type == deform.widget.FileUploadWidget:
            kwargs['description'] = kwargs['default']
            kwargs['default'] = colander.null
        if kwargs['col'].nullable is True or \
                kwargs['col'].primary_key is True:
            node_kwargs = {'missing': True}
        default_kwargs = {
            'title': self.translate(kwargs['title']),
            'name': col_name,
            'default': kwargs['default'],
            'description': kwargs['description'],
            'widget': widget,
            'validator': validator,
        }
        default_kwargs.update(**node_kwargs)
        return colander.SchemaNode(column_type(), **default_kwargs)

    # TODO: rewrite it
    def get_foreign_key_node(self, **kwargs):
        kwargs['sa_type'] = sqlalchemy.ForeignKey
        for rel in self.relationships:
            if kwargs['col'] in rel.remote_side or kwargs['col'] in rel.local_columns:
                choices = self.dbsession.query(rel.mapper).all()
                choices = [('', '')] + _sa_row_to_choises(choices)
                rel_obj = getattr(self.obj, rel.key, None)
                kwargs['col_name'] = rel.key + '[]'
                if rel_obj:
                    kwargs['default'] = get_pk(rel_obj)
                return self.get_node(values=choices, **kwargs)

    def custom_type_preprocessing(self, col):
        if isinstance(col, (list, tuple)):
            group = col[0]
            c = col[1]
            gs = GroupShema(group, self.table, self.obj, self.dbsession, c)
            self.schema.add(gs.schema)
            return True
        elif col.__class__.__name__ == "WidgetRelationship":
            col.preprocessing()
            choices = self.dbsession.query(col.table).all()
            choices = [('', '')] + _sa_row_to_choises(choices)
            rel_name = col.relation.key
            selected = []
            if self.obj:
                selected = getattr(self.obj, rel_name)
                try:
                    iter(selected)
                    selected = [get_pk(x) for x in selected]
                except TypeError:
                    selected = []
            m2m = colander.SchemaNode(
                colander.Set(),
                title=self.translate(col.info['name']),
                name=rel_name+'[]',
                default=selected,
                widget=deform.widget.SelectWidget(
                    values=choices,
                    multiple=True,
                ),
            )
            self.schema.add(m2m)
            return True
        elif col.__class__.__name__ == "WidgetInlines":
            col.preprocessing()
            schema = col.schema()
            self.schema.add(schema)
            return True
        return False

    def build(self, columns):
        for col in columns:
            if self.custom_type_preprocessing(col):
                continue

            node = None
            title = get_column_title(col, self.translate)
            default = get_column_default_value(col, self.obj)
            description = get_column_description(col)
            css_class = self.get_column_css_styles(col)
            sa_type = get_column_type(col)
            params = {'col': col,
                      'sa_types': sa_type,
                      'title': title,
                      'description': description,
                      'default': default,
                      'css_class': css_class,
                      'sa_type': sa_type,
                      }

            if hasattr(col, 'foreign_keys'):
                if col.foreign_keys:
                    node = self.get_foreign_key_node(**params)
            if not node:
                node = self.get_node(**params)
            self.schema.add(node)


def form_generator(dbsession, obj, table, columns_by_group, request):
    schema = colander.Schema()
    js_list = []
    for group, columns in columns_by_group:
        gs = GroupShema(group, table, obj, dbsession, columns,
                        translate=request.localizer.translate)
        schema.add(gs.schema)
        js_list.extend(gs.js_list)
    return Form(schema, request=request), list(set(js_list))
