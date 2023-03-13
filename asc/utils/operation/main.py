import argparse
import os
import signal
from functools import wraps
from multiprocessing import Pool

from ...platforms import *
from ...types.platforms import Platforms

STOP = False
PLATFORMS = {
    "ms": MS,
}


def parse_args():
    parser = argparse.ArgumentParser(
        prog="python -m main",
        description="ASC Platform Crawler",
        epilog="",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        help="verbosity level",
        type=int,
        default=1,
        choices=range(1, 4),  # 1, 2, 3
        required=False,
    )
    parser.add_argument(
        "-u",
        "--upload",
        help="upload downloaded files to NAS",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-rm",
        "--remove",
        help="remove downloaded files",
        action=argparse.BooleanOptionalAction,
    )
    args = parser.parse_args()

    os.environ["VERBOSITY"] = str(args.verbosity)

    os.environ["UPLOAD"] = str(False)
    if args.upload:
        os.environ["UPLOAD"] = str(True)

    os.environ["REMOVE"] = str(False)
    if args.remove:
        os.environ["REMOVE"] = str(True)

    return args


def handle_keyboard_interrupt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global ctrl_c_entered
        if not ctrl_c_entered:
            signal.signal(signal.SIGINT, default_sigint_handler)  # the default
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                ctrl_c_entered = True
                return KeyboardInterrupt()
            finally:
                signal.signal(signal.SIGINT, pool_ctrl_c_handler)
        else:
            return KeyboardInterrupt()

    return wrapper


@handle_keyboard_interrupt
def work(platform):
    remove = eval(os.environ["REMOVE"])
    upload = eval(os.environ["UPLOAD"])

    PLATFORMS[platform]().crawl(remove=remove, upload=upload)


def pool_ctrl_c_handler(*args, **kwargs):
    global ctrl_c_entered
    ctrl_c_entered = True


def init_pool():
    # set global variable for each process in the pool:
    global ctrl_c_entered
    global default_sigint_handler
    ctrl_c_entered = False
    default_sigint_handler = signal.signal(signal.SIGINT, pool_ctrl_c_handler)


def crawl(platforms: list[Platforms]):
    parse_args()

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    thread = 4

    cpu_count = os.cpu_count()
    if cpu_count:
        thread = int(cpu_count / 2)

    if thread > 4:
        thread = 4

    pool = Pool(thread, initializer=init_pool)

    results = pool.map(work, platforms)
    if any(map(lambda x: isinstance(x, KeyboardInterrupt), results)):
        print("Ctrl+C pressed. Stopping...")

    pool.close()
    pool.join()
