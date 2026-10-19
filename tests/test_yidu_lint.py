import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import yidu_lint as L


def cats(t):
    return {c for _, c, _ in L.lint(t)}


class T(unittest.TestCase):
    def test_buzzword(self):
        self.assertIn("黑话", cats("我们要赋能业务。"))

    def test_filler(self):
        self.assertIn("套话", cats("总的来说，结果不错。"))

    def test_metaphor_verb(self):
        self.assertIn("比喻动词", cats("这个数据击穿了认知。"))

    def test_not_but_overuse(self):
        t = "不是快，而是稳。\n不是贵，而是值。\n不是少，而是精。"
        self.assertIn("不是…而是 滥用", cats(t))

    def test_not_but_single_ok(self):
        self.assertNotIn("不是…而是 滥用", cats("不是快，而是稳。"))

    def test_bold(self):
        t = "**一**和**二**和**三**和**四**"
        self.assertIn("过度加粗", cats(t))

    def test_long_sentence(self):
        self.assertIn("过长句", cats("我" * 80 + "。"))

    def test_line_number(self):
        self.assertEqual(L.lint("好。\n\n综上所述，好。")[0][0], 3)

    def test_clean(self):
        self.assertEqual(L.lint("服务器昨晚重启了两次。原因是磁盘满了。"), [])


class Exempt(unittest.TestCase):
    def test_fenced_code(self):
        self.assertEqual(L.lint("```\n赋能 综上所述\n```\n好。"), [])

    def test_tilde_fence(self):
        self.assertEqual(L.lint("~~~\n赋能\n~~~"), [])

    def test_inline_code(self):
        self.assertEqual(L.lint("词表里有 `赋能` 这个词。"), [])

    def test_quote_block(self):
        self.assertEqual(L.lint("> 综上所述，赋能。"), [])

    def test_usage_line(self):
        self.assertEqual(L.lint("用法：python3 x.py 赋能.md"), [])

    def test_after_fence_still_checked(self):
        self.assertEqual(L.lint("```\nx\n```\n赋能业务。")[0][0], 4)

    def test_line_numbers_kept(self):
        self.assertEqual(L.lint("> 引用\n\n综上所述。")[0][0], 3)

    def test_no_exempt_option(self):
        self.assertTrue(L.lint("`赋能`", exempt=False))


class Round2(unittest.TestCase):
    def test_new_buzz(self):
        self.assertIn("黑话", cats("我们要打出组合拳。"))

    def test_new_filler(self):
        self.assertIn("套话", cats("众所周知，水是湿的。"))

    def test_new_metaphor(self):
        self.assertIn("比喻动词", cats("数据谱写了新篇章。"))

    def test_seq_stack(self):
        t = "首先，备份。\n其次，升级。\n最后，重启。"
        self.assertIn("首先其次最后 堆叠", cats(t))

    def test_seq_partial_ok(self):
        self.assertNotIn("首先其次最后 堆叠", cats("首先备份，然后升级。"))

    def test_closer_help(self):
        self.assertIn("结尾套话", cats("就这些。希望对你有帮助！"))

    def test_closer_ask(self):
        self.assertIn("结尾套话", cats("如有疑问，欢迎随时提问。"))

    def test_closer_none(self):
        self.assertNotIn("结尾套话", cats("这个脚本帮助我们备份。"))

    def test_emoji_many(self):
        self.assertIn("emoji 过多", cats("好🚀 快✨ 强💡"))

    def test_emoji_few_ok(self):
        self.assertNotIn("emoji 过多", cats("好🚀 快✨"))

    def test_dash_many(self):
        self.assertIn("破折号过多", cats("甲——乙。丙——丁。戊——己。"))

    def test_dash_few_ok(self):
        self.assertNotIn("破折号过多", cats("甲——乙。"))


FIX = Path(__file__).resolve().parent / "fixtures"
EXPECT = {
    "ai_01": "黑话", "ai_02": "首先其次最后 堆叠", "ai_03": "不是…而是 滥用",
    "ai_04": "emoji 过多", "ai_05": "破折号过多", "ai_06": "比喻动词",
    "ai_07": "过度加粗", "ai_08": "过长句", "ai_09": "结尾套话",
}


class Fixtures(unittest.TestCase):
    def test_ai_samples_hit_expected_rule(self):
        for name, cat in EXPECT.items():
            t = (FIX / (name + ".txt")).read_text(encoding="utf-8")
            self.assertIn(cat, cats(t), name)

    def test_human_samples_clean(self):
        for f in FIX.glob("human_*.txt"):
            self.assertEqual(L.lint(f.read_text(encoding="utf-8")), [], f.name)

    def test_summarize(self):
        self.assertEqual(L.summarize([(1, "a", "x"), (2, "a", "y"), (3, "b", "z")]), {"a": 2, "b": 1})

    def test_json_output(self):
        import io, json, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = L.main(["x", "--json", str(FIX / "ai_01.txt")])
        d = json.loads(buf.getvalue())
        self.assertEqual(code, 1)
        self.assertEqual(d["total"], sum(d["summary"].values()))
        self.assertIn("黑话", d["summary"])
        self.assertEqual(d["hits"][0].keys(), {"line": 0, "rule": 0, "match": 0}.keys())

    def test_table_and_url_not_long_sentence(self):
        row = "| " + " | ".join(["短格" * 10] * 4) + " |"
        self.assertEqual(L.lint(row), [])
        self.assertEqual(L.lint("来源 https://example.com/" + "a" * 100), [])



class ProfileTests(unittest.TestCase):
    def cats(self, t, profile=None):
        return {c for _, c, _ in L.lint(t, profile=profile)}

    def test_tech_skips_align(self):
        t = "把两个字段对齐后再比较。"
        self.assertIn("黑话", self.cats(t))
        self.assertNotIn("黑话", self.cats(t, "tech"))

    def test_tech_still_flags_other_buzzwords(self):
        self.assertIn("黑话", self.cats("我们要赋能业务。", "tech"))

    def test_formal_skips_lead(self):
        t = "要发挥引领作用。"
        self.assertIn("黑话", self.cats(t))
        self.assertNotIn("黑话", self.cats(t, "formal"))

    def test_skip_is_per_profile(self):
        self.assertIn("黑话", self.cats("把字段对齐。", "formal"))

    def test_long_sentence_threshold(self):
        t = "甲" * 90 + "。"
        self.assertIn("过长句", self.cats(t))
        self.assertIn("过长句", self.cats(t, "essay"))
        self.assertNotIn("过长句", self.cats(t, "tech"))
        self.assertIn("过长句", self.cats(("甲" * 110) + "。", "tech"))
        self.assertNotIn("过长句", self.cats(t, "formal"))
        self.assertIn("过长句", self.cats(("甲" * 130) + "。", "formal"))

    def test_cli_bad_profile(self):
        self.assertEqual(L.main(["x", "--profile", "nope", "f.txt"]), 2)

    def test_ai_fixtures_caught_under_all_profiles(self):
        d = Path(__file__).resolve().parent / "fixtures"
        for prof in (None, "tech", "formal", "essay"):
            for f in sorted(d.glob("ai_*.txt")):
                self.assertTrue(L.lint(f.read_text(encoding="utf-8"), profile=prof), (prof, f.name))

if __name__ == "__main__":
    unittest.main()
