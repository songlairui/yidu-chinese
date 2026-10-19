#!/usr/bin/env python3
"""对 cache/ 里的人写语料跑 yidu_lint，按场景、规则统计命中。语料全是人写，所以每个命中都算误报。
用法：python3 tests/corpus/run_corpus.py [--auto] [--detail]
默认所有场景都用默认参数；--auto 则 tech/formal/essay 场景用同名 profile，百科仍用默认。"""
import collections, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import yidu_lint

def main(argv):
    auto = "--auto" in argv
    detail = "--detail" in argv
    files = sorted((HERE / "cache").glob("*.txt"))
    by = collections.defaultdict(lambda: collections.defaultdict(int))
    words = collections.defaultdict(collections.Counter)
    chars = collections.Counter(); n = collections.Counter()
    for f in files:
        scene = f.name.split("__")[0]
        text = f.read_text(encoding="utf-8")
        chars[scene] += len(text); n[scene] += 1
        hits = yidu_lint.lint(text, profile=scene if auto and scene in yidu_lint.PROFILES else None)
        for _, cat, w in hits:
            by[scene][cat] += 1; words[(scene, cat)][w] += 1
    for scene in sorted(by.keys() | n.keys()):
        tot = sum(by[scene].values())
        print("%s：%d 篇，%d 字，共 %d 处" % (scene, n[scene], chars[scene], tot))
        for cat, c in sorted(by[scene].items(), key=lambda kv: -kv[1]):
            ex = ""
            if detail: ex = "  " + "、".join("%s×%d" % kv for kv in words[(scene, cat)].most_common(8))
            print("  %s：%d%s" % (cat, c, ex))
if __name__ == "__main__":
    main(sys.argv)
