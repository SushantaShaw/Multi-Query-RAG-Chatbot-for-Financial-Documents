import logging

def setup_logger(name="rag-logger", log_file="rag-app.log", level=logging.INFO):
    """Function to setup a logger."""
    
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create a file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    
    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add the handlers to the logger
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger