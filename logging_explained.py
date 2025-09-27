"""
Python Logging Functions Explained
This script demonstrates various logging concepts and functions
"""

import logging
import sys
from datetime import datetime

def basic_logging_example():
    """Demonstrates basic logging setup and usage"""
    print("\n=== BASIC LOGGING EXAMPLE ===")
    
    # Basic configuration
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Get a logger
    logger = logging.getLogger('basic_example')
    
    # Different log levels
    logger.debug("This is a DEBUG message - detailed info for diagnosing problems")
    logger.info("This is an INFO message - general information about program execution")
    logger.warning("This is a WARNING message - something unexpected happened")
    logger.error("This is an ERROR message - a serious problem occurred")
    logger.critical("This is a CRITICAL message - program may not be able to continue")

def advanced_logging_setup():
    """Demonstrates advanced logging configuration"""
    print("\n=== ADVANCED LOGGING SETUP ===")
    
    # Create custom logger
    logger = logging.getLogger('advanced_example')
    logger.setLevel(logging.DEBUG)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s'
    )
    simple_formatter = logging.Formatter('%(levelname)s: %(message)s')
    
    # File handler
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(simple_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Test the logger
    logger.debug("Debug message - only goes to file")
    logger.info("Info message - only goes to file")
    logger.warning("Warning message - goes to both file and console")
    logger.error("Error message - goes to both file and console")
    
    return logger

def logging_with_exceptions():
    """Demonstrates logging exceptions and stack traces"""
    print("\n=== LOGGING WITH EXCEPTIONS ===")
    
    logger = logging.getLogger('exception_example')
    
    try:
        # Intentionally cause an error
        result = 10 / 0
    except ZeroDivisionError as e:
        # Log the exception with stack trace
        logger.error("Division by zero occurred", exc_info=True)
        logger.exception("This also logs the exception with stack trace")
        
    try:
        # Another error example
        my_list = [1, 2, 3]
        value = my_list[10]
    except IndexError:
        logger.error("List index out of range", exc_info=True)

def custom_log_levels():
    """Demonstrates creating custom log levels"""
    print("\n=== CUSTOM LOG LEVELS ===")
    
    # Add custom log level
    TRACE_LEVEL = 5
    logging.addLevelName(TRACE_LEVEL, "TRACE")
    
    def trace(self, message, *args, **kwargs):
        if self.isEnabledFor(TRACE_LEVEL):
            self._log(TRACE_LEVEL, message, args, **kwargs)
    
    # Add trace method to Logger class
    logging.Logger.trace = trace
    
    logger = logging.getLogger('custom_level')
    logger.setLevel(TRACE_LEVEL)
    
    # Create handler for custom level
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(handler)
    
    logger.trace("This is a TRACE level message")
    logger.debug("This is a DEBUG level message")
    logger.info("This is an INFO level message")

def logging_best_practices():
    """Demonstrates logging best practices"""
    print("\n=== LOGGING BEST PRACTICES ===")
    
    logger = logging.getLogger('best_practices')
    
    # 1. Use appropriate log levels
    def process_user_data(user_id, data):
        logger.info(f"Processing data for user {user_id}")
        
        if not data:
            logger.warning(f"No data provided for user {user_id}")
            return False
            
        try:
            # Simulate processing
            processed_count = len(data)
            logger.info(f"Successfully processed {processed_count} items for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to process data for user {user_id}: {e}")
            return False
    
    # 2. Use string formatting efficiently
    user_id = 12345
    items = ['item1', 'item2', 'item3']
    
    # Good: Lazy evaluation
    logger.debug("User %s has %d items", user_id, len(items))
    
    # Also good: f-strings (Python 3.6+)
    logger.info(f"Processing {len(items)} items for user {user_id}")
    
    # 3. Don't log sensitive information
    password = "secret123"
    logger.info(f"User login attempt for user {user_id}")  # Don't log password!
    
    # Test the function
    process_user_data(user_id, items)
    process_user_data(user_id, [])

def structured_logging():
    """Demonstrates structured logging with extra fields"""
    print("\n=== STRUCTURED LOGGING ===")
    
    # Custom formatter for structured logs
    class StructuredFormatter(logging.Formatter):
        def format(self, record):
            # Add custom fields to log record
            if hasattr(record, 'user_id'):
                record.msg = f"[User:{record.user_id}] {record.msg}"
            if hasattr(record, 'request_id'):
                record.msg = f"[Req:{record.request_id}] {record.msg}"
            return super().format(record)
    
    logger = logging.getLogger('structured')
    handler = logging.StreamHandler()
    handler.setFormatter(StructuredFormatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # Log with extra context
    logger.info("User logged in", extra={'user_id': 123, 'request_id': 'abc-def'})
    logger.warning("Invalid request", extra={'user_id': 456, 'request_id': 'xyz-789'})

def main():
    """Main function to run all logging examples"""
    print("Python Logging Functions Explained")
    print("=" * 50)
    
    # Run all examples
    basic_logging_example()
    advanced_logger = advanced_logging_setup()
    logging_with_exceptions()
    custom_log_levels()
    logging_best_practices()
    structured_logging()
    
    print("\n=== LOGGING LEVELS HIERARCHY ===")
    print("CRITICAL (50) - Most severe")
    print("ERROR    (40) - Error occurred")
    print("WARNING  (30) - Something unexpected")
    print("INFO     (20) - General information")
    print("DEBUG    (10) - Detailed diagnostic info")
    print("NOTSET   (0)  - All messages")
    
    print("\n=== KEY LOGGING FUNCTIONS ===")
    print("logging.basicConfig() - Basic logging setup")
    print("logging.getLogger()   - Get/create logger instance")
    print("logger.setLevel()     - Set minimum log level")
    print("logger.addHandler()   - Add output handler")
    print("logger.debug/info/warning/error/critical() - Log messages")
    print("logger.exception()    - Log exception with traceback")
    
    print(f"\nCheck 'app.log' file for detailed logs created at {datetime.now()}")

if __name__ == "__main__":
    main()