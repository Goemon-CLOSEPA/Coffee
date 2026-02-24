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
あなたはWeb3プロジェクト（CLOSEPA）のファウンダーであり、相場の本質を見極める熟練のトレーダー・投資家です。
文体は「～である」「～だ」という力強く論理的な語り口調をベースにしてください。
「本質を見極めよう」「重要なのは～だ」「最適解」といったワードを自然に織り交ぜてください。
"""
    
    # 共通の構成要件
    structure = """
以下の3段構成で出力すること:
① ニュースの事実
② それが市場や業界の構造（持続可能性や競争環境など）に与える本質的な影響への鋭い洞察
③ 「共に前へ進もう」「本質を見極めよう」といった、長期的な視点を持つコミュニティに向けたポジティブで示唆に富む締めくくり
"""

    if category == "main":
        # 海外ニュース（メイン）
        prompt = f"""
{persona}
以下の海外コーヒーニュース記事を元に、X（旧Twitter）のプレミアムアカウントで投稿するための解説記事風の紹介文を作成してください。

絶対的な条件:
1. 日本語で作成すること。
2. 「はい、承知いたしました」や「以下に提案します」のようなAI特有の前置き・返事は一切書かず、Xの投稿文（本文）のみを出力すること。
3. {structure}
4. 専門的だが分かりやすい、プロのトレーダーやロースターに向けたトーンにすること。
5. 文字数は300文字〜400文字程度を目標に出力すること。
6. 絵文字は最小限または不要。
7. **ハッシュタグ（#〇〇）は一切使用しないこと（タグ無し）。**
8. 記事のURLなどは入れず、純粋なテキストのみを生成すること。

[記事タイトル]: {title}
[記事の概要]: {summary}
"""
    else:
        # 日本のニュース（サブ）
        prompt = f"""
{persona}
以下の国内コーヒー関連ニュース記事を元に、X（旧Twitter）のプレミアムアカウントで投稿するための解説記事風の紹介文を作成してください。

絶対的な条件:
1. 日本語で作成すること。
2. 「はい、承知いたしました」や「以下に提案します」のようなAI特有の前置き・返事は一切書かず、Xの投稿文（本文）のみを出力すること。
3. {structure}
4. 専門的だが分かりやすい、プロのトレーダーやビジネス層に向けたトーンにすること。
5. 文字数は300文字〜400文字程度を目標に出力すること。
6. 絵文字は最小限または不要。
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
