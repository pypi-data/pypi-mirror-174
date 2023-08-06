import logging
import sys
import pdb
import os


def setup_custom_logger(name, log_level=logging.DEBUG, file_name="log_file"):

    if file_name:
        isExist = os.path.exists(file_name)
        if not isExist:
            os.makedirs(file_name, exist_ok=True)
        file_name = os.path.join(file_name + "\log_file.log")
        file = open(file_name, "a+")
        handler = logging.FileHandler(file_name)
    else:
        handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )
    log_level = log_level.lower()
    # pdb.set_trace()
    if log_level == "critical":
        log_level = logging.CRITICAL
    elif log_level == "debug":
        print("inside")
        log_level = logging.DEBUG
    elif log_level == "info":
        log_level = logging.INFO
    elif log_level == "warning":
        log_level = logging.WARNING

    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    print("log_level is ", log_level)
    logger.setLevel(log_level)
    logger.addHandler(handler)

    return logger
