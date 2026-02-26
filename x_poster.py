import os
import tweepy

def post_to_x(text, url="", image_path=None):
    """
    Posts the text and url/image to X.
    Uses API v1.1 to upload media (if any), then uses API v2 to post the tweet.
    """
    consumer_key = os.environ.get("X_API_KEY")
    consumer_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")
    
    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("Error: Twitter API credentials (X_API_KEY, etc.) are not fully set in environment variables.")
        return False
        
    try:
        # Client for API v2 operations (Posting Tweets)
        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        
        # Format the tweet content
        tweet_content = text
        if url:
             tweet_content = f"{text}\n\n{url}"
        
        # Handle Media Upload if an image is provided
        media_ids = None
        if image_path and os.path.exists(image_path):
            # API v1.1 for media upload
            auth = tweepy.OAuth1UserHandler(
                consumer_key, consumer_secret, access_token, access_token_secret
            )
            api = tweepy.API(auth)
            
            print(f"Uploading media: {image_path}")
            media = api.media_upload(image_path)
            media_ids = [media.media_id]
        
        # Post the tweet (with or without media)
        if media_ids:
            response = client.create_tweet(text=tweet_content.strip(), media_ids=media_ids)
        else:
            response = client.create_tweet(text=tweet_content.strip())
            
        print(f"Successfully posted to X: {response.data}")
        return True
        
    except tweepy.errors.TooManyRequests:
        print("Error: X API Rate Limit exceeded.")
        return False
    except tweepy.errors.Unauthorized:
        print("Error: Twitter Unauthorized. Please check your API keys.")
        return False
    except tweepy.errors.Forbidden as e:
        print(f"\n[403 FORBIDDEN ERROR DETAILS V2]")
        print(f"API Response messages: {e.api_messages}")
        print(f"API Response errors: {e.api_errors}")
        print(f"API Response codes: {e.api_codes}")
        print(f"Raw string: {e}")
        # This usually means Tweet is too long, duplicate content, or permissions issue
        return False
    except Exception as e:
        print(f"Unknown Network or API Error posting to X: {e}")
        return False
