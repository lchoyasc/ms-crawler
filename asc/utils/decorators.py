import _thread as thread
import threading

from .logger import Logger


def exit_after(seconds):
    """
    use as decorator to exit process if function takes longer than s seconds
    """
    logger = Logger()

    def outer(fn):
        def inner(*args, **kwargs):
            success = True
            timer = threading.Timer(seconds, quit_function, args=[fn.__name__, seconds])
            timer.start()
            while success:
                try:
                    result = fn(*args, **kwargs)
                    success = False
                    logger.debug("success")
                finally:
                    timer.cancel()
                logger.debug("exiting...")
            return result

        return inner

    return outer


def quit_function(fn_name, seconds):
    """
    Used to end the function if it took too long too long
    """
    logger = Logger()
    # print to stderr, unbuffered in Python 2.
    logger.info("{0} took more than {1}".format(fn_name, seconds))
    thread.interrupt_main()  # raises KeyboardInterrupt
