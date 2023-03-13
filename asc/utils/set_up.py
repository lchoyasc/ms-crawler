import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()


def load_env(key: str) -> Any:
    """
    - return value of variable from .env file
    - raise ImportError if key is not found
    """
    try:
        value = os.environ[key]
    except KeyError as e:
        m = f"{e} not found in .env file"
        raise ImportError(m)

    # check path validity, mkdir if necessary
    if key == "LOCAL_DATA_PATH":
        return _check_path(value)

    # check if NAS env is either PROD or DEV
    if key == "NAS_ENV":
        if value in ["PROD", "DEV"]:
            return value
        else:
            m = f"{value} is not a valid value for environment variable NAS_ENV (PROD or DEV)"
            raise ImportError(m)

    return value


def _check_path(path: str) -> str:
    """
    - check if path is a dir, return path if so
    - create dir, fallback to ./data is failed to create dir
    """
    if os.path.isdir(path):
        return path

    try:
        os.mkdir(path)
        return path
    except Exception as e:
        os.mkdir("./data")
        return "./data"
