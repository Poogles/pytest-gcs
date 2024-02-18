"""GCS process factory."""
from pathlib import Path
from typing import Callable, Generator, List, Optional

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.tmpdir import TempPathFactory
from port_for import get_port

from pytest_gcs.config import get_config
from pytest_gcs.executor import GCSExecutor


def gcs_proc(
    executable: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    filesystemroot: Optional[Path] = None,
    corsheaders: Optional[List[str]] = None,
    externalurl: Optional[str] = None,
    loglevel: Optional[str] = None,
) -> Callable[[FixtureRequest, TempPathFactory], Generator[GCSExecutor, None, None]]:
    """Fixture factory for pytest-gcs."""

    @pytest.fixture(scope="session")
    def gcs_proc_fixture(
        request: FixtureRequest, tmp_path_factory: TempPathFactory
    ) -> Generator[GCSExecutor, None, None]:
        """Fixture for pytest-gcs.

        This fixture:
        * Get configs.
        * Run gcs process.
        * Stop gcs process after tests runs and does any cleanup.

        Args:
            request: Request fixture we're targeting.
            tmp_path_factory: Temporary directory fixture.

        Yields:
            Configured and active GCSExecutor.
        """
        config = get_config(request)
        gcs_exec = executable or config["executable"]

        assert gcs_exec, "Unable to find a fake-gcs-server exec."

        if filesystemroot:
            _filesystemroot = filesystemroot
        elif config["filesystemroot"]:
            _filesystemroot = Path(config["filesystemroot"])
        else:
            _filesystemroot = tmp_path_factory.mktemp(
                f"pytest-gcs-{request.fixturename}"
            )

        gcs_port = (
            get_port(port) if port else get_port(config["port"]) or get_port(None)
        )
        assert gcs_port, "Unable to find a port available."

        gcs_executor = GCSExecutor(
            executable=Path(gcs_exec),
            port=gcs_port,
            host=host or config["host"],
            filesystemroot=_filesystemroot,
            corsheaders=corsheaders or config["corsheaders"],
            externalurl=externalurl or config["externalurl"],
            loglevel=loglevel or config["loglevel"],
        )
        with gcs_executor:
            yield gcs_executor

    return gcs_proc_fixture
