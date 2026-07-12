# dbt-impact-graph

A dependency-free CLI for analyzing simplified dbt model lineage and change impact.

## Quick start

```bash
python impact.py models.json --changed stg_orders
```

Model records declare a name, upstream `depends_on`, and test evidence. The analyzer returns downstream impact, a minimal rerun set, untested models, and isolated models.

## Test

```bash
python -m unittest discover -v
```

## License

MIT.
