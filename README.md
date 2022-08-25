# uniq-ch

A Python library for counting distinct elements in a stream,
using [ClickHouse uniq][ClickHouseRefUniq] data structure.

This uses [BJKST][BarYossef+02], a probabilistic algorithm that relies on
adaptive sampling and provides fast, accurate and deterministic results.
Two BJKSTs can be merged, making the data structure well suited for map-reduce
settings.

[Repository] | [Documentation]

[ClickHouseRefUniq]: https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/uniq/
[BarYossef+02]: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.12.6276
[Repository]: https://github.com/vivienm/python-uniq-ch
[Documentation]: https://vivienm.github.io/python-uniq-ch/
