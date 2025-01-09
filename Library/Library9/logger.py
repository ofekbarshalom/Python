import logging
from path import Paths

class Logger:
    _log = None

    @staticmethod
    def get_logger():
        if Logger._log is None:
            # Setup the logger
            Logger._log = logging.getLogger("SystemLogger")
            Logger._log.setLevel(logging.DEBUG)  # Set the logging level (DEBUG, INFO, etc.)

            # Create a file handler to save logs to a file
            file_handler = logging.FileHandler(Paths.LOGGER.value)
            file_handler.setLevel(logging.DEBUG)

            # Create a formatter for logs
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)

            # Add handlers to the logger
            Logger._log.addHandler(file_handler)

        return Logger._log
