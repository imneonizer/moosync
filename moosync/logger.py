import logging
from logging.handlers import RotatingFileHandler

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "/tmp/gsp.log",
                    filemode = "w",
                    format = Log_Format, 
                    level = logging.INFO)
logger = logging.getLogger()