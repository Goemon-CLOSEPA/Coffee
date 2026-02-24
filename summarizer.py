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
以下の海外コーヒーニュース記事を元に、X（旧Twitter）のプレミアムアカウント（長文可能）で投稿するための解説記事風の紹介文を作成してください。

絶対的な条件:
1. 日本語で作成すること。
2. 「はい、承知いたしました」や「以下に提案します」のようなAI特有の前置き・返事は一切書かず、Xの投稿文（本文）のみを出力すること。
3. 専門的だが分かりやすい、プロのトレーダーやロースターに向けた解説記事風のトーンにすること。
4. 単なる要約や箇条書きだけでなく、記事の背景や市場・ビジネスへの影響に対する「洞察（インサイト）」を必ず含めること。
5. 文字数は300文字〜400文字程度を目標に出力すること。
6. 絵文字は最小限または不要。
7. ハッシュタグ（#Coffee #Crypto など）は文章が途切れないよう、必ず本文の一番最後に配置すること。

[記事タイトル]: {title}
[記事の概要]: {summary}
"""
    else:
        # 日本のニュース（サブ）
        prompt = f"""
以下の国内コーヒー関連ニュース記事を元に、X（旧Twitter）のプレミアムアカウント（長文可能）で投稿するための解説記事風の紹介文を作成してください。

絶対的な条件:
1. 日本語で作成すること。
2. 「はい、承知いたしました」や「以下に提案します」のようなAI特有の前置き・返事は一切書かず、Xの投稿文（本文）のみを出力すること。
3. 専門的だが分かりやすい、プロのトレーダーやビジネス層に向けた解説記事風のトーンにすること。
4. 単なる事実の羅列だけでなく、国内のコーヒートレンドや今後の市場への影響に対する「洞察（インサイト）」を必ず含めること。
5. 文字数は300文字〜400文字程度を目標に出力すること。
6. 絵文字は最小限または不要。
7. ハッシュタグ（#Coffee #Crypto など）は文章が途切れないよう、必ず本文の一番最後に配置すること。

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
            
        return text
    except Exception as e:
        print(f"Error summarizing with Gemini: {e}")
        return None
