"""GCS process executor.

Starts a local GCS server using the targeted configuration.
"""

from pathlib import Path
from typing import List, Optional

from mirakuru import HTTPExecutor


class GCSExecutor(HTTPExecutor):
    """Local GCS executor."""

    def __init__(
        self,
        executable: Path,
        host: str,
        port: int,
        filesystemroot: Path,
        data: Optional[Path] = None,
        corsheaders: Optional[List[str]] = None,
        externalurl: Optional[str] = None,
        loglevel: Optional[str] = None,
    ) -> None:
        """Start up local GCS.

        Args:
            executable: executable to call.
            host: host address fixture will be started on.
            port: port fixture will listen on.
            filesystemroot: path to on local file system fixture will
                use as local storage.
            corsheaders: allowed cors headers.
            externalurl: location header in returned URLs.
            loglevel: log level passed to `fake-gcs-server` binary.

        Returns:
            None
        """
        command = [
            str(executable),
            "-scheme",
            "http",
            "-port",
            str(port),
            "-filesystem-root",
            str(filesystemroot),
        ]

        if data:
            command.extend(["-data", str(data)])

        if corsheaders:
            command.extend(["-cors-headers", ",".join(corsheaders)])

        if externalurl:
            command.extend(["-external-url", externalurl])

        if loglevel:
            command.extend(["-log-level", loglevel])

        self._starting_command = command
        self.executable = executable

        super().__init__(
            command, url=f"http://localhost:{port}", timeout=5, status="404"
        )

    def start(self) -> "GCSExecutor":
        """Start the GCS executor."""
        super().start()
        return self
