import logging
import pathlib
import sys
from typing import Literal, Optional

from colorlog import ColoredFormatter

from ..utils.set_up import load_env


class Logger(logging.Logger):
    def __init__(
        self, name: str = "Unnamed", verbosity: Optional[Literal[1, 2, 3]] = None
    ):
        """
        params
        - name: `str` - name of the logger
        - verbosity: `1,2,3` - controls the level of details of the logged messages on stdout

        found this little description on Stack Overflow and I think it's quite useful, please log the messages accordingly

        debug: A quirky message only developers care about
        info: Curious users might want to know this
        warn: Something is wrong and any user should be informed
        error: Serious stuff, this is red for a reason
        critical: OH NO everything is on fire
        """
        super().__init__(name)
        self.verbosity = verbosity
        if self.verbosity is None:
            try:
                # ignoring type check as env VERBOSITY is check on arg parser
                VERBOSITY: Literal[1, 2, 3] = int(load_env("VERBOSITY"))  # type: ignore
                self.verbosity = VERBOSITY
            except:
                self.verbosity = 1
        self.log_dir = pathlib.Path(load_env("LOCAL_DATA_PATH")).joinpath("log")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir.joinpath("logger.log")

        self.add_console_handler()
        self.add_file_handler()

    def add_console_handler(self) -> None:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        LOGFORMAT = "[%(name)s] - %(levelname)s - %(message)s"
        formatter = ColoredFormatter(LOGFORMAT)
        if self.verbosity == 1:
            LOGFORMAT = "%(log_color)s[%(name)s] %(message)s%(reset)s"
            formatter = ColoredFormatter(
                LOGFORMAT,
                log_colors={
                    "INFO": "white",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            )
        elif self.verbosity == 2:
            console_handler.setLevel(logging.NOTSET)
            LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s[%(name)s] %(message)s%(reset)s"
            formatter = ColoredFormatter(LOGFORMAT)
        elif self.verbosity == 3:
            console_handler.setLevel(logging.NOTSET)
            line1 = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(pathname)s line:%(lineno)d %(funcName)s()%(reset)s"
            line2 = "           | %(log_color)s%(asctime)s%(reset)s"
            line3 = "           | %(log_color)s[%(name)s] %(message)s%(reset)s"
            LOGFORMAT = f"{line1}\n{line2}\n{line3}"
            formatter = ColoredFormatter(LOGFORMAT)
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

    def add_file_handler(self) -> None:
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        LOGFORMAT = logging.Formatter(
            "%(asctime)s %(levelname)-8s | [%(name)s] %(message)s"
        )
        file_handler.setFormatter(LOGFORMAT)
        self.addHandler(file_handler)
