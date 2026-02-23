import os
import google.generativeai as genai

def summarize_article(title, summary, category, max_retries=3):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return None
        
    genai.configure(api_key=api_key)
    # Using the flash model for quick, cost-effective, and high quality generation
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    if category == "main":
        # 海外ニュース（メイン）
        prompt = f"""
以下の海外コーヒーニュース記事を元に、X（旧Twitter）に投稿するための紹介文を作成してください。

絶対的な条件:
1. 日本語で作成すること。
2. 「はい、承知いたしました」や「以下に提案します」のようなAI特有の前置き・返事は一切書かず、Xの投稿文（本文）のみを出力すること。
3. 価格変動の要因（天候、物流、需給など）や市場・ビジネスへの影響に焦点を当て、トレーダーやロースター向けに客観的でフラットな箇条書きにすること。
4. 絵文字や宣伝文句は一切不要。
5. 90文字〜100文字程度に収めること（URLと合わせて140字の制限に確実に収めるため）。
6. ハッシュタグは文末に1〜2個（#Coffee #Crypto など）つけること。

[記事タイトル]: {title}
[記事の概要]: {summary}
"""
    else:
        # 日本のニュース（サブ）
        prompt = f"""
以下の国内コーヒー関連ニュース記事を元に、X（旧Twitter）に投稿するための紹介文を作成してください。

絶対的な条件:
1. 日本語で作成すること。
2. 「はい、承知いたしました」や「以下に提案します」のようなAI特有の前置き・返事は一切書かず、Xの投稿文（本文）のみを出力すること。
3. 国内のコーヒートレンドとして、要点を簡潔でニュートラルな文章にまとめること（客観的・フラット）。絵文字は最小限または不要。
4. 90文字〜100文字程度に収めること（URLと合わせて140字の制限に確実に収めるため）。
5. ハッシュタグは文末に1〜2個（#Coffee #Crypto など）つけること。

[記事タイトル]: {title}
[記事の概要]: {summary}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Strip out any conversational prefixes if Gemini still includes them
        if text.startswith("はい、") or "承知いたしました" in text[:20]:
            text = text.split("\n", 1)[-1].strip()
        if text.startswith("---"):
            text = text.replace("---", "").strip()
            
        # Ensure it's not too long
        if len(text) > 115:
            text = text[:112] + "..."
            
        return text
    except Exception as e:
        print(f"Error summarizing with Gemini: {e}")
        return None
