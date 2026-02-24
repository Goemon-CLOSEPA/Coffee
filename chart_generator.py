import yfinance as yf
import matplotlib.pyplot as plt
import os
import google.generativeai as genai

CHART_FILENAME = "chart.png"

def generate_coffee_futures_chart():
    """
    Fetches the last 1 month of KC=F (Coffee Futures) data via yfinance,
    generates a matplotlib chart saved to chart.png,
    and returns the latest close price and daily change percentage.
    """
    print("Fetching KC=F data from yfinance...")
    ticker = yf.Ticker("KC=F")
    # Fetch 1 month of daily data
    hist = ticker.history(period="1mo")
    
    if hist.empty:
        print("Error: No data retrieved for KC=F.")
        return None, None
        
    # Extract latest data
    latest_close = hist['Close'].iloc[-1]
    prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else latest_close
    
    price_change = latest_close - prev_close
    pct_change = (price_change / prev_close) * 100
    
    # Generate Plot
    plt.figure(figsize=(10, 5))
    plt.plot(hist.index, hist['Close'], color='#6f4e37', linewidth=2) # Coffee brown color
    plt.title('Coffee C Futures (KC=F) - Last 30 Days', fontsize=14, fontweight='bold')
    plt.ylabel('Price (USd/lb)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Rotate dates for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(CHART_FILENAME)
    plt.close()
    print(f"Chart saved to {CHART_FILENAME}")
    
    return latest_close, pct_change

def generate_market_commentary(latest_price, pct_change):
    """
    Uses Gemini to generate a short market commentary based on the 
    daily price action.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return None
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    direction = "上昇" if pct_change >= 0 else "下落"
    sign = "+" if pct_change >= 0 else ""
    
    prompt = f"""
あなたはWeb3プロジェクト（CLOSEPA）のファウンダーであり、相場の本質を見極める熟練のトレーダー・投資家です。
文体は「～である」「～だ」という力強く論理的な語り口調をベースにしてください。
「本質を見極めよう」「重要なのは～だ」「最適解」といったワードを自然に織り交ぜてください。

本日のコーヒー先物（アラビカ種: KC=F）の市場価格データを元に、X（旧Twitter）に「毎朝の市況アップデート」として投稿するコメントを作成してください。

データ:
- 最新価格: {latest_price:.2f} ＵSセント/ポンド
- 前日比: {sign}{pct_change:.2f}% ({direction})

絶対的な条件:
1. 日本語で作成すること。
2. 「はい」などのAI特有の前置きは一切書かず、Xの投稿文（本文）のみを出力すること。
3. おはようございます等の挨拶は不要。いきなり本題（今日の価格と前日比）から入ること。
4. この価格変動から読み取れる、市場や業界の構造への鋭い洞察（インサイト）を含めること。
5. 「共に前へ進もう」「本質を見極めよう」といった、長期的な視点を持つコミュニティに向けたポジティブで示唆に富む締めくくりを入れること。
6. 添付するチャート画像（過去1ヶ月の推移）と一緒に見られることを前提としたトーンにすること（約200〜300文字）。
7. **ハッシュタグ（#〇〇）は一切使用しないこと（タグ無し）。**
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Strip out any conversational prefixes
        if text.startswith("はい、") or "承知いたしました" in text[:20]:
            text = text.split("\n", 1)[-1].strip()
            
        return text
    except Exception as e:
        print(f"Error generating market commentary with Gemini: {e}")
        return None
