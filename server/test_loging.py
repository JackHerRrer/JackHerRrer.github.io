import logging
import os
from systemd.journal import JournalHandler

# Define module logger
logger = logging.getLogger(__name__)
# Initially set to log all - change this in production
logger.setLevel(logging.DEBUG)

# Create journal logger
journalHandler = JournalHandler(SYSLOG_IDENTIFIER='my_app_name')

# create formatter - can also use %(lineno)d -
# see https://stackoverflow.com/questions/533048/how-to-log-source-file-name-and-line-number-in-python/44401529
# formatter = logging.Formatter(
#     '%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s | %(filename)s > %(module)s > %(funcName)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )

# # add formatter to jh
# journalHandler.setFormatter(formatter)

# add jh to logger
logger.addHandler(journalHandler)


# logger.setLevel(logging.INFO)

logger.info("test log")