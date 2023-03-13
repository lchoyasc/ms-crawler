import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from ...platforms.base import Crawler
from ...utils.database import is_report_scraped
from ...utils.set_up import load_env

URL = "https://ny.matrix.ms.com/eqr/research/webapp/rlservices/search/v3/composite.json"
REPORT_TYPES = [
    "Change in Recommendation/Volatility",
    "Change in Price Target",
    "Assumption of Coverage",
    "Change in Earnings Forecast",
    "Company News Analysis",
    "Company Update",
    "EarningsPreview",
    "Event",
    "Initiation of Coverage",
    "Resumption of Coverage",
    "SurveyAnalysisAndResults",
    "PortfolioStrategy",
]


class MSHelper(Crawler):
    """
    helper class for Kepler inherited from base class `Crawler`
    """

    def __init__(self) -> None:
        super().__init__()
        self.url: str = URL
        self.report_types: list[str] = REPORT_TYPES
        # self.pwd = load_env("KC_PWD")
        # self.token = ""

    def get_payload(self, report_type_broker="Assumption of Coverage", page=1, size=50):
        start_date = self.get_from_date().strftime("%d/%m/%Y")
        end_date = datetime.now().strftime("%d/%m/%Y")
        return {
            "search": f"(researchtype==Equity);(region==Europe,region==North America,region==Asia Pacific,region==Japan);(subject=={report_type_broker});date==custom={start_date}..{end_date}",
            "sort": "d",
            "noSearch": False,
            "gn": False,
            "didyoumean": False,
            "lang": "en",
            "prefLang": "en",
            "countMode": "best",
            "showcard": False,
            "queryID": "f532-4b7e-f61a-7e4b-5fa7",
            "size": size,
            "page": page,
        }

    def save_json(self, data: dict) -> Path:
        filemame = (
            f'{datetime.now().isoformat().replace(":", "").replace(".", "_")}.json'
        )
        filepath = self.platform_dir.joinpath(filemame)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
            f.close()

        self.logger.debug(f"created {filepath.resolve()}")
        return filepath
