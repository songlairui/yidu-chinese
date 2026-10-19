#!/usr/bin/env python3
"""运行时下载人写中文语料到 tests/corpus/cache/（已 gitignore，不入库）。
来源与许可见 SOURCES.md。每篇只取前 MAXC 字做节选。纯标准库。"""
import json, re, sys, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
MAXC = 3000
UA = "yidu-corpus/0.1 (research; local lint calibration)"

# (场景, 文件名, 类型, 标题或URL)
ITEMS = [
    ("encyclopedia", "wp_photosynthesis", "wiki:zh.wikipedia.org", "光合作用"),
    ("encyclopedia", "wp_yangtze", "wiki:zh.wikipedia.org", "长江"),
    ("encyclopedia", "wp_pythagoras", "wiki:zh.wikipedia.org", "勾股定理"),
    ("encyclopedia", "wp_papermaking", "wiki:zh.wikipedia.org", "造纸术"),
    ("tech", "wp_http", "wiki:zh.wikipedia.org", "超文本传输协议"),
    ("tech", "wp_git", "wiki:zh.wikipedia.org", "Git"),
    ("tech", "wp_rdb", "wiki:zh.wikipedia.org", "关系数据库"),
    ("tech", "pydoc_classes", "html:p", "https://docs.python.org/zh-cn/3/tutorial/classes.html"),
    ("tech", "pydoc_errors", "html:p", "https://docs.python.org/zh-cn/3/tutorial/errors.html"),
    ("formal", "gov_xxgk", "html:p", "https://www.gov.cn/zhengce/zhengceku/2019-04/15/content_5382991.htm"),
    ("formal", "gov_gbf31", "html:p", "https://www.gov.cn/zhengce/zhengceku/202406/content_6958231.htm"),
    ("formal", "gov_gbf29", "html:p", "https://www.gov.cn/zhengce/zhengceku/202406/content_6955905.htm"),
    ("formal", "gov_gbf9", "html:p", "https://www.gov.cn/zhengce/zhengceku/202403/content_6940155.htm"),
    ("formal", "gov_gbf33", "html:p", "https://www.gov.cn/zhengce/zhengceku/202407/content_6961216.htm"),
    ("essay", "ws_beiying", "ws:zh.wikisource.org", "背影"),
    ("essay", "ws_hetang", "ws:zh.wikisource.org", "荷塘月色"),
]


def get(url):
    import time
    for i in range(5):
        try:
            return _get(url)
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == 4: raise
            time.sleep(20 * (i + 1))


def _get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()


def wiki(host, title):
    q = urllib.parse.urlencode({"action": "query", "prop": "extracts", "explaintext": 1, "redirects": 1,
                                "titles": title, "format": "json", "formatversion": 2, "variant": "zh-cn"})
    d = json.loads(get("https://%s/w/api.php?%s" % (host, q)))
    t = d["query"]["pages"][0].get("extract", "")
    t = re.sub(r"^=+.*?=+\s*$", "", t, flags=re.M)
    return t


def wikisource(host, title):
    q = urllib.parse.urlencode({"action": "parse", "page": title, "prop": "text", "redirects": 1,
                                "format": "json", "formatversion": 2, "variant": "zh-cn"})
    h = json.loads(get("https://%s/w/api.php?%s" % (host, q)))["parse"]["text"]
    h = re.sub(r"<(style|script|table)\b.*?</\1>", "", h, flags=re.S)
    h = re.sub(r"</p>|<br\s*/?>", "\n", h)
    t = re.sub(r"<[^>]+>", "", h)
    import html as _h
    return re.sub(r"\n\s*\n+", "\n\n", _h.unescape(t)).strip()


class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.in_p = 0; self.skip = 0; self.out = []
    def handle_starttag(self, tag, a):
        if tag in ("script", "style", "nav", "pre", "code"): self.skip += 1
        if tag == "p": self.in_p += 1
    def handle_endtag(self, tag):
        if tag in ("script", "style", "nav", "pre", "code"): self.skip = max(0, self.skip - 1)
        if tag == "p" and self.in_p:
            self.in_p -= 1; self.out.append("\n")
    def handle_data(self, d):
        if self.in_p and not self.skip: self.out.append(d)


def html_p(url):
    raw = get(url)
    try: s = raw.decode("utf-8")
    except UnicodeDecodeError: s = raw.decode("gb18030", "ignore")
    p = P(); p.feed(s)
    return re.sub(r"\n\s*\n+", "\n\n", "".join(p.out)).strip()


def main():
    CACHE.mkdir(exist_ok=True)
    for scene, name, kind, ref in ITEMS:
        f = CACHE / ("%s__%s.txt" % (scene, name))
        if f.exists(): continue
        try:
            if kind.startswith("wiki"): t = wiki(kind.split(":", 1)[1], ref)
            elif kind.startswith("ws"): t = wikisource(kind.split(":", 1)[1], ref)
            else: t = html_p(ref)
        except Exception as e:
            print("失败", name, e); continue
        if "gov.cn" in str(ref):
            m = re.search(r"各省、自治区|^第一条", t, flags=re.M)
            if m: t = t[m.start():]
        if kind.startswith("ws"):
            t = re.split(r"\n\s*这部作品在", t)[0]  # 去掉维基文库的版权状态页脚
        t = t.strip()[:MAXC]
        if len(t) < 200:
            print("过短，跳过", name, len(t)); continue
        f.write_text(t + "\n", encoding="utf-8"); print("OK", f.name, len(t))

if __name__ == "__main__":
    main()
