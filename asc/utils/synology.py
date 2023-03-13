import os
from pathlib import Path
from typing import Optional

from synology_api import filestation  # type: ignore

from ..types.platforms import Platforms
from .logger import Logger
from .set_up import load_env

SYNOLOGY_USER = load_env("SYNOLOGY_USER")
SYNOLOGY_PWD = load_env("SYNOLOGY_PWD")
SYNOLOGY_PORT = 5000
NAS_ENV = load_env("NAS_ENV")
SYNOLOGY_FOLDER = "epigen"


class FileStationManager(filestation.FileStation):
    """
    This class inherited `FileStation` of `synology_api` to connect Synology NAS
    """

    def __init__(self, platform: Platforms) -> None:
        self.platform = platform
        self.logger = Logger("Synology FileStation")
        super().__init__(
            ip_address="a-s-capital.synology.me",
            port=SYNOLOGY_PORT,
            username=SYNOLOGY_USER,
            password=SYNOLOGY_PWD,
            debug=False,
        )

    def upload_one(self, des: str, path: str) -> Optional[str]:
        self.upload_file(des, path)
        return path

    def upload_many_to_platform(
        self, paths: list[Path], subfolder: Optional[str] = None
    ) -> None:
        count = 0
        des = f"/{SYNOLOGY_FOLDER}/{self.platform}"
        if subfolder:
            des += f"/{subfolder}"

        self.logger.info(f"start uploading {len(paths)} file(s) to {des}...")
        for path in paths:
            if os.path.exists(path):
                self.logger.debug(f"start uploading {path}")
                response = self.upload_file(des, path)
                if response == "Upload Complete":
                    count += 1
                else:
                    self.logger.error(
                        f"failed to upload {path.resolve()} to {des}: {response}"
                    )
            else:
                self.logger.error(f"{path} doesn't exist")

        self.logger.info(f"uploaded {count} file(s) to {des}")
