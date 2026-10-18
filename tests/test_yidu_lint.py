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


if __name__ == "__main__":
    unittest.main()
