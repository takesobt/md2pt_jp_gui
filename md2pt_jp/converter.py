from typing import Optional
import re
#import pdb

def convert_markdown_to_plaintext(markdown_text: str) -> str:
    text = markdown_text

    # --- オリジナルのmarkdown情報の変換 ---

    # Step 1: 見出しの変換の前処理
    # Step 1-1: 既に【】がついている見出しをクリーンに（#【見出し】 → #見出し）
    text = re.sub(r'^(#+)\s*【(.*?)】', r'\1 \2', text, flags=re.MULTILINE)

    # Step 1-2: 既に☆☆がついている見出しをクリーンに（#☆☆見出し☆☆ → #見出し）
    text = re.sub(r'^(#+)\s*☆☆(.*?)☆☆', r'\1 \2', text, flags=re.MULTILINE)

    # Step 1-3: 既に☆EPISODE☆がついている見出しをクリーンに（#☆EPISODE☆見出し → #見出し）
    text = re.sub(r'^(#+)\s*☆EPISODE☆\s*(.+)', r'\1 \2', text, flags=re.MULTILINE)

    # Step 2: ###（見出し3）→ 【見出し３】
    text = re.sub(r'^###\s*(.+)', lambda m: f'【{m.group(1).strip()}】', text, flags=re.MULTILINE)

    # Step 3: ##（見出し2）→ ☆☆見出し２☆☆
    text = re.sub(r'^##\s*(.+)', lambda m: f'☆☆{m.group(1).strip()}☆☆', text, flags=re.MULTILINE)

    # Step 4: #（見出し1）→ ☆EPISODE☆見出し１
    text = re.sub(r'^#\s*(.+)', lambda m: f'☆EPISODE☆{m.group(1).strip()}', text, flags=re.MULTILINE)

    # Step 5: 区切り線（---）を全角線に変換
    text = re.sub(r'^-{3,}\s*$', '＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝', text, flags=re.MULTILINE)

    # Step 6: 画像リンク行（Markdown: ![...](...)）を削除
    text = re.sub(r'^!\[.*?\]\(.*?\)\s*$', '', text, flags=re.MULTILINE)

    # --- 一般的なmarkdown情報の変換 ---

    # 強調記号の削除 (★★text★★ → text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)

    # イタリック記号の削除 (*text* → text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)

    # 箇条書きの変換 (- や * → ・)
    text = re.sub(r'^\s*[-*+]\s+', '・', text, flags=re.MULTILINE)

    # 番号付きリスト (1. → ・)
    text = re.sub(r'^\s*\d+\.\s+', '・', text, flags=re.MULTILINE)

    # インラインコードの除去 (`text` → text)
    text = re.sub(r'`(.*?)`', r'\1', text)

    # <br> → 改行
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)

    # 複数改行の整理
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()