#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
import os
from deform.widget import TextInputWidget, TextAreaWidget, CheckboxWidget

cur_path = os.path.dirname(os.path.realpath(__file__))
deform_path = os.path.join(cur_path, 'templates', 'deform')


class ElfinderWidget(TextInputWidget):
    template = 'sacrud_deform:templates/deform/Elfinder.pt'


class HstoreWidget(TextAreaWidget):
    template = 'sacrud_deform:templates/deform/Hstore.pt'


class SlugWidget(TextInputWidget):
    template = 'sacrud_deform:templates/deform/Slug.pt'


class HiddenCheckboxWidget(CheckboxWidget):
    template = 'sacrud_deform:templates/deform/HiddenCheckbox.pt'


class M2MWidget(CheckboxWidget):
    template = 'sacrud_deform:templates/deform/Many2Many.pt'
