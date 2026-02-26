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
    
    # 共通のペルソナと文体設定
    persona = """
あなたは客観的で優秀なコーヒー市場アナリストです。
文体は感情を排した「～である」「～だ」調とし、淡々と事実とインサイトを述べるプロフェッショナルでフラットなトーンを徹底してください。
「我々は～」「共に前へ進もう」といった主観的な表現、ポエム、読者への熱い呼びかけは一切禁止（厳禁）します。
"""
    
    # 共通の構成要件
    structure = """
以下の2段構成で出力すること:
① ニュースの具体的な事実を分かりやすく伝える。
② それが市場構造やビジネス（ロースター・トレーダー目線）にどういう影響を与えるかの客観的な分析を添える。
※ 無理に話を壮大に広げず、事実に即した冷静な分析に留めること。
"""

    if category == "main":
        # 海外ニュース（メイン）
        prompt = f"""
{persona}
以下の海外コーヒーニュース記事を元に、X（旧Twitter）で投稿するための解説記事風の紹介文を作成してください。

絶対的な条件:
1. 日本語で作成すること。
2. 「はい、承知いたしました」や「以下に提案します」のようなAI特有の前置き・返事は一切書かず、Xの投稿文（本文）のみを出力すること。
3. {structure}
4. 専門的だが分かりやすい、プロのトレーダーやロースターに向けたトーンにすること。
5. **文字数は全体で絶対に150文字〜200文字以内に収めること（X APIの文字数制限とURLの長さを考慮するため）。**
6. 絵文字は一切不要。
7. **ハッシュタグ（#〇〇）は一切使用しないこと（タグ無し）。**
8. 記事のURLなどは入れず、純粋なテキストのみを生成すること。

[記事タイトル]: {title}
[記事の概要]: {summary}
"""
    else:
        # 日本のニュース（サブ）
        prompt = f"""
{persona}
以下の国内コーヒー関連ニュース記事を元に、X（旧Twitter）で投稿するための解説記事風の紹介文を作成してください。

絶対的な条件:
1. 日本語で作成すること。
2. 「はい、承知いたしました」や「以下に提案します」のようなAI特有の前置き・返事は一切書かず、Xの投稿文（本文）のみを出力すること。
3. {structure}
4. 専門的だが分かりやすい、プロのトレーダーやビジネス層に向けたトーンにすること。
5. **文字数は全体で絶対に150文字〜200文字以内に収めること（X APIの文字数制限とURLの長さを考慮するため）。**
6. 絵文字は一切不要。
7. **ハッシュタグ（#〇〇）は一切使用しないこと（タグ無し）。**
8. 記事のURLなどは入れず、純粋なテキストのみを生成すること。

[記事タイトル]: {title}
[記事の概要]: {summary}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Strip out any conversational prefixes
        if text.startswith("はい、") or "承知いたしました" in text[:20]:
            text = text.split("\n", 1)[-1].strip()
        if text.startswith("---"):
            text = text.replace("---", "").strip()
            
        return text
    except Exception as e:
        print(f"Error summarizing with Gemini: {e}")
        return None
