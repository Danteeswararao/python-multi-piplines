import logging
from datetime import date

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('age_validation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def validate_age(birth_date):
    """
    Validate age based on date of birth.
    Returns True if age >= 18, False otherwise.
    """
    logger.info(f"Validating age for birth date: {birth_date}")
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    logger.info(f"Calculated age: {age}")
    is_valid = age >= 18
    logger.info(f"Age validation result: {'PASSED' if is_valid else 'FAILED'}")
    
    return is_valid

def main():
    logger.info("Starting age validation process")
    
    try:
        # Get date of birth from user
        logger.info("Requesting user input for date of birth")
        print("Enter your date of birth:")
        year = int(input("Year (YYYY): "))
        month = int(input("Month (MM): "))
        day = int(input("Day (DD): "))
        
        logger.info(f"User input received - Year: {year}, Month: {month}, Day: {day}")
        
        birth_date = date(year, month, day)
        logger.info(f"Birth date created successfully: {birth_date}")
        
        # Calculate and display age
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        print(f"Your age is: {age}")
        logger.info(f"Age displayed to user: {age}")
        
        # Validate age
        if not validate_age(birth_date):
            logger.warning(f"Access denied for user with age {age} (under 18)")
            print("Access denied: You must be 18 or older.")
            print("exit")
            return False
        else:
            logger.info(f"Access granted for user with age {age} (18 or older)")
            print("Access granted: You are 18 or older.")
            return True
            
    except ValueError as e:
        logger.error(f"ValueError occurred: {e}")
        print("Invalid date format. Please enter valid numbers.")
        return False
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    logger.info("Age validator script started")
    result = main()
    logger.info(f"Age validator script completed with result: {result}")
    logger.info("=" * 50)