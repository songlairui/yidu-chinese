# 易读中文

修复中文文本 AI 腔的 skill + 小工具。是日文项目 [nanaism/yomiyasu](https://github.com/nanaism/yomiyasu) 的中文衍生版。

## Credits 与许可
- 灵感与框架来自 https://github.com/nanaism/yomiyasu（MIT，Copyright (c) 2026 nanaism）。本项目是衍生作品，保留其 MIT 许可与版权声明，见 `LICENSE`。
- `UNICODE-LICENSE.txt`：本项目目前**未使用**任何 Unicode 数据文件，因此未随附。日后若引入，再加入原文件。
- 本仓库的词表、规则、代码均为重新编写，未拷贝原项目的日文内容。

## MVP 用法
```
python3 scripts/yidu_lint.py 文章.md      # 有命中退出码 1
python3 -m unittest discover tests -v     # 跑测试
```
把 `skills/yidu-zhongwen/SKILL.md` 交给支持 skill 的 AI 助手，让它按规则改写，并做复述检验。示例见 `examples/before_after.md`。

## 局限
- lint 只做词表与简单正则，不理解语义；会误报也会漏报。
- 句长、加粗、「不是…而是」的阈值是经验值，未经实测校准。
- 词表偏小，需要真实语料迭代。
- 目前只覆盖现代白话文；路线图见 `docs/ROADMAP.md`。
