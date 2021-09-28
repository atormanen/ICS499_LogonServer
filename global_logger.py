import logging

VERBOSE = 15
verbose_level = 'VERBOSE'
logPath = './logs'
fileName = 'logon_server.log'

log_formatter = logging.Formatter("%(levelname)-7.7s %(threadName)-12.12s %(asctime)s: %(message)s")
logger = logging.getLogger()
logging.addLevelName(VERBOSE, verbose_level)

# file_handler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
file_handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", "./logs/logon_server.log"))
file_handler.setFormatter(log_formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

#logger.setLevel(logging.INFO)
#logger.setLevel(verbose_level)
logger.setLevel(logging.DEBUG)
