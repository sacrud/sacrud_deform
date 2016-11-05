|Build Status| |Coverage Status|

.. |Build Status| image:: https://travis-ci.org/sacrud/sacrud_deform.svg?branch=master
   :target: https://travis-ci.org/sacrud/sacrud_deform
.. |Coverage Status| image:: https://coveralls.io/repos/sacrud/sacrud_deform/badge.png?branch=master
   :target: https://coveralls.io/r/sacrud/sacrud_deform?branch=master

sacrud_deform
=============

Form generotor for SQLAlchemy models.

Install
=======

develop version from source

.. code-block:: bash

  pip install git+https://github.com/sacrud/sacrud_deform.git


.. code-block:: bash

  pip install sacrud_deform

Use
===

.. code-block:: python

    from sacrud_deform import SacrudForm

    form = SacrudForm(obj=obj,
                      dbsession=DBSession,
                      request=request,
                      table=MyModel)
    form_html = form().render()

Support and Development
=======================

To report bugs, use the `issue tracker
<https://github.com/sacrud/sacrud_deform/issues>`_.

We welcome any contribution: suggestions, ideas, commits with new
futures, bug fixes, refactoring, docs, tests, translations etc.

If you have question, contact me sacrud@uralbash.ru or IRC channel #sacrud
