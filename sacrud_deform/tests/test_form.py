#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
test models of sacrud_pages
"""

import unittest

import colander
import deform
import sqlalchemy
from sqlalchemy import Column, create_engine, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sacrud_deform import (_get_column_type_by_sa_type,
                           _get_widget_type_by_sa_type, GroupShema, HTMLText)

Base = declarative_base()


class MyModel(Base):
    __tablename__ = "mymodel"

    pk = Column('id', Integer, primary_key=True)
    title = Column(Unicode)


def add_fixture(model, fixtures, session):
    """
    Add fixtures to database.

    Example::

    hashes = ({'foo': {'foo': 'bar', '1': '2'}}, {'foo': {'test': 'data'}})
    add_fixture(TestHSTORE, hashes)
    """
    for fixture in fixtures:
        session.add(model(**fixture))


def add_mptt_pages(session):
    pages = (
        {'pk': '1', },
        {'pk': '2', },
        {'pk': '3', },
        {'pk': '4', },
        {'pk': '5', },
        {'pk': '6', },
        {'pk': '7', },
        {'pk': '8', },
        {'pk': '9', },
        {'pk': '10', },
        {'pk': '11', },

        {'pk': '12', },
        {'pk': '13', },
        {'pk': '14', },
        {'pk': '15', },
        {'pk': '16', },
        {'pk': '17', },
        {'pk': '18', },
        {'pk': '19', },
        {'pk': '20', },
        {'pk': '21', },
        {'pk': '22', },
    )
    add_fixture(MyModel, pages, session)
    session.commit()


class TestFormBase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        MyModel.__table__.create(self.engine)
        self.session.commit()
        add_mptt_pages(self.session)

    def tearDown(self):
        self.session.close()


class TestForm(TestFormBase):

    def test_tree_initialize(self):
        self.assertEqual([(x+1,) for x in range(22)],
                         self.session.query(MyModel.pk).all())

    def test_column_type_by_sa_type(self):
        column_type = _get_column_type_by_sa_type(Integer)
        self.assertEqual(column_type, colander.Integer)

    def test_widget_type_by_sa_type(self):
        widget_type = _get_widget_type_by_sa_type(Integer)
        self.assertEqual(widget_type, deform.widget.TextInputWidget)

    def test_html_text(self):
        text = HTMLText(u"<hr />Вселенная в Опастносте!")
        self.assertEqual(text.__html__(),
                         u"<hr />Вселенная в Опастносте!")


class TestFormGroupShema(TestFormBase):

    def _init_gs(self):
        return GroupShema("My Group name", self.table, None, self.session)

    def setUp(self):
        super(TestFormGroupShema, self).setUp()
        self.columns = MyModel.__table__.columns
        self.table = MyModel
        relations = sqlalchemy.inspect(MyModel).relationships
        self.relationships = [rel for rel in relations]

    def test_group_shema_init(self):
        gs = GroupShema("My Group name", self.table, None, self.session)
        self.assertEqual(gs.obj, None)
        self.assertEqual(gs.table, self.table)
        self.assertEqual(gs.relationships, self.relationships)
        self.assertEqual(gs.dbsession, self.session)
        self.assertEqual(gs.js_list, [])

    def test_get_column_title(self):
        gs = self._init_gs()
        col = MyModel.__table__.c.title
        title = gs.get_column_title(col)
        self.assertEqual(title, 'title')

        col.info['verbose_name'] = 'foo'
        title = gs.get_column_title(col)
        self.assertEqual(title, 'foo')

        col.info['sacrud_position'] = 'inline'
        title = gs.get_column_title(col)
        self.assertEqual(title, 'foo')

        del col.info['verbose_name']
        col.sacrud_name = 'bar'
        title = gs.get_column_title(col)
        self.assertEqual(title, 'bar')

    def test_get_column_description(self):
        gs = self._init_gs()
        col = MyModel.__table__.c.title
        description = gs.get_column_description(col)
        self.assertEqual(description, None)

        col.info['description'] = 'foo <hr />'
        description = gs.get_column_description(col)
        self.assertEqual(description.__html__(), 'foo <hr />')

    def test_get_column_css_styles(self):
        gs = self._init_gs()
        col = MyModel.__table__.c.title

        css = gs.get_column_css_styles(col)
        self.assertEqual(css, None)
