# 人写语料来源与许可

语料**不入库**。`fetch_corpus.py` 运行时下载到 `tests/corpus/cache/`（已 gitignore），每篇只取前 3000 字节选。仓库里只有脚本和本清单。
下载：`python3 tests/corpus/fetch_corpus.py`；统计：`python3 tests/corpus/run_corpus.py [--auto] [--detail]`。
下载日期：2026-10-18。

## 百科（4 篇）和技术中的 3 篇：中文维基百科
- 许可：CC BY-SA 4.0（署名、相同方式共享）。页面历史里有作者署名，见各条目「查看历史」。
- 不入库的原因：入库就得按相同方式共享并逐篇署名；节选只在本机用于统计，不再分发。
- 条目（URL 均为 `https://zh.wikipedia.org/wiki/<标题>`）：光合作用、长江、勾股定理、造纸术、超文本传输协议、Git、关系数据库。

## 技术（2 篇）：Python 官方文档中文版
- URL：https://docs.python.org/zh-cn/3/tutorial/classes.html 、https://docs.python.org/zh-cn/3/tutorial/errors.html
- 许可：PSF License Version 2（Python 3.8.6 起，文档中的示例代码另可按 0BSD 使用）。依据：https://docs.python.org/3/license.html 。译者贡献按 CC0 提供给 PSF（python-docs-zh-cn 的 README）；但译文是英文文档的衍生作品，仍适用 PSF 许可（discuss.python.org 上的讨论）。使用需保留 PSF 版权声明，所以同样不入库。
- 注意：这是译文，文风带翻译腔，不完全等同原生中文。

## 公文（5 篇）：中国政府网
- 《中华人民共和国政府信息公开条例》（国令第711号）：https://www.gov.cn/zhengce/zhengceku/2019-04/15/content_5382991.htm
- 国办发〔2024〕31 号：https://www.gov.cn/zhengce/zhengceku/202406/content_6958231.htm
- 国办发〔2024〕29 号：https://www.gov.cn/zhengce/zhengceku/202406/content_6955905.htm
- 国办发〔2024〕9 号：https://www.gov.cn/zhengce/zhengceku/202403/content_6940155.htm
- 国办发〔2024〕33 号：https://www.gov.cn/zhengce/zhengceku/202407/content_6961216.htm
- 许可依据：《著作权法》第五条第（一）项，法律、法规，国家机关的决议、决定、命令和其他具有立法、行政、司法性质的文件不适用本法（来源：https://www.gov.cn/guoqing/2021-10/29/content_5647633.htm ）。国办发通知我认为属于「行政性质文件」，这是我的判断，不是法律意见。
- 是否入库：法律上可以，但为了和其他类一致，仍只存 URL。

## 随笔（2 篇）：中文维基文库
- 朱自清《背影》（1925）https://zh.wikisource.org/wiki/背影 ；《荷塘月色》（1927）https://zh.wikisource.org/wiki/荷塘月色
- 状态：作者 1948 年去世。维基文库页面标注「1931 年 1 月 1 日以前出版，作者 1948 年逝世，在美国及保护期为作者终身加 75 年以下的国家和地区属于公有领域」。国家版权局页面（web.archive.org 存档）说明作者死后第 50 年 12 月 31 日起进入公有领域，并举朱自清为例。作品本身我认为在中国大陆和美国均属公有领域；署名权等人身权不受期限限制，使用时应署作者名。
- 注意：维基文库的文本是繁体（API 的简体转换未生效），而词表是简体，所以这 2 篇的 0 命中不能说明词表对随笔有效。**essay 的语料校准基本没有做成。**

## 没做的场景
- 新闻：没找到许可明确、能稳定下载的来源，跳过。
