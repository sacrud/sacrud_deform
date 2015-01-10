#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
import colander
import deform
from sqlalchemy import Column
from sqlalchemy.orm.properties import ColumnProperty, RelationshipProperty
from sqlalchemy.orm.relationships import MANYTOMANY, MANYTOONE, ONETOMANY

from colanderalchemy import SQLAlchemySchemaNode

from .common import _sa_row_to_choises, get_pk, get_column_title
from sacrud.common import columns_by_group


def property_values(dbsession, column):
    choices = dbsession.query(column.mapper).all()
    return [('', '')] + _sa_row_to_choises(choices)


class SacrudForm(object):

    def __init__(self, dbsession, obj, table, request):
        self.dbsession = dbsession
        self.translate = request.localizer.translate
        self.obj = obj
        self.table = table
        self.columns_by_group = columns_by_group(self.table)
        self.schema = colander.Schema()

    def build(self):
        appstruct = {}
        for group_name, columns in self.columns_by_group:
            group = self.group_schema(group_name, columns)
            self.schema.add(group)
            appstruct = dict({group_name: group.dictify(self.obj)}.items()
                             + appstruct.items())
        form = deform.Form(self.schema)
        form.set_appstruct(appstruct)
        return form

    def group_schema(self, group, columns):
        columns = self.preprocessing(columns)
        includes = [x for x in columns]
        return SQLAlchemySchemaNode(self.table,
                                    name=group,
                                    title=group,
                                    includes=includes)

    def get_relationship_schemanode(self, column):
        default = None
        selected = []
        relationship = getattr(self.obj, column.key, None)
        values = property_values(self.dbsession, column)
        if column.direction is MANYTOONE:
            if relationship:
                default = get_pk(relationship)
            field = colander.SchemaNode(
                colander.String(),
                title=get_column_title(column, self.translate),
                name=column.key + '[]',
                default=default,
                missing=None,
                widget=deform.widget.SelectWidget(values=values))
        elif column.direction in (ONETOMANY, MANYTOMANY):
            if relationship:
                try:
                    iter(relationship)
                    selected = [get_pk(x) for x in relationship]
                except TypeError:
                    selected = []
            field = colander.SchemaNode(
                colander.Set(),
                title=get_column_title(column, self.translate),
                name=column.key + '[]',
                default=selected,
                missing=None,
                widget=deform.widget.SelectWidget(
                    values=values,
                    multiple=True,
                ),
            )
        return field

    def preprocessing(self, columns):
        new_column_list = []
        for column in columns:
            if hasattr(column, 'property'):
                column = column.property
            if not isinstance(column, (Column, ColumnProperty,
                                       RelationshipProperty)):
                continue
            elif isinstance(column, RelationshipProperty):
                field = self.get_relationship_schemanode(column)
                new_column_list.append(field)
            elif isinstance(column, (ColumnProperty, Column)):
                new_column_list.append(column.name)
        return new_column_list


def includeme(config):
    config.add_static_view('sacrud_deform_static', 'sacrud_deform:static')
