#!/usr/bin/env python3
"""易读中文 lint：检测中文常见 AI 腔。纯标准库。
用法：python3 scripts/yidu_lint.py 文件.md   或   cat 文件 | python3 scripts/yidu_lint.py -
退出码：有命中为 1，无命中为 0。"""
import re
import sys
from pathlib import Path

LISTS = Path(__file__).resolve().parent.parent / "skills" / "yidu-zhongwen" / "references" / "lists"
MAX_SENT = 60       # 单句超过此字数提示（经验阈值，可调，非实证）
MAX_BOLD = 3        # 每篇加粗处超过此数提示
NOT_BUT = re.compile(r"不是[^。！？\n]{1,30}?[，,]?\s*而是")
NOT_BUT_LIMIT = 2   # 「不是…而是」出现多于此数视为滥用
BOLD = re.compile(r"\*\*[^*\n]+\*\*")


def load(name):
    out = []
    for ln in (LISTS / name).read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            out.append(ln)
    return out


def lint(text):
    """返回 [(行号, 类别, 命中)]"""
    hits = []
    lines = text.splitlines()
    for cat, fn in (("黑话", "buzzwords.txt"), ("套话", "filler.txt"), ("比喻动词", "metaphor_verbs.txt")):
        words = load(fn)
        for i, ln in enumerate(lines, 1):
            for w in words:
                if w in ln:
                    hits.append((i, cat, w))
    nb = [(i, m.group(0)) for i, ln in enumerate(lines, 1) for m in NOT_BUT.finditer(ln)]
    if len(nb) > NOT_BUT_LIMIT:
        hits += [(i, "不是…而是 滥用", s) for i, s in nb]
    bolds = [(i, m.group(0)) for i, ln in enumerate(lines, 1) for m in BOLD.finditer(ln)]
    if len(bolds) > MAX_BOLD:
        hits += [(i, "过度加粗", s) for i, s in bolds]
    for i, ln in enumerate(lines, 1):
        if ln.lstrip().startswith(("#", "```")):
            continue
        for s in re.split(r"[。！？!?；;]", ln):
            if len(s) > MAX_SENT:
                hits.append((i, "过长句", s[:12] + "…(%d字)" % len(s)))
    return sorted(hits, key=lambda h: h[0])


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    text = sys.stdin.read() if argv[1] == "-" else Path(argv[1]).read_text(encoding="utf-8")
    hits = lint(text)
    for i, cat, w in hits:
        print("第%d行 [%s] %s" % (i, cat, w))
    print("共 %d 处" % len(hits))
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
