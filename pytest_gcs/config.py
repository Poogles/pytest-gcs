"""Config loading helpers."""

from typing import Any, Optional, TypedDict, List

from _pytest.fixtures import FixtureRequest


class GcsConfigType(TypedDict):
    """pytest-gcs config definition type."""

    executable: str
    port: Optional[int]
    host: str
    filesystemroot: str
    corsheaders: List[str]
    externalurl: str
    loglevel: str


def get_config(request: FixtureRequest) -> GcsConfigType:
    """Return a dictionary with config options."""

    def get_conf_option(option: str) -> Any:
        option_name = "gcs_" + option
        return request.config.getoption(option_name) or request.config.getini(
            option_name
        )

    port = get_conf_option("port")
    config: GcsConfigType = {
        "executable": get_conf_option("executable"),
        "port": int(port) if port else None,
        "host": get_conf_option("host"),
        "filesystemroot": get_conf_option("filesystemroot"),
        "corsheaders": get_conf_option("corsheaders"),
        "externalurl": get_conf_option("externalurl"),
        "loglevel": get_conf_option("loglevel"),
    }
    return config
