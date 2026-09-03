"""Codexが書いた【指導要領：保健分野 (3) ア (ｴ)】の表記を、解説の本文にある項目と学年配当に照らして検査する"""
import re,sys,glob,docx
VALID={ # 内容番号 -> {ア: 小項目, イ: None}
 "1":{"ア":set("ｱｲｳｴｵｶ"),"イ":set()},
 "2":{"ア":set("ｱｲｳｴ"),"イ":set()},
 "3":{"ア":set("ｱｲｳｴ"),"イ":set()},
 "4":{"ア":set("ｱｲｳ"),"イ":set()},
}
GRADE2={("1","ア","ｳ"),("1","ア","ｴ"),("1","イ",None),("3","ア","ｱ"),("3","ア","ｲ"),("3","ア","ｳ"),("3","ア","ｴ"),("3","イ",None)}
NORM=str.maketrans("（）アイウエオカ","()ｱｲｳｴｵｶ")
pat=re.compile(r"【指導要領[：:]\s*保健分野\s*[（(]\s*([1-4１-４])\s*[)）]\s*([アイ])\s*(?:[（(]\s*([ｱｲｳｴｵｶアイウエオカ])\s*[)）])?\s*(?:[（(]関連[：:].*?[)）])?\s*】")
ok=bad=0
for f in sorted(glob.glob(sys.argv[1]+"/*.docx")):
    d=docx.Document(f); texts=[p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows: texts.append(" | ".join(c.text for c in r.cells))
    n=0
    for line in texts:
        for m in pat.finditer(line):
            n+=1
            num=m.group(1).translate(str.maketrans("１２３４","1234")); ab=m.group(2); sub=m.group(3).translate(NORM) if m.group(3) else None
            valid = ab in VALID[num] and ((sub is None and ab=="イ") or (sub in VALID[num]["ア"] and ab=="ア"))
            g2 = (num,ab,sub) in GRADE2
            flag = "OK " if valid and g2 else ("項目なし" if not valid else "2年の範囲外")
            if not (valid and g2): bad+=1; print(f"  {flag}: {m.group(0)}  ← {line[:70]}")
            else: ok+=1
    print(f"{f.split('/')[-1]}: 表記 {n} 件")
print(f"合計 OK {ok} / NG {bad}")
