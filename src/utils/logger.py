import logging
import sys
import os
from typing import Optional

class ScannerLogger:
    """
    Custom logger setup that handles both console output and file rotation.
    """
    
    @staticmethod
    def setup_logger(name: str = "NetSentry", log_file: Optional[str] = None, level: str = "INFO") -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
        
        # Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File Handler
        if log_file:
            # Ensure directory exists
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            fh = logging.FileHandler(log_file)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            
        return logger
