import os
import tweepy

def post_to_x(text, url=""):
    """
    Posts the summarized text and url to X using API v2.
    Keys expected from environment variables (.env):
    X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
    """
    consumer_key = os.environ.get("X_API_KEY")
    consumer_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")
    
    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("Error: Twitter API credentials (X_API_KEY, etc.) are not fully set in environment variables.")
        return False
        
    try:
        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        
        # Format the tweet content: Text + Newline + URL
        tweet_content = f"{text}\n\n{url}".strip()
        
        response = client.create_tweet(text=tweet_content)
        print(f"Successfully posted to X: {response.data}")
        return True
        
    except tweepy.errors.TooManyRequests:
        print("Error: X API Rate Limit exceeded.")
        return False
    except tweepy.errors.Unauthorized:
        print("Error: Twitter Unauthorized. Please check your API keys.")
        return False
    except tweepy.errors.Forbidden:
        print("Error: Twitter Forbidden. Ensure the app has Read and Write permissions.")
        return False
    except Exception as e:
        print(f"Unknown Network or API Error posting to X: {e}")
        return False
