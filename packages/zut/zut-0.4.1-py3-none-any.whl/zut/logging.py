from __future__ import annotations
import logging, os, sys, atexit
from copy import copy
from . import colors


class ColorFormatter(logging.Formatter):
    def __init__(self, fmt: str = None, **kwargs):
        if isinstance(fmt, str):
            if "[%(name)s]" in fmt:
                fmt = fmt.replace("[%(name)s]", colors.FOREGROUND_GRAY % "[%(name)s]")
            elif "%(name)s" in fmt:
                fmt = fmt.replace("%(name)s", colors.FOREGROUND_GRAY % "[%(name)s]")
        
        super().__init__(fmt, **kwargs)

    def getColorFormat(self, level: int):
        if level == logging.DEBUG:
            return colors.FOREGROUND_GRAY
        elif level == logging.INFO:
            return colors.FOREGROUND_BLUE
        elif level == logging.WARNING:
            return colors.FOREGROUND_YELLOW
        elif level == logging.ERROR:
            return colors.FOREGROUND_RED
        elif level == logging.CRITICAL:
            return colors.BACKGROUND_RED
        else:
            return "%s"
    
    def formatMessage(self, record: logging.LogRecord):
        # make a copy so that other handlers (e.g. file handlers) do not get color escape characters
        colorRecord = copy(record)
        colorRecord.levelname = self.getColorFormat(colorRecord.levelno) % colorRecord.levelname
        return super().formatMessage(colorRecord)


class CountHandler(logging.Handler):
    def __init__(self, level=logging.WARNING, formatter: logging.Formatter = None):
        self.colorFormatter = formatter if isinstance(formatter, ColorFormatter) else None
        self.counts: dict[int, int] = {}
        atexit.register(self.print_counts)
        super().__init__(level=level)

    def print_counts(self):
        msg = ""

        levelnos = sorted(self.counts.keys(), reverse=True)
        for levelno in levelnos:
            levelname = logging.getLevelName(levelno)
            colorfmt = self.colorFormatter.getColorFormat(levelno) if self.colorFormatter else "%s"
            msg += (", " if msg else "") + colorfmt % levelname + ": %d" % self.counts[levelno]

        if msg:
            print("Logged " + msg)

    def emit(self, record: logging.LogRecord):
        if record.levelno >= self.level:
            if not record.levelno in self.counts:
                self.counts[record.levelno] = 1
            else:
                self.counts[record.levelno] += 1


def configure_logging(level=None, format=None, filename=None, filelevel=None, fileformat=None, nocount=False, nocolor=False):
    if level is None:
        level = logging.getLevelName(os.environ.get("LOGLEVEL", "INFO").upper())

    if filename is None:
        if "LOGFILE" in os.environ:
            filename = os.environ.get("LOGFILE")

    if filename and filelevel is None:
        if "LOGFILELEVEL" in os.environ:
            filelevel = logging.getLevelName(os.environ["LOGFILELEVEL"].upper())

    if format is None:
        format = "%(levelname)s [%(name)s] %(message)s"

    if fileformat is None:
        fileformat = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    elif fileformat is False:
        fileformat = format

    # Add console handler
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)
    formatter = logging.Formatter(format) if nocolor else ColorFormatter(format)
    handler.setFormatter(formatter)
    handlers = [handler]
    
    if filename:
        # Add file handler
        handler = logging.FileHandler(filename)
        handler.setLevel(filelevel if filelevel else level)
        handler.setFormatter(logging.Formatter(fileformat))
        handlers.append(handler)

    if not nocount:
        # Add count handler
        handlers.append(CountHandler(formatter=formatter))
    
    logging.basicConfig(level=min(level, filelevel) if filelevel else level, handlers=handlers)
