"""
Logging utility for the BurnAI API.
"""
import os
import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logging(name: str = "burnai_api", log_level: str = "INFO") -> logging.Logger:
    """
    Set up logging for the application.
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent.parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Create a logger
    logger = logging.getLogger(name)
    
    # Set the logging level
    level = getattr(logging, log_level.upper())
    logger.setLevel(level)
    
    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Create a file handler for the log file
    log_file = logs_dir / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    
    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 