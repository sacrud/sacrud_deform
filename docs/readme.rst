|Build Status| |Coverage Status| |Stories in Progress| |PyPI|

.. |Build Status| image:: https://travis-ci.org/ITCase/sacrud_deform.svg?branch=master
   :target: https://travis-ci.org/ITCase/sacrud_deform
.. |Coverage Status| image:: https://coveralls.io/repos/ITCase/sacrud_deform/badge.png?branch=master
   :target: https://coveralls.io/r/ITCase/sacrud_deform?branch=master
.. |Stories in Progress| image:: https://badge.waffle.io/ITCase/sacrud_deform.png?label=in%20progress&title=In%20Progress
   :target: http://waffle.io/ITCase/sacrud_defrom
.. |PyPI| image:: http://img.shields.io/pypi/dm/sacrud_deform.svg
   :target: https://pypi.python.org/pypi/sacrud_deform/

sacrud_deform
==============

Form generotor for SQLAlchemy models.

Install
=======

develop version from source

.. code-block:: bash

  pip install git+git://github.com/ITCase/sacrud_deform@develop

from pypi

.. code-block:: bash

  pip install sacrud_deform

Use
===

For get column of model use sacrud function :py:func:`sacrud.common.columns_by_group`.

.. code-block:: python

        columns_of_model = columns_by_group(MyModel)
        data, js_list = form_generator(dbsession=DBSession,
                                       obj=obj_of_model,
                                       table=MyModel,
                                       columns_by_group=columns_of_model,
                                       request=self.request)
        form = data.render()

Support and Development
=======================

To report bugs, use the `issue tracker <https://github.com/ITCase/sacrud_deform/issues>`_
or `waffle board <https://waffle.io/ITCase/sacrud_deform>`_.

We welcome any contribution: suggestions, ideas, commits with new futures, bug fixes, refactoring, docs, tests, translations etc

If you have question, contact me sacrud@uralbash.ru or IRC channel #sacrud
