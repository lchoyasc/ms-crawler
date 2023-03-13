from datetime import datetime, timedelta

from pymongo import MongoClient
from pymongo.collection import Collection

from ..types.platforms import Platforms
from .logger import Logger
from .set_up import load_env

DB_USER = load_env("DB_USER")
DB_PWD = load_env("DB_PWD")
NAS_ENV = load_env("NAS_ENV")
MONGO_PORT = "7001" if NAS_ENV == "PROD" else "7000"
MONGO_URI = f"mongodb://{DB_USER}:{DB_PWD}@a-s-capital.synology.me:{MONGO_PORT}/"


def get_report_collection(platform: Platforms) -> Collection:
    """Get platforms raw reports collection from the MongoDB database"""
    mongo_client: MongoClient = MongoClient(MONGO_URI)
    collection = mongo_client["reports"][platform]
    return collection


def get_last_report_datetime(platform: Platforms) -> datetime:
    """
    get the latest publish_datetime in HKT from platform's reports in the database
    """
    logger = Logger("MongoDB")

    logger.debug(f"getting datetime of lastest {platform} report from the database")
    collection = get_report_collection(platform)
    query_result = collection.find(
        sort=[("publish_datetime", -1)], projection=["publish_datetime"], limit=1
    )
    result_list = [report for report in query_result]
    if result_list:
        last_report_datetime_utc = result_list[0]["publish_datetime"]
        last_report_datetime_hkt = last_report_datetime_utc + timedelta(hours=8)
    else:
        # return a default date for new reports sources
        logger.info(f"no matching report in the database '{collection.full_name}'")
        return datetime(2021, 1, 1)

    logger.debug(f"lastest {platform} report at {last_report_datetime_hkt} (HKT)")
    return last_report_datetime_hkt


def is_report_scraped(platform: Platforms, uid: str) -> bool:
    collection = get_report_collection(platform)
    doc = collection.find_one({"uid": uid})

    if doc:
        return True
    return False


if __name__ == "__main__":
    a = get_last_report_datetime("gs")
    print(a)
