"""Tests main conftest file."""

import warnings

# import pytest_gcs.factories.noproc
import pytest_gcs.factories.client
import pytest_gcs.factories.proc

warnings.filterwarnings(
    "error",
    category=DeprecationWarning,
    module="(_pytest|pytest|redis|path|mirakuru).*",
)

gcs_proc = pytest_gcs.factories.proc.gcs_proc()
gcslocal = pytest_gcs.factories.client.gcslocal("gcs_proc")

gcs_proc1 = pytest_gcs.factories.proc.gcs_proc()
gcslocal1 = pytest_gcs.factories.client.gcslocal("gcs_proc1")

gcs_proc2 = pytest_gcs.factories.proc.gcs_proc()
gcslocal2 = pytest_gcs.factories.client.gcslocal("gcs_proc2")
