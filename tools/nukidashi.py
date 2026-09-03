"""文科省の解説PDFから、指定ページの本文をテキストファイルに抜き出す。
使い方: python3 nukidashi.py 解説.pdf 開始ページ 終了ページ 出力.txt
ページ番号は「印刷されているページ番号」ではなくPDFの通し番号（1始まり）。
先頭に出典を1行書いてから使う。pymupdf が要る（pip install pymupdf）。
"""
import sys, re
import fitz

pdf, start, end, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
d = fitz.open(pdf)
parts = []
for n in range(start, end + 1):
    lines = []
    for l in d[n - 1].get_text().split("\n"):
        s = l.strip()
        if not s or re.fullmatch(r"\d{1,3}", s):
            continue
        lines.append(l.rstrip())
    parts.append(f"\n［PDF p.{n}］\n" + "\n".join(lines))
open(out, "w", encoding="utf-8").write("出典：（ここに文書名を書く）\n" + "\n".join(parts))
print(out, "に", end - start + 1, "ページ分を書き出しました")
