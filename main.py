from datetime import datetime

from asc.platforms import MS
from asc.types.platforms import Platforms
from asc.utils import operation

platforms: list[Platforms] = [
    "ms",
]


def main():
    # operation.crawl(platforms=platforms)
    ms = MS()
    ms.set_latest_report_dt(dt=datetime(2023, 2, 1))
    ms.crawl()


if __name__ == "__main__":
    main()
