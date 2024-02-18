## Pytest GCS

This is a pytest plugin in similar vein to [pytest-postgres](https://github.com/ClearcodeHQ/pytest-postgresql) and [pytest-kafka](https://pypi.org/project/pytest-kafka/).

This would have been much more painful without [Mirakuru](https://github.com/ClearcodeHQ/mirakuru)
and [fake-gcs-server](https://github.com/fsouza/fake-gcs-server); this is a simple wrapper around
those tools.


### Setup

This tool requires you to have a copy of the `fake-gcs-server` binary somewhere on your path.


### Demo

```python
# conftest.py
from pytest_gcs.factories import client as gcs_client
from pytest_gcs.factories import proc as gcs_process

# Create a process and a local client that targets that process.
gcs_proc = gcs_process.gcs_proc()
gcslocal = gcs_client.gcslocal("gcs_proc")

# tests/test_gcs.py
from google.cloud import storage
from pytest_gcs.executor.process import GCSExecutor


def test_can_create_gcs_bucket(gcs_proc: GCSExecutor, gcslocal: storage.Client) -> None:
    """MVP to ensure everything works."""
    bucket = "test_base"
    gcslocal.create_bucket(bucket)
    buckets = [x.name for x in gcslocal.list_buckets()]

    assert bucket in buckets
```


### Contributing

PRs are accepted.

```sh
# Install the dependencies with:
pip install .[test]
# Install pre-commit hooks.
pre-commit install
# Validate everything passes.
pre-commit run --all
# Run the tests.
pytest tests/
```


### TODOs

* Implement the events outputs, `-event.bucket`, `-event.list`, etc.
