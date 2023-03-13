import os
import pickle
from datetime import date, datetime, timedelta
from typing import Optional

from ..types.platforms import Platforms


def get_from_date(dt: datetime, day: int) -> date:
    # minus 1 day to include hours, minutes in time difference
    return (dt - timedelta(days=day)).date()


def get_date_delta(dt: datetime, day: int) -> int:
    # calculate how many days of reports should be downlaoded
    time_diff = datetime.now() - dt
    # add 1 to include hours, minutes in time difference
    return time_diff.days + day


def _get_cookies_file_path(platform: Platforms) -> str:
    return f"./.cache/{platform}_cookies.pkl"


def get_cookies_cache(platform: Platforms) -> Optional[dict]:
    try:
        return pickle.load(open(_get_cookies_file_path(platform), "rb"))
    except:
        return None


def put_cookies_cache(cookies: dict, platform: Platforms) -> bool:
    if not os.path.exists("./.cache"):
        os.mkdir("./.cache")
    try:
        pickle.dump(cookies, open(_get_cookies_file_path(platform), "wb"))
        return True
    except:
        return False


def delete_cookies_cache(platform: Platforms) -> bool:
    if os.path.exists(_get_cookies_file_path(platform=platform)):
        os.remove(_get_cookies_file_path(platform=platform))
        return True
    return False
