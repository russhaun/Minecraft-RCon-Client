import logging

def mylogger(name, filename):
    file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(funcName)s~%(message)s')
    #console_formatter = logging.Formatter('%(asctime)s~%(levelname)s -- %(message)s')
    console_formatter = logging.Formatter('%(asctime)s - %(message)s')
    
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    
    return logger