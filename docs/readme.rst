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

.. code-block:: python

        data = form_generator(dbsession=DBSession,
                                   obj=obj_of_model, table=MyModel,
                                   columns=columns_of_model)
        form, js_list = data.render()
