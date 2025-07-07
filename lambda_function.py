from dotenv import load_dotenv
import os

# load key-value pairs from .env into environment
load_dotenv()

def lambda_handler(event=None, context=None):
    username = os.getenv("AMSTERDAM_USERNAME")
    password = os.getenv("AMSTERDAM_PASSWORD")
    
    print("Username:", username)
    print("Password:", password)
    
    return {
        "statusCode": 200,
        "body": f"Credentials loaded for user {username}"
    }
    
# run locally for testing
if __name__ == "__main__":
    lambda_handler()