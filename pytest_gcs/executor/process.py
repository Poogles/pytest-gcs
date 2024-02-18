from pathlib import Path
from typing import List, Optional

from mirakuru import HTTPExecutor


class GCSExecutor(HTTPExecutor):
    def __init__(
        self,
        executable: Path,
        host: str,
        port: int,
        filesystemroot: Path,
        corsheaders: Optional[List[str]] = None,
        externalurl: Optional[str] = None,
        loglevel: Optional[str] = None,
    ) -> None:
        command = [
            str(executable),
            "-scheme",
            "http",
            "-port",
            str(port),
            "-filesystem-root",
            str(filesystemroot),
        ]

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
        super().start()
        return self
