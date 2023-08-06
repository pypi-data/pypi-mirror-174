import asyncio
import logging
import os

from uvicorn.logging import ColourizedFormatter

from hautils import ha_que


class DeQueHandler(logging.Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to a stream. Note that this class does not close the stream, as
    sys.stdout or sys.stderr may be used.
    """

    terminator = '\n'

    def __init__(self, que=None):
        """
        Initialize the handler.

        If stream is not specified, sys.stderr is used.
        """
        super().__init__()
        if que is None:
            que = ha_que
        self.que = que

    def emit(self, record):
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        try:
            stream = self.que
            # issue 35046: merged two stream.writes into one.
            stream.push(record.message)
            self.flush()
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)

    def setStream(self, stream):
        """
        Sets the StreamHandler's stream to the specified value,
        if it is different.

        Returns the old stream, if the stream was changed, or None
        if it wasn't.
        """
        if stream is self.que:
            result = None
        else:
            result = self.que
            self.acquire()
            try:
                self.flush()
                self.que = stream
            finally:
                self.release()
        return result

    def __repr__(self):
        level = logging.getLevelName(self.level)
        name = getattr(self.que, 'name', '')
        #  bpo-36015: name can be an int
        name = str(name)
        if name:
            name += ' '
        return '<%s %s(%s)>' % (self.__class__.__name__, name, level)


log_level = os.getenv("LOG_LEVEL", "INFO")
logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName(log_level))
standard = logging.StreamHandler()
standard.setLevel(logging.getLevelName(log_level))

formatter = ColourizedFormatter(fmt=(
    "%(levelprefix)-8s %(asctime)-15s - "
    "%(filename)10s:%(lineno)-3d - %(message)s"))

standard.setFormatter(formatter)
logger.addHandler(standard)
# deque_handler = DeQueHandler()
# logger.addHandler(deque_handler)
