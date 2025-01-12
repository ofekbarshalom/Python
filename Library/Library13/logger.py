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

    @staticmethod
    def log_decorator(success_message, fail_message):
        def decorator(func):
            def wrapper(*args, **kwargs):
                log = Logger.get_logger()
                try:
                    result = func(*args, **kwargs)
                    log.info(f"{success_message}")
                    return result
                except Exception:
                    log.error(f"{fail_message}")
                    return None
            return wrapper

        return decorator

    @staticmethod
    def log_search():
        def decorator(func):
            def wrapper(search_entry, search_type_combobox, table, *args, **kwargs):
                log = Logger.get_logger()
                query = search_entry.get()
                search_type = search_type_combobox.get()
                try:
                    result = func(search_entry, search_type_combobox, table, *args, **kwargs)
                    log.info(f"Search book '{query}' by {search_type} completed successfully")
                    return result
                except Exception:
                    log.error(f"Search book '{query}' by {search_type} completed fail")
                    raise

            return wrapper

        return decorator

    @staticmethod
    def log_with_param(success_message, fail_message):
        def decorator(func):
            def wrapper(*args, **kwargs):
                log = Logger.get_logger()

                # Get the parameter from kwargs (explicitly named 'param')
                param = kwargs.get("param", "Unknown")

                try:
                    result = func(*args, **kwargs)  # Call the wrapped function
                    log.info(success_message.format(param))  # Format success message with param
                    return result
                except Exception:
                    log.error(f"{fail_message.format(param)}")  # Format failure message with param
                    raise

            return wrapper

        return decorator
