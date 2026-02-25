import os
import time
from datetime import datetime
from dotenv import load_dotenv
from news_fetcher import fetch_latest_news
from history_manager import is_posted, save_to_history
from summarizer import summarize_article
from x_poster import post_to_x
from chart_generator import generate_coffee_futures_chart, generate_market_commentary, CHART_FILENAME

# Load environment variables
load_dotenv()

def run_news_branch():
    print("Executing News Post Branch...")
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

def run_chart_branch():
    print("Executing Morning Chart Branch...")
    
    # 1. Generate Chart
    latest_price, pct_change = generate_coffee_futures_chart()
    
    if latest_price is None:
        print("Failed to fetch coffee futures data.")
        return
        
    # 2. Generate Market Commentary
    print("Generating market commentary via Gemini...")
    commentary = generate_market_commentary(latest_price, pct_change)
    
    if not commentary:
        print("Failed to generate market commentary.")
        return
        
    print(f"\n[Generated Commentary]\n{commentary}\n")
    
    # 3. Post to X with Image
    print("Posting Chart to X...")
    if os.environ.get("DRY_RUN", "false").lower() == "true":
        print("DRY_RUN is enabled. Skipping actual post to X.")
    else:
        try:
            success = post_to_x(text=commentary, image_path=CHART_FILENAME)
            if success:
                print("Successfully posted Morning Chart to X.")
            else:
                print("Failed to post Morning Chart.")
        except Exception as e:
            print(f"Error during posting to X: {e}")

def main():
    print("Starting Coffee & Crypto X Bot...")
    
    # Check manual run type
    run_type = os.environ.get("RUN_TYPE")
    
    if run_type == "chart":
        print("Manual Trigger: Chart Branch")
        run_chart_branch()
    elif run_type == "news":
        print("Manual Trigger: News Branch")
        run_news_branch()
    else:
        # Check current time
        # GitHub actions servers run in UTC. 22:00 UTC == 07:00 JST.
        current_utc_hour = datetime.utcnow().hour
        print(f"Current UTC Hour: {current_utc_hour}")
        
        # Branching Logic
        if current_utc_hour == 22:
            # Run Chart Branch at 7:00 AM JST
            run_chart_branch()
        else:
            # Run standard news branch otherwise
            run_news_branch()

if __name__ == "__main__":
    main()
