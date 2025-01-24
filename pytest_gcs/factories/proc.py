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
    data: Optional[str] = None,
    data_fixture_name: Optional[str] = None,
    corsheaders: Optional[List[str]] = None,
    externalurl: Optional[str] = None,
    loglevel: Optional[str] = None,
) -> Callable[[FixtureRequest, TempPathFactory], Generator[GCSExecutor, None, None]]:
    """Creates a pytest fixture for managing a fake GCS (Google Cloud Storage) server.

        This function returns a pytest fixture that sets up a `GCSExecutor` instance
        for testing purposes. It ensures that the fake GCS server is properly configured, 
        started before tests run, and shut down afterward.

        Args:
            executable: Path to the fake GCS server executable. Defaults to the
                value from pytest-gcs config.
            host: The host address to bind the server to. Defaults to config.
            port: The port for the GCS server. If not provided, an available
                port is selected.
            filesystemroot: The root directory for GCS storage. Defaults to a
                temporary directory.
            data: Path to the initial dataset file. Defaults to config.
            data_fixture_name: Name of another fixture that provides the dataset
                file path. Defaults to config.
            corsheaders: List of CORS headers allowed by the server. Defaults to
                config.
            externalurl: External URL the server should be reachable at.
                Defaults to config.
            loglevel: Logging level for the server. Defaults to config.

        Returns:
            A pytest fixture that, when used, provides a running `GCSExecutor` instance.

        Example:
            ```python
            @pytest.fixture
            def gcs_instance(gcs_proc):
                yield from gcs_proc()
            ```
        """


    @pytest.fixture(scope="session")
    def gcs_proc_fixture(
        request: FixtureRequest,
        tmp_path_factory: TempPathFactory,
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

        if data_fixture_name:
            data_path = request.getfixturevalue(data_fixture_name)
        elif data:
            data_path = Path(data)
        else:
            data_path = Path(config["data"])

        gcs_executor = GCSExecutor(
            executable=Path(gcs_exec),
            port=gcs_port,
            host=host or config["host"],
            filesystemroot=_filesystemroot,
            data=data_path,
            corsheaders=corsheaders or config["corsheaders"],
            externalurl=externalurl or config["externalurl"],
            loglevel=loglevel or config["loglevel"],
        )
        with gcs_executor:
            yield gcs_executor

    return gcs_proc_fixture
