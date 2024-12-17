"""Tests main conftest file."""

import warnings
from pathlib import Path
from typing import Generator

import pytest

# import pytest_gcs.factories.noproc
import pytest_gcs.factories.client
import pytest_gcs.factories.proc

warnings.filterwarnings(
    "error",
    category=DeprecationWarning,
    module="(_pytest|pytest|google|path|mirakuru).*",
)

gcs_proc = pytest_gcs.factories.proc.gcs_proc()
gcslocal = pytest_gcs.factories.client.gcslocal("gcs_proc")

gcs_proc1 = pytest_gcs.factories.proc.gcs_proc()
gcslocal1 = pytest_gcs.factories.client.gcslocal("gcs_proc1")

gcs_proc2 = pytest_gcs.factories.proc.gcs_proc()
gcslocal2 = pytest_gcs.factories.client.gcslocal("gcs_proc2")


@pytest.fixture(scope="session")
def seeded_data(
    tmp_path_factory: pytest.TempPathFactory,
) -> Generator[Path, None, None]:
    """Create seeded data."""
    tmp_path = tmp_path_factory.mktemp("pytest-gcs-seeded")
    bucket_dir = tmp_path / "bucket"
    bucket_dir.mkdir()
    bucket_file = bucket_dir / "test"
    bucket_file.touch()
    yield tmp_path


gcs_proc_seeded = pytest_gcs.factories.proc.gcs_proc(data_fixture_name="seeded_data")
gcslocal_seeded = pytest_gcs.factories.client.gcslocal("gcs_proc_seeded")
