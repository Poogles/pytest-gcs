import shutil
from pathlib import Path
from typing import Optional

from tempfile import TemporaryDirectory

from mirakuru import HTTPExecutor


class GCSExecutor(HTTPExecutor):
    def __init__(
        self,
        port: int = 12345,
        host: Optional[str] = None,
        filesystemroot: Optional[Path] = None,
        executable: Optional[Path] = None,
    ) -> None:
        if not filesystemroot:
            self._temp_dir = TemporaryDirectory()
            _filesystemroot = self._temp_dir.name
        else:
            _filesystemroot = str(filesystemroot)

        if not executable:
            possible_path = shutil.which("fake-gcs-server")
            if not possible_path:
                raise Exception("Unable to find `fake-gcs-server`")

            _executable = possible_path
        else:
            _executable = str(executable)

        command = [
            _executable,
            "-scheme",
            "http",
            "-port",
            str(port),
            "-filesystem-root",
            str(_filesystemroot),
        ]
        super().__init__(
            command, url=f"http://localhost:{port}", timeout=5, status="404"
        )

    def start(self) -> "GCSExecutor":
        super().start()
        return self
