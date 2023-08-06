.. _install:

Installation
============

pglift can be installed from PyPI.

First, it is recommended to use a dedicated virtualenv:
::

    $ python3 -m venv .venv
    $ . .venv/bin/activate
    (.venv) $ pip install 'pip>=20.3'

then proceed with actual installation as:
::

    (.venv) $ pip install pglift

The :ref:`Ansible <tutorial_ansible>` collection is not shipped with the
Python package, so follow the :doc:`development setup <../dev>` to use the
Ansible interface.

.. note::
   If usage of systemd as service manager and/or scheduler is planned,
   additional steps might be needed, see :ref:`detailed systemd installation
   instructions <systemd_install>`.

Once installed, the ``pglift`` command should be available:

::

    $ pglift
    Usage: pglift [OPTIONS] COMMAND [ARGS]...

      Deploy production-ready instances of PostgreSQL

    Options:
      --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
      --help                          Show this message and exit.

    Commands:
      database  Manipulate databases
      instance  Manipulate instances
      role      Manipulate roles

Runtime dependencies
--------------------

pglift operates PostgreSQL and a number of satellite components, each
available as independent software packages. Thus, depending of selected
components (see :ref:`site settings <settings>`), the following packages might
be needed:

- ``postgresql``
- ``pgbackrest``
- ``prometheus-postgres-exporter``
- ``powa`` (with ``pg_qualstats`` and ``pg_stat_kcache``)
