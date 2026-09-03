import sys

from loguru import logger

logger.remove()

logger.add(
    sink="logs/all_texts/{time:YYYY-MM-DD}.log",
    level="INFO",
    rotation="1 day",
    retention="3 days",
    format="time: {time:YYYY-MM-DD HH:mm:ss}, "
           "level: {level}, "
           "message: {message}",
)

logger.add(
    sink="logs/errors/{time:YYYY-MM-DD}.log",
    level="ERROR",
    rotation="1 day",
    retention="5 days",
    format="time: {time:YYYY-MM-DD HH:mm:ss}, "
           "level: {level}, "
           "message: {message}",
)

logger.add(
    sink=sys.stdout,
    level="ERROR",
    format="<red>time: {time:YYYY-MM-DD HH:mm:ss}, "
           "level: {level}, "
           "<underline>message: "
           "{message}</underline></red>",
    colorize=True
)
