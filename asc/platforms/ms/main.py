import json
import math
import pathlib
from pprint import pprint
from typing import Any

import browser_cookie3  # type: ignore
import requests

from .helpers import MSHelper


class MS(MSHelper):
    """
    Request json by getting oauth token
    """

    platform = "ms"

    def __init__(self):
        super().__init__()

    def user_validation(self) -> bool:
        self.cj = browser_cookie3.chrome()
        if not self.cj:
            return False
        return True

    def crawl_data(self) -> list[pathlib.Path]:
        raw_json: dict = {}
        for report_type_broker in self.report_types:
            payload = self.get_payload(report_type_broker=report_type_broker, size=10)
            self.logger.debug(payload)

            self.logger.debug(f"start request for total count ({report_type_broker})")
            res = requests.post(self.url, cookies=self.cj, json=payload)
            report_count = int(
                res.json()["searchAndCardResponse"]["rcsSearchResponse"]["sd"]["t"]
            )

            page_count = math.ceil(report_count / 50)
            self.logger.debug(f"report count : {report_count}")
            self.logger.debug(f"page count : {page_count}")
            raw_reports_json: list = []
            for page in range(page_count):
                page += 1
                self.logger.debug(f"requesting page {page}")
                page_payload = self.get_payload(report_type_broker, page=page, size=50)
                page_res = requests.post(self.url, cookies=self.cj, json=page_payload)
                raw_reports_json += page_res.json()["searchAndCardResponse"][
                    "rcsSearchResponse"
                ]["docs"]

            raw_json[report_type_broker] = raw_reports_json

        path = self.save_json(data=raw_json)
        return [path]

    def crawl_files(self) -> list[pathlib.Path]:
        return super().crawl_files()

    def callback(self) -> Any:
        return super().callback()
