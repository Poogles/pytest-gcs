"""GCS client fixture factory."""

from typing import Callable, Generator

import pytest
from _pytest.fixtures import FixtureRequest
from google.auth.credentials import AnonymousCredentials
from google.cloud import storage

from pytest_gcs.executor import GCSExecutor


def gcslocal(
    process_fixture_name: str,
) -> Callable[[FixtureRequest], Generator[storage.Client, None, None]]:
    """Create connection fixture factory for pytest-gcs.

    Args:
        process_fixture_name: Name of fixture to load client on.

    Returns:
        Local GCS client factory.
    """

    @pytest.fixture(scope="session")
    def gcslocal_factory(
        request: FixtureRequest,
    ) -> Generator[storage.Client, None, None]:
        """Create connection for pytest-gcs.

        1. Load GCS fixture.
        2. Create a new local client that targets the fixture.

        Args:
            request: pytest request fixture.

        Yields:
            GCS client configured for test fixture.
        """
        proc_fixture: GCSExecutor = request.getfixturevalue(process_fixture_name)

        gcs_host = proc_fixture.host
        gcs_port = proc_fixture.port
        endpoint = f"http://{gcs_host}:{gcs_port}"

        gcs_client = storage.Client(
            credentials=AnonymousCredentials(),
            project="testing123",
            client_options={"api_endpoint": f"{endpoint}"},
        )

        yield gcs_client

    return gcslocal_factory
