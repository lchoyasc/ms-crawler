import pathlib
import shutil
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Any, Optional

from ..types.platforms import Platforms
from ..utils.database import get_last_report_datetime
from ..utils.helpers import (
    delete_cookies_cache,
    get_cookies_cache,
    get_date_delta,
    get_from_date,
    put_cookies_cache,
)
from ..utils.logger import Logger
from ..utils.set_up import load_env
from ..utils.synology import FileStationManager

PLATFORM_DISPLAY_NAME = {
    "ms": "Morgan Stanley",
}


class Crawler(ABC):
    """
    helper class that provides a standard way to create an platform crawler using inheritance
    """

    def __init__(self):
        self.platform  # check if properties are defined in sub-class
        self.validated = False  # default not validated
        self.data_paths = []
        self.file_paths = []

        # create necessary class variable
        self.display_name = self.platform
        try:
            self.display_name = PLATFORM_DISPLAY_NAME[self.platform]
        except:
            pass

        self.platform_dir = pathlib.Path(load_env("LOCAL_DATA_PATH")).joinpath(
            self.platform
        )
        self.platform_dir.mkdir(parents=True, exist_ok=True)

        self.latest_report_dt = get_last_report_datetime(self.platform)

        # initiate logger
        self.logger = Logger(self.display_name)
        # initiate file station manager
        self.synology = FileStationManager(self.platform)

    @property
    def platform(self) -> Platforms:
        raise NotImplementedError

    @abstractmethod
    def user_validation(self) -> bool:
        """
        validate user from crawling site

        return `boolean` to update the class attribute `validated`
        """
        return False

    @abstractmethod
    def crawl_data(self) -> list[pathlib.Path]:
        """
        crawl programmatic data and save in data exchange format e.g. JSON, CSV

        return `list` of `pathlib.Path` to update class attribute `data_paths`
        """
        return []

    @abstractmethod
    def crawl_files(self) -> list[pathlib.Path]:
        """
        crawl reports and save in raw/readable format e.g. HTML, PDF

        return a `list` of `pathlib.Path` to update class attribute `file_paths`
        """
        return []

    @abstractmethod
    def callback(self) -> Any:
        """
        callback function to run after crawling
        """
        pass

    def get_cookies_cache(self) -> Optional[dict]:
        return get_cookies_cache(self.platform)

    def put_cookies_cache(self, cookies: dict) -> bool:
        return put_cookies_cache(cookies, self.platform)

    def delete_cookies_cache(self) -> bool:
        return delete_cookies_cache(self.platform)

    def set_latest_report_dt(self, dt: datetime) -> None:
        self.latest_report_dt = dt

    def get_from_date(self, day: int = 1) -> date:
        """
        return `datetime.date` of date n-1 of the latest report
        """
        return get_from_date(self.latest_report_dt, day)

    def get_date_delta(self, day: int = 1) -> int:
        """
        return number of days
        """
        return get_date_delta(self.latest_report_dt, day)

    def upload_to_synology(self) -> None:
        """
        upload crawled files to Synology NAS to root level of platform folder

        override if necessary e.g. uploading to subfolder
        """
        paths = []
        paths += self.data_paths
        paths += self.file_paths
        self.synology.upload_many_to_platform(paths)

    def crawl(
        self,
        replace_paths: bool = True,
        upload: bool = True,
        remove: bool = True,
    ) -> None:
        """
        main function to start crawling

        params:
        - replace_paths: `boolean` - replace class attribute `data_paths` and `file_paths` after crawling, default `True`
        - upload: `boolean` - upload paths to Synology NAS after crawling, default `True`
        - remove: `boolean` - remove files in local platform folder after upload, default `True`
        """
        self.logger.info(f"start crawling {self.display_name}...")
        # validate user
        if not self.validated:
            self.validated = self.user_validation()

        if not self.validated:
            self.logger.critical("CRAWLING ENDED - FAILED TO AUTHENTICATE USER")
            return

        # crawl
        data_paths = self.crawl_data()
        self.data_paths = data_paths if replace_paths else self.data_paths + data_paths

        file_paths = self.crawl_files()
        self.file_paths = file_paths if replace_paths else self.file_paths + file_paths

        all_paths = data_paths + file_paths
        self.logger.info(f"created {len(all_paths)} files")

        # upload
        if upload:
            self.upload_to_synology()

        # remove local files
        if remove:
            shutil.rmtree(self.platform_dir)

        self.callback()
        self.logger.info("end crawling")
