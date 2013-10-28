import logging
import os

logger = None

def init_logging():
    global logger
    if logger is not None:
        return
    formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
    logger = logging.getLogger()

    this_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    log_file = os.path.join(this_dir, 'em.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    #logger.setLevel(logging.INFO)

#init_logging()
