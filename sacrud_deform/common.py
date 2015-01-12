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
import json
from gettext import gettext as _

from sacrud.common import pk_to_list


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


def get_column_param(col, name, translate=_):
    if 'colanderalchemy' in col.info and name in col.info['colanderalchemy']:
        name = col.info['colanderalchemy'][name]
    elif name == 'title':
        name = getattr(col, 'name', col.key)
    else:
        name = ''
    return translate(name)


def get_column_description(col):
    if 'description' in col.info:
        return HTMLText(col.info['description'])
    return None
