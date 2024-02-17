import pytest_gcs.factories.proc
import pytest_gcs.factories.client

gcs_proc = pytest_gcs.factories.proc.gcs_proc()
gcslocal = pytest_gcs.factories.client.gcslocal("gcs_proc")
