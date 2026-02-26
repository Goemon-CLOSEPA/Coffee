import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

def test_twitter_post():
    consumer_key = os.environ.get("X_API_KEY")
    consumer_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")
    
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    
    text_content = "Barista Magazineはナパバレーで初のビジネス教育イベント「Camp Coffee Shop」を4日間開催する。現役および将来のコーヒーショップオーナーが対象である。\n\nこのイベントは、カフェ経営の専門知識需要の高まりを示唆する。ロースター・トレーダー視点では、顧客であるカフェの事業安定化が市場全体の品質向上と長期的な成長基盤を強化する可能性がある。"
    url = "https://dailycoffeenews.com/2026/02/25/barista-magazine-hosting-camp-coffee-shop-in-napa/"
    
    payloads_to_test = [
        ("Full text with URL", f"{text_content}\n\n{url}"),
        ("Text only, no URL", text_content),
        ("Very short text with URL", f"テスト投稿です。\n\n{url}")
    ]
    
    for desc, payload in payloads_to_test:
        print(f"\n--- Testing: {desc} ---")
        try:
            response = client.create_tweet(text=payload)
            print(f"Success! Tweet ID: {response.data['id']}")
            # Since we just want to know what triggers it, we can break on success
            # But let's test all just in case (though it might hit duplicate tweet if it's identical to something else? No, these are unique enough for now, except maybe Twitter will block multiple tests. Actually let's just do one test and return)
            return
        except tweepy.errors.Forbidden as e:
            print(f"403 Forbidden.")
        except Exception as e:
            print(f"Other Error: {e}")

if __name__ == "__main__":
    test_twitter_post()