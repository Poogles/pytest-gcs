from shutil import which

from pytest import Parser

import pytest_gcs.factories.client
import pytest_gcs.factories.proc

_HELP_EXEC = "Exec file to target."
_HELP_HOST = "Host to run GCS service on."
_HELP_PORT = "Port to run GCS service on."
_HELP_FILESYSTEMROOT = "File system path buckets will be stored/created at."
_HELP_CORSHEADERS = "Comma separated list of headers to add to the CORS allowlist."
_HELP_EXTERNALURL = (
    "Optional external URL, returned in the Location header for uploads."
    " Defaults to local address."
)
_HELP_LOGLEVEL = (
    "Level for bucket logging. level for logging. Options"
    " same as for logrus: trace, debug, info, warn, error, fatal, and panic"
)


def pytest_addoption(parser: Parser) -> None:
    """Plugin configuration options."""
    parser.addini(
        name="gcs_executable", help=_HELP_EXEC, default=which("fake-gcs-server")
    )
    parser.addini(name="gcs_host", help=_HELP_HOST, default="127.0.0.1")
    parser.addini(name="gcs_port", help=_HELP_PORT)
    parser.addini(name="gcs_filesystemroot", help=_HELP_FILESYSTEMROOT)
    parser.addini(name="gcs_corsheaders", help=_HELP_CORSHEADERS)
    parser.addini(name="gcs_externalurl", help=_HELP_EXTERNALURL)
    parser.addini(name="gcs_loglevel", help=_HELP_LOGLEVEL)

    parser.addoption(
        "--gcs-executable", action="store", dest="gcs_executable", help=_HELP_EXEC
    )
    parser.addoption("--gcs-host", action="store", dest="gcs_host", help=_HELP_HOST)
    parser.addoption("--gcs-port", action="store", dest="gcs_port", help=_HELP_PORT)
    parser.addoption(
        "--gcs-filesystemroot",
        action="store",
        dest="gcs_filesystemroot",
        help=_HELP_FILESYSTEMROOT,
    )
    parser.addoption(
        "--gcs-corsheaders",
        action="store",
        dest="gcs_corsheaders",
        help=_HELP_CORSHEADERS,
    )
    parser.addoption(
        "--gcs-externalurl",
        action="store",
        dest="gcs_externalurl",
        help=_HELP_EXTERNALURL,
    )
    parser.addoption(
        "--gcs-loglevel", action="store", dest="gcs_loglevel", help=_HELP_LOGLEVEL
    )


gcs_proc = pytest_gcs.factories.proc.gcs_proc()
gcslocal = pytest_gcs.factories.client.gcslocal("gcs_proc")
