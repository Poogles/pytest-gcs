from typing import Callable, Generator, Optional, Union

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.tmpdir import TempPathFactory

from port_for import get_port

from pytest_gcs.executor import GCSExecutor


def gcs_proc(
    executable: Optional[str] = None,
    timeout: Optional[int] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    datadir: Optional[str] = None,
) -> Callable[[FixtureRequest, TempPathFactory], Generator[GCSExecutor, None, None]]:
    """Fixture factory for pytest-gcs."""

    @pytest.fixture(scope="session")
    def gcs_proc_fixture(
        request: FixtureRequest, tmp_path_factory: TempPathFactory
    ) -> Generator[GCSExecutor, None, None]:
        """Fixture for pytest-gcs.

        #. Get configs.
        #. Run gcs process.
        #. Stop gcs process after tests.

        :param request: fixture request object
        :param tmpdir_factory:
        :rtype: pytest_gcs.executors.TCPExecutor
        :returns: tcp executor
        """

        gcs_port = get_port(port) if port else get_port(None)
        assert gcs_port
        gcs_executor = GCSExecutor(port=gcs_port)
        with gcs_executor:
            yield gcs_executor

    return gcs_proc_fixture
