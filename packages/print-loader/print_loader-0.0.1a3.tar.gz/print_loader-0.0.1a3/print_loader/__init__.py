# SPDX-FileCopyrightText: 2022-present abhishek-compro <abhishek.prasad@noorahealth.org>
#
# SPDX-License-Identifier: MIT

import io
import sys
import threading
from datetime import datetime, timedelta

CLEAR_LINE_ESCAPE_SEQUENCE = "\33[2K\r"


class printl:
    """Print with a indefinite loader

    Print a message with a loader and elapsed time

    Parameters
    ----------
    message : str
        Message to be printed while loading
    update_every : float  (default: 1)
        Update interval (in seconds) of loader.
        Set to 0 to disable updating the loader.
    loading_chars : list[str]  (default: [".", "..", "..."])
        List of string that will be displayed one by one per update while loading
    loading_fmt : str  (default: "({elapsed_time}) {message} {loading_char}")
        Format to be used while printing loading message
    done_fmt : str  (default: "({elapsed_time}) {message} ✓\n")
        Format to be used while printing done message
    print_func : Callable[[printl, bool], None]  (default: printl._print_win32 on MS Windows and printl._print_posix on rest)
        Use this function to print

    Examples
    --------

    >>> import time
    >>> with printl("sleeping"):
    ...     time.sleep(3)
    >>> with printl("sleeping", update_every=0):
    ...     time.sleep(3)
    >>> import requests
    >>> with printl("loading python.org", loading_chars=["－", "\",  "|", "/"], update_every=0.1):
    ...     response = requests.get("https://python.org")
    """

    def __init__(
        self,
        message: str,
        update_every: float = 1,
        loading_chars: list[str] = [".", "..", "..."],
        loading_fmt: str = "({elapsed_time}) {message} {loading_char}",
        done_fmt: str = "({elapsed_time}) {message} ✓",
        print_func=None,
    ):
        self.message = message
        self.loading_fmt = loading_fmt
        self.done_fmt = done_fmt
        self.start_time: datetime = None
        self.loading_chars = loading_chars
        if print_func is None:
            if sys.platform == "win32":
                self.print_func = printl._print_win32
            else:
                self.print_func = printl._print_posix
        else:
            self.print_func = print_func
        self.__counter = -1
        self.__last_msg_len = 0
        self.__update_every = update_every if update_every > 0 else 0
        self.__timer: threading.Timer = None
        self.__timer_lock = threading.Lock()

    def _print_win32(self, stop=False):
        if stop:
            msg = self.done_fmt.format(
                message=self.message, elapsed_time=self.elapsed_time_str()
            )
        else:
            msg = self.loading_fmt.format(
                message=self.message,
                elapsed_time=self.elapsed_time_str(),
                loading_char=self.next_loading_char(),
            )
        diff = self.__last_msg_len - len(msg)
        sys.stdout.write("\r" + msg + " " * diff + "\b" * diff)
        if stop:
            sys.stdout.write("\n")
        self.__last_msg_len = len(msg)
        sys.stdout.flush()

    def _print_posix(self, stop=False):
        sys.stdout.write(CLEAR_LINE_ESCAPE_SEQUENCE)
        if stop:
            sys.stdout.write(
                self.done_fmt.format(
                    message=self.message, elapsed_time=self.elapsed_time_str()
                )
                + "\n"
            )
        else:
            sys.stdout.write(
                self.loading_fmt.format(
                    message=self.message,
                    elapsed_time=self.elapsed_time_str(),
                    loading_char=self.next_loading_char(),
                )
            )
        sys.stdout.flush()

    def elapsed_time(self) -> timedelta:
        """Returns elapsed time as a timedelta type.
        Formula used is (now - start).
        To access start use .start_time"""
        return datetime.utcnow() - self.start_time

    def elapsed_time_str(self) -> str:
        """Returns elapsed time as a string in the "d hh mm ss.ss" format where:
        - d is days
        - hh is hours
        - mm is minutes
        - ss.ss is seconds to 2 digits of precision after decimal point
        """
        try:
            et = self.elapsed_time()
        except TypeError:
            return f"0d 00h 00m 00.00s"
        micros = et.microseconds // 10000
        secs = et.seconds % 60
        mins = et.seconds // 60
        hrs = et.seconds // 3600
        return f"{et.days}d {hrs:02}h {mins:02}m {secs:02}.{micros:0>2}s"

    def next_loading_char(self):
        """Switches to the next loading char and returns it.

        If it was the last loading char then it will cycle back to the first char in
        the list and return it.

        If loading_chars was set to be an empty list then an empty string will be
        returned.
        """
        if len(self.loading_chars) == 0:
            return ""
        self.__counter = (self.__counter + 1) % len(self.loading_chars)
        return self.loading_chars[self.__counter]

    def __print_loading_loop(self):
        """Start an indefinite loop using daemon timer thread to keep calling
        print_func(self) at update_every seconds.

        To stop this loop call __unset_timer method.
        """
        if self.__update_every <= 0:
            return

        with self.__timer_lock:
            self.print_func(self)

            self.__timer = threading.Timer(
                self.__update_every, self.__print_loading_loop
            )
            self.__timer.daemon = True  # join not needed
            self.__timer.start()

    def __unset_timer(self):
        """Stops the timer started by __print_loading_loop gracefully which basically
        pauses/stops the loading."""
        if self.__timer is None:
            return

        with self.__timer_lock:
            self.__timer.cancel()
            self.__timer = None

    def start(self):
        """Starts the loading and resets the start_time."""
        if self.__update_every > 0:
            self.__print_loading_loop()
        else:
            self.print_func(self)
        self.start_time = datetime.utcnow()

    def stop(self, clear=None):
        """Stops the loading and prints the done message specified by done_fmt."""
        self.__unset_timer()
        self.print_func(self, stop=True)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def __del__(self):
        self.__unset_timer()
