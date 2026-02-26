import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

def test_twitter_post():
    consumer_key = os.environ.get("X_API_KEY")
    consumer_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")
    
    # 1. Test Client V2 setup
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    
    print("Testing API V2 Text Post...")
    try:
        response = client.create_tweet(text="Test post from local script")
        print(f"Success! Tweet ID: {response.data['id']}")
    except tweepy.errors.Forbidden as e:
        print(f"\n[403 FORBIDDEN ERROR DETAILS V2]")
        print(f"API Response messages: {e.api_messages}")
        print(f"API Response errors: {e.api_errors}")
        print(f"API Response codes: {e.api_codes}")
        print(f"Raw string: {e}")
    except Exception as e:
        print(f"Other Error: {e}")

if __name__ == "__main__":
    test_twitter_post()