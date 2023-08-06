#importing required packages
from datetime import datetime
import inspect
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler as crf
import json
import os

#Configuring the log file name
# Opening JSON file
DIR = os.path.dirname(__file__)
if not DIR:
    FILE_PATH = "main_config.json"
else:
    FILE_PATH = DIR + "/main_config.json"

with open(FILE_PATH, 'r') as readfile:
    main_config = json.load(readfile)

file_path= main_config["Log_Path"]
file_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
my_path = file_path + file_time

#defining the logger function and default log level is DEBUG
def customLogger(logLevel=logging.DEBUG):
    # Gets the name of the class / method from where this method is called
    loggerName = inspect.stack()[1][3]
    logger = logging.getLogger(loggerName)
    # By default, log all messages
    logger.setLevel(logLevel)

    #this line helps to generate multiple log files when the log file limit exceeds 20mb
    my_handler = crf("{0}.log".format(my_path), mode='a', maxBytes=20*1024*1024)
    my_handler.setLevel(logLevel)
    # %(name)s will display the class/function name from where it is logging
    formatter = logging.Formatter('%(asctime)s - %(name)s- %(levelname)s: %(message)s',
                                  datefmt='%m/%d/%Y %I:%M:%S %p')
    my_handler.setFormatter(formatter)
    logger.addHandler(my_handler)
    return logger