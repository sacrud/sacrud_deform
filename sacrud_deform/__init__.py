#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
import json

from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request

import deform
import colander
from saexttype import ChoiceType
from sqlalchemy import Enum, Column, Boolean
from pkg_resources import resource_filename
from sacrud.common import columns_by_group, get_relationship
from colanderalchemy import SQLAlchemySchemaNode
from sqlalchemy.orm.properties import ColumnProperty, RelationshipProperty
from sqlalchemy.orm.relationships import MANYTOONE, ONETOMANY, MANYTOMANY
from sqlalchemy.dialects.postgresql import JSON, JSONB, HSTORE

from .common import get_pk, get_column_param, _sa_row_to_choises
from .widgets import HiddenCheckboxWidget


class JSONType(colander.SchemaType):
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null

        return json.dumps(appstruct, indent=2, ensure_ascii=False)

    def deserialize(self, node, cstruct):
        if not cstruct:
            return colander.null

        try:
            return cstruct
        except Exception:
            raise colander.Invalid(
                node, '"{}" is not a valid JSON'.format(cstruct))


def property_values(dbsession, column):
    choices = dbsession.query(column.mapper).all()
    return [('', '-- Choose your option --')] + _sa_row_to_choises(choices)


def is_columntype(column, target):
    if hasattr(column, 'type') and isinstance(column.type, target):
        return True
    return False


def get_single_field_relatioships(table):
    relationships = get_relationship(table)
    return {list(rel.local_columns)[0]: rel for rel in relationships
            if len(rel.local_columns) == 1}


class SacrudForm(object):

    def __init__(self, dbsession, obj, table):
        self.dbsession = dbsession
        self.obj = obj
        self.table = table
        self.columns_by_group = columns_by_group(self.table)
        self.schema = colander.Schema()
        self.relationships = get_single_field_relatioships(self.table)

    def __call__(self, request=None):
        self.translate = request.localizer.translate if request else None
        appstruct = self.make_appstruct()
        form = deform.Form(self.schema)
        form.set_appstruct(appstruct)
        return form

    def make_appstruct(self):
        appstruct = {}
        for group_name, columns in self.columns_by_group:
            group = self.group_schema(group_name, columns)
            self.schema.add(group)
            appstruct = dict(
                list({group_name: group.dictify(self.obj)}.items()) +
                list(appstruct.items())
            )
        return appstruct

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

        def is_required_field(column):
            if all([col.nullable for col in column.local_columns]):
                return None
            return colander.required

        if column.direction is MANYTOONE:
            if relationship:
                default = get_pk(relationship)
            field = colander.SchemaNode(
                colander.String(),
                title=get_column_param(column, 'title', self.translate),
                description=get_column_param(column, 'description',
                                             self.translate),
                name=column.key + '[]',
                default=default,
                missing=is_required_field(column),
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
                title=get_column_param(column, 'title', self.translate),
                description=get_column_param(column, 'description',
                                             self.translate),
                name=column.key + '[]',
                default=selected,
                missing=None,
                widget=deform.widget.SelectWidget(
                    values=values,
                    multiple=True,
                    size="7",
                    css_class='browser-default'
                ),
            )
        return field

    def preprocessing(self, columns):
        new_column_list = []
        for class_member_name, column in columns:
            if hasattr(column, 'primary_key') and column.primary_key:
                relation = self.relationships.get(column, column)
                if hasattr(relation, 'direction') \
                        and relation.direction == MANYTOMANY:
                    columns.append((relation.key, relation))
            if hasattr(column, 'property'):
                column = column.property
            if isinstance(column, ColumnProperty):
                column = column.columns[0]

            try:
                column.info['colanderalchemy']
            except KeyError:
                column.info['colanderalchemy'] = {}

            # Check types
            if not isinstance(column, (Column, ColumnProperty,
                                       RelationshipProperty)):
                continue
            elif isinstance(column, RelationshipProperty):
                field = self.get_relationship_schemanode(column)
                new_column_list.append(field)
            elif is_columntype(column, (ChoiceType, Enum)):
                if is_columntype(column, Enum):
                    column.type.choices = zip(
                        column.type.enums, column.type.enums
                    )
                field = colander.SchemaNode(
                    colander.String(),
                    title=get_column_param(column, 'title', self.translate),
                    description=get_column_param(column, 'description',
                                                 self.translate),
                    name=column.key,
                    missing=None,
                    widget=deform.widget.SelectWidget(
                        values=column.type.choices,
                    ),
                )
                new_column_list.append(field)
            elif is_columntype(column, (JSON, JSONB, HSTORE)):
                try:
                    column.info['colanderalchemy']['typ']
                except KeyError:
                    column.info['colanderalchemy']['typ'] = JSONType()
                try:
                    column.info['colanderalchemy']['widget']
                except KeyError:
                    column.info['colanderalchemy']['widget'] = \
                        deform.widget.TextAreaWidget()
                new_column_list.append(class_member_name)
            elif is_columntype(column, Boolean):
                field = colander.SchemaNode(
                    colander.Boolean(),
                    title=get_column_param(column, 'title',
                                           self.translate),
                    description=get_column_param(column, 'description',
                                                 self.translate),
                    name=column.key,
                    widget=HiddenCheckboxWidget(),
                    missing=None,
                )
                new_column_list.append(field)
            elif isinstance(column, (ColumnProperty, Column)):
                new_column_list.append(class_member_name)
        return new_column_list


def includeme(config):

    config.add_translation_dirs(
        'colander:locale',
        'deform:locale',
    )

    def translator(term):
        return get_localizer(get_current_request()).translate(term)

    deform_template_dir = resource_filename('deform', 'templates/')
    zpt_renderer = deform.ZPTRendererFactory(
        [deform_template_dir],
        translator=translator)
    deform.Form.set_default_renderer(zpt_renderer)

    config.add_static_view('sacrud_deform_static', 'sacrud_deform:static')
