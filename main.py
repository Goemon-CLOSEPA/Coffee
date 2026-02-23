import os
from dotenv import load_dotenv
from news_fetcher import fetch_latest_news
from history_manager import is_posted, save_to_history
from summarizer import summarize_article
from x_poster import post_to_x

# Load environment variables
load_dotenv()

def main():
    print("Starting Coffee & Crypto X Bot...")
    
    # 1. Fetch news
    print("Fetching latest news...")
    try:
        articles_data = fetch_latest_news()
    except Exception as e:
        print(f"Critical error fetching news: {e}")
        return

    # 2. Filter out already posted articles for each category
    unposted = {
        "main": [a for a in articles_data["main"] if not is_posted(a['link'])],
        "sub":  [a for a in articles_data["sub"] if not is_posted(a['link'])]
    }
    
    # 3. Apply Quotas: Select EXACTLY 1 article per execution. 
    # Prioritize 'main' (English) over 'sub' (Japanese).
    target_article = None
    if unposted["main"]:
        target_article = unposted["main"][0]
        print(f"Selected 1 unposted article from 'main' (English source).")
    elif unposted["sub"]:
        target_article = unposted["sub"][0]
        print(f"Selected 1 unposted article from 'sub' (Japanese source).")
    else:
        print("No new articles to post in this run.")
        return
        
    # 4. Process the single article
    print(f"\n--- Processing Article ---")
    print(f"Title: {target_article['title']}")
    print(f"Category: {target_article['category']}")
    
    # Summarize with Gemini
    print("Summarizing with Gemini...")
    try:
        summary_text = summarize_article(target_article['title'], target_article['summary'], target_article['category'])
    except Exception as e:
        print(f"Error during summarization: {e}.")
        return
        
    if not summary_text:
        print("Failed to generate summary.")
        return
        
    print(f"\n[Generated Summary]\n{summary_text}\n{target_article['link']}\n")
    
    # Post to X
    print("Posting to X...")
    if os.environ.get("DRY_RUN", "false").lower() == "true":
        print("DRY_RUN is enabled. Skipping actual post to X.")
        success = True
    else:
        try:
            success = post_to_x(summary_text, target_article['link'])
        except Exception as e:
            print(f"Error during posting to X: {e}")
            success = False
    
    # Save to history if successful
    if success:
        save_to_history(target_article['link'])
        print("Successfully recorded URL in history.")
    else:
        print("Failed to post to X. URL not recorded in history.")
        
    print("\nExecution completed.")

if __name__ == "__main__":
    main()
