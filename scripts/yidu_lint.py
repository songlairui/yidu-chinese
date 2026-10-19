#!/usr/bin/env python3
"""易读中文 lint：检测中文常见 AI 腔。纯标准库。
用法：python3 scripts/yidu_lint.py [--json] [--profile tech|formal|essay] 文件.md   或   cat 文件 | python3 scripts/yidu_lint.py -
退出码：有命中为 1，无命中为 0。"""
import json
import re
import sys
from pathlib import Path

LISTS = Path(__file__).resolve().parent.parent / "skills" / "yidu-zhongwen" / "references" / "lists"
MAX_SENT = 60       # 单句超过此字数提示（经验阈值，可调，非实证）
MAX_BOLD = 3        # 每篇加粗处超过此数提示
NOT_BUT = re.compile(r"不是[^。！？\n]{1,30}?[，,]?\s*而是")
NOT_BUT_LIMIT = 2   # 「不是…而是」出现多于此数视为滥用
SEQ_WORDS = ("首先", "其次", "最后")   # 三者同时出现视为套路堆叠
CLOSERS = re.compile(r"(希望(以上|这些|本文|这篇|这份|上述)?[^。！\n]{0,12}?(对你|对您|对大家)?有(所)?帮助|如有(任何)?(疑问|问题)[^。\n]{0,10}(随时|请)[^。\n]{0,10}|欢迎(随时)?(继续)?(提问|留言|交流)|祝(你|您)[^。\n]{0,8}(愉快|顺利))")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2705\u274C]")
EMOJI_LIMIT = 2
DASH = re.compile("——")
DASH_LIMIT = 2
BOLD = re.compile(r"\*\*[^*\n]+\*\*")


# 场景参数。依据见 docs/TUNING.md；skip 为该场景下属于正常用词、不报的词。
PROFILES = {
    "essay": {"max_sent": 60, "skip": ()},
    "tech": {"max_sent": 100, "skip": ("对齐", "沉淀", "链路")},
    "formal": {"max_sent": 120, "skip": ("引领", "赛道", "抓手", "全方位", "赋予")},
}


def load(name):
    out = []
    for ln in (LISTS / name).read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            out.append(ln)
    return out


URL = re.compile(r"https?://\S+")
INLINE_CODE = re.compile(r"`[^`\n]*`")
USAGE_PREFIX = ("用法：", "用法:", "运行：", "运行:", "命令：", "命令:", "示例命令", "$ ", "python3 ", "python ")


def mask_exempt(text):
    """把豁免内容（围栏代码块、引用块、行内代码、用法说明）替换为空行/删除，保持行号不变。"""
    out, fence = [], None
    for ln in text.splitlines():
        st = ln.lstrip()
        m = re.match(r"(`{3,}|~{3,})", st)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            out.append("")
            continue
        if m:
            fence = m.group(1)
            out.append("")
            continue
        if st.startswith(">") or st.startswith(USAGE_PREFIX):
            out.append("")
            continue
        out.append(INLINE_CODE.sub("", ln))
    return out


def lint(text, exempt=True, profile=None):
    """返回 [(行号, 类别, 命中)]"""
    hits = []
    prof = PROFILES[profile] if profile else {"max_sent": MAX_SENT, "skip": ()}
    max_sent = prof["max_sent"]
    lines = mask_exempt(text) if exempt else text.splitlines()
    for cat, fn in (("黑话", "buzzwords.txt"), ("套话", "filler.txt"), ("比喻动词", "metaphor_verbs.txt")):
        words = [w for w in load(fn) if w not in prof["skip"]]
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
    seq = [(i, w) for w in SEQ_WORDS for i, ln in enumerate(lines, 1) if w in ln]
    if all(any(w == x for _, x in seq) for w in SEQ_WORDS):
        hits += [(i, "首先其次最后 堆叠", w) for i, w in seq]
    for i, ln in enumerate(lines, 1):
        for m in CLOSERS.finditer(ln):
            hits.append((i, "结尾套话", m.group(0)))
    em = [(i, m.group(0)) for i, ln in enumerate(lines, 1) for m in EMOJI.finditer(ln)]
    if len(em) > EMOJI_LIMIT:
        hits += [(i, "emoji 过多", e) for i, e in em]
    ds = [(i, "——") for i, ln in enumerate(lines, 1) for _ in DASH.finditer(ln)]
    if len(ds) > DASH_LIMIT:
        hits += [(i, "破折号过多", d) for i, d in ds]
    for i, ln in enumerate(lines, 1):
        if ln.lstrip().startswith(("#", "```")):
            continue
        ln = URL.sub("", ln)
        for s in re.split(r"[。！？!?；;|]", ln):
            if len(s) > max_sent:
                hits.append((i, "过长句", s[:12] + "…(%d字)" % len(s)))
    return sorted(hits, key=lambda h: h[0])


def summarize(hits):
    """按规则汇总命中数。"""
    out = {}
    for _, cat, _ in hits:
        out[cat] = out.get(cat, 0) + 1
    return out


def main(argv):
    args = argv[1:]
    as_json = "--json" in args
    args = [a for a in args if a != "--json"]
    profile = None
    if "--profile" in args:
        k = args.index("--profile")
        if k + 1 >= len(args) or args[k + 1] not in PROFILES:
            print("--profile 取值：" + "、".join(PROFILES))
            return 2
        profile = args[k + 1]
        del args[k:k + 2]
    if len(args) != 1:
        print(__doc__)
        return 2
    text = sys.stdin.read() if args[0] == "-" else Path(args[0]).read_text(encoding="utf-8")
    hits = lint(text, profile=profile)
    if as_json:
        print(json.dumps({
            "total": len(hits),
            "summary": summarize(hits),
            "hits": [{"line": i, "rule": c, "match": w} for i, c, w in hits],
        }, ensure_ascii=False, indent=2))
        return 1 if hits else 0
    for i, cat, w in hits:
        print("第%d行 [%s] %s" % (i, cat, w))
    print("共 %d 处" % len(hits))
    for cat, n in sorted(summarize(hits).items(), key=lambda kv: -kv[1]):
        print("  %s：%d" % (cat, n))
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
