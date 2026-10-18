# 路线图

状态标签：**已证实**（有可查依据）／**推测**（合理但未验证）／**未证实**（方向，未核实文献）。
带来源链接的条目已于 2026-10-18 用网络检索核对；没有链接的仍按原标签，未核实。

## 一、语言学理论
| 条目 | 目标 | 依据 | 状态 | 下一步验证 |
|---|---|---|---|---|
| 衔接与连贯 | 检测句间断裂、连接词堆砌 | 衔接（cohesion）概念见 Halliday & Hasan《Cohesion in English》（1976，Longman）：[出版社页面](https://www.routledge.com/Cohesion-in-English/Halliday-Hasan/p/book/9780582550414)，[WorldCat](https://search.worldcat.org/title/2323723)。该书研究英语；对中文和 AI 腔的解释力未验证 | 已证实（概念存在）；解释力仍为推测 | 标 30 段人写/AI 文，看连接词密度能否区分 |
| 主位—述位 | 检查句首信息是否是旧信息 | Theme/Rheme 以及 Given+New 在 Halliday《Introduction to Functional Grammar》（第 4 版目录第 3 章「Clause as message」）中有论述：[全文目录](https://archive.org/stream/ANINTRODUCTIONTOFUNCTIONALGRAMMAR2014/AN%20INTRODUCTION%20TO%20FUNCTIONAL%20GRAMMAR%202014_djvu.txt)。汉语适用方式未核实 | 已证实（理论存在）；汉语适用仍未证实 | 查文献，再小样本人工标注 |
| 话题优先特征 | 汉语主语常省略，「主谓清晰」规则别过度补主语 | Li & Thompson（1976）提出汉语是话题突出型语言：[Taylor & Francis 页面](https://www.taylorfrancis.com/chapters/edit/10.4324/9781003766667-15/subject-topic-new-typology-language-charles-li-sandra-thompson)，[Li & Thompson 对普通话的论述](https://lrc.la.utexas.edu/books/typology/5-mandarin)。该观点影响大但有争议：[2021 年综述](https://doi.org/10.1353/jcl.2021.0010)。所以只能当参考，不能当定论 | 已证实（该论断存在且有争议） | 查权威综述后引用 |
| 信息结构 | 新旧信息排序、焦点 | 方向 | 未证实 | 同上 |

## 二、其他语系方案
| 条目 | 目标 | 依据 | 状态 | 下一步 |
|---|---|---|---|---|
| 日文原项目 | 借鉴规则分层、评测方式 | 原仓库存在（MIT），已读其 LICENSE | 已证实（存在与许可） | 通读其 docs/evals，列可迁移项 |
| 英文 plain language 运动 | 借鉴「平实写作」指南 | 美国《Plain Writing Act of 2010》（Public Law 111-274）：[法律原文](https://www.govinfo.gov/content/pkg/PLAW-111publ274/pdf/PLAW-111publ274.pdf)；[Federal Plain Language Guidelines（2011）](https://ies.ed.gov/sites/default/files/rel-central/document/2024/10/Federal%20Plain%20Language%20Guidelines.pdf)；[Digital.gov 原则](https://digital.gov/guides/plain-language/principles)。指南条目尚未逐条摘要 | 已证实（法律与指南存在）；逐条摘要未做 | 查官方指南原文后摘要 |
| 各语种可读性研究 | 对比方法 | 方向 | 未证实 | 文献检索 |

## 三、中国汉字研究
| 条目 | 目标 | 依据 | 状态 | 下一步 |
|---|---|---|---|---|
| 常用字表 | 标出生僻字、提示替换 | 《通用规范汉字表》：国务院通知（国发〔2013〕23号，落款 2013-06-05），[中国政府网](https://www.gov.cn/gongbao/content/2013/content_2481095.htm)；收字 8105 个，一级 3500、二级 3000、三级 1605：[教育部](https://www.moe.gov.cn/jyb_xwfb/xw_fbh/moe_2069/s7135/s7562/s7569/201308/t20130827_156353.html)。注：教育部另一页写 2013-08-19 发布通知，落款与公布日期不同，引用时需注明 | 已证实 | 取官方原表，写入数据文件并标来源与许可 |
| 字频 | 用频率判断难字 | 方法常见，语料选择影响大 | 推测 | 选公开语料自行统计并记录 |
| 字形 | 简繁、异体处理 | 方向 | 未证实 | 先列需求 |
| 可读性公式在中文的适用性 | 评估现有公式是否可用 | 英文公式基于词/音节，不能直接套用，属推断；中文研究待查 | 推测 | 收集带难度标注的文本，检验相关性 |

## 四、古汉语场景
| 条目 | 目标 | 依据 | 状态 | 下一步 |
|---|---|---|---|---|
| 文白转换 | 译文不加不减 | 与本项目「不加信息」规则同向 | 推测 | 建小测试集，人工对照 |
| 断句标点 | 辅助标点 | 方向 | 未证实 | 调研现有开源工具，评估再决定 |
| 典故保真 | 不改写典故本意 | 方向 | 推测 | 规则：典故只标注不改写 |

## 五、场景适配
| 场景 | 目标 | 依据 | 状态 | 下一步 |
|---|---|---|---|---|
| 公文 | 保留规范套语，只删空话 | 公文有固定格式，需区分「必要套语」与「AI 套话」 | 推测 | 找真实公文样例，建白名单 |
| 技术文档 | 术语不改 | 同上 | 推测 | 术语表豁免机制 |
| PR/提交信息 | 简短、写清改了什么 | 实践经验 | 推测 | 在自己仓库试用 |
| 邮件 | 去客套堆砌，保留礼貌 | 同上 | 推测 | 试用并看用户反馈 |
| 论文摘要 | 数字与结论不变 | 与核心规则一致 | 推测 | 用已发表摘要做前后对照 |
| 客服 | 语气温和与平实平衡 | 方向 | 未证实 | 收集语料后评估 |

## 近期优先
1. 扩词表（需真实语料；目前新增词仅凭常见印象，未经语料验证）。
2. 做 30 段人写/AI 文标注集，校准阈值（现有 11 段自拟样本，见 docs/TUNING.md）。
3. 豁免机制：代码块、行内代码、引用、用法说明已做；术语表豁免未做。
