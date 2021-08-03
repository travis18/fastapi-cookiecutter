import sys
import logbook
from logbook import StreamHandler
# , ERROR, NOTICE, INFO, DEBUG, LoggerGroup, lookup_level, LogRecord
from logbook.more import ColorizingStreamHandlerMixin
from app.core.config import settings

logbook.set_datetime_format("local")

class ColorizedStreamHandler(ColorizingStreamHandlerMixin, StreamHandler):
    """A colorizing stream handler that writes to stdout.  It will only
    colorize if a terminal was detected.  Note that this handler does
    not colorize on Windows systems.

    .. versionadded:: 0.3
    .. versionchanged:: 1.0
       Added Windows support if `colorama`_ is installed.

    .. _`colorama`: https://pypi.org/pypi/colorama
    """
    def __init__(self, *args, **kwargs):
        StreamHandler.__init__(self, *args, **kwargs)
        # self.force_color()
        
    def get_color(self, record):
        """Returns the color for this record."""
        if record.level >= logbook.ERROR:
          return 'red'
        elif record.level >= logbook.NOTICE:
          return 'yellow'
        elif record.level >= logbook.INFO:
          return 'green'
        elif record.level >= logbook.DEBUG:
          return 'darkblue'
        return 'lightgray'
      
logger_group = logbook.LoggerGroup(level=logbook.lookup_level(settings.LOGMODE))

basicstream_handler = ColorizedStreamHandler(sys.stdout, level=logbook.lookup_level(settings.LOGMODE))

def default_formatter(record:logbook.LogRecord, handler):
  basic = f"[{record.time}][{record.level_name}] {record.channel}: {record.message} "
  for ex in record.extra:
    basic += f"[{ex}:{record.extra[ex]}]"
  return basic

basicstream_handler.formatter = default_formatter

basicstream_handler.push_application()