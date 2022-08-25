uniq-ch
=======

A Python library for counting distinct elements in a stream,
using `ClickHouse uniq <ClickHouseRefUniq_>`_ data structure.

This uses `BJKST <BarYossef+02_>`_, a probabilistic algorithm that relies on
adaptive sampling and provides fast, accurate and deterministic results.
Two BJKSTs can be merged, making the data structure well suited for map-reduce
settings.

Repository_

.. _ClickHouseRefUniq: https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/uniq/
.. _BarYossef+02: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.12.6276
.. _Repository: https://github.com/vivienm/python-uniq-ch


API reference
-------------

.. currentmodule:: uniq_ch

.. autoclass:: uniq_ch.BJKST
   :members:
   :undoc-members:
   :special-members: __bool__, __ior__, __len__, __or__


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
