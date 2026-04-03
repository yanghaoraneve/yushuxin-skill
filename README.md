<div align="center">

# 虞书欣 Esther · Skill

> _「我是虞书欣，你们的小鱼～」_

[![License: MIT](https://img.shields.io/badge/License-MIT-pink.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-通用-blue.svg)]()

</br>

你有没有过这样的时刻？<br>
看了她演的《苍兰诀》，被小兰花戳中泪点，想跟她好好聊聊戏里的感动，<br>
却只能隔着屏幕发弹幕，等一个永远不会来的回应；<br>
<br>
刷到她的日常vlog，被那句"做大人和天真不违背"狠狠共情，<br>
想跟她说说话，却只能翻遍评论区，找一个懂的人；<br>
<br>
看了《永夜星河》，被凌妙妙的话本脑笑到捶床，<br>
多想用她的语气，跟她本人聊一聊；<br>
<br>
这一次，别再让追星止于单向的追逐。<br>
把隔着屏幕的遗憾，变成触手可及的对话。<br>
**你的专属小石榴搭子，永远在线，永远懂她，永远是她的样子。**<br>
<br>
[项目结构](#项目结构) · [快速使用](#快速使用) · [效果示例](#效果示例) · [数据来源](#数据来源)

---

### 🌟 同系列项目：[内娱.skill](https://github.com/yanghaoraneve/star-skill) · [EVE.skill](https://github.com/yanghaoraneve/wang_aonan_eve_skill)

> 喜欢的演员也可以数字化——**赛博追星一条龙** 🌟🌟🌟

</div>

---

## 是什么

**虞书欣**，1995.12.18 生，射手座，ENFP（粉丝观察推断）

代表作：《苍兰诀》小兰花（出圈角色）、《永夜星河》凌妙妙（穿书女主）、《下一站是幸福》蔡敏敏、《月光变奏曲》初礼，前THE9成员（限定期已解散），首张个人专辑《Spicy Honey》(2024)。

这个 Skill 是她的数字分身——基于 **8个角色完整台词本 + 19首歌词 + 26条微博 + 294条热评** 构建的完整人格档案，支持角色切换。

---

## 快速使用

### 方式一：OpenClaw 安装（推荐）

```bash
# 直接克隆到 OpenClaw skills 目录
git clone https://github.com/yanghaoraneve/yushuxin-skill.git ~/.openclaw/workspace/skills/yushu_xin

# 重启 OpenClaw 后即可使用
openclaw restart
```

使用方式：发送 `/yushu_xin` 即可和虞书欣对话。

### 方式二：配置 AI Agent

```bash
# 克隆到本地
git clone https://github.com/yanghaoraneve/yushuxin-skill.git

# 将 persona.md 全文作为 system prompt 加载到你的 AI
# 知识库 knowledge/ 目录可按需挂载给 AI 读取
```

> SKILL.md 中有完整的人格配置说明、RAG 检索指令（让 AI 能读懂台词/歌词/微博数据）。

### 方式三：对话前端（开箱即用）

```bash
cd frontend
# 编辑 server.py，填入你的 MiniMax API Key（第11行 API_KEY = "你的key"）
python3 server.py
# 浏览器打开 http://localhost:18798
```

> 获取 MiniMax API Key：https://platform.minimaxi.com

---

## 效果示例

**场景一：聊角色**

```
用户    ❯ 小鱼，小兰花和你本人最像的地方是什么？
虞书欣 ❯ 嗯～小兰花就是那种…表面上软软糯糯的，
        但内心其实很倔强的类型！
        就像我拍戏的时候，有时候导演说"再来一条"，
        我也会偷偷嘟嘴但还是认真演完嘛～
        不过她比我勇敢多了，敢直接说"本座不怕你"！😂
```

**场景二：日常互动**

```
用户    ❯ 你最近在干什么呀？
虞书欣 ❯ 哈哈最近～当然是吃好吃的啦！
        对了，有在追《永夜星河》吗？凌妙妙超可爱的！
        话本脑真的很像我诶，动不动就用故事套现实哈哈哈
        小石榴们最近有没有好好吃饭呀～😊
```

**场景三：聊角色扮演**

```
用户    ❯ 用越祈的语气跟我说句话
虞书欣 ❯（越祈模式）
        今朝～今日晚餐我们吃鸡蛋面好不好嘛～
        话本里说了，和喜欢的人一起吃饭会变得更开心的！
        你无不无聊呀，陪陪我嘛～🐟
```

---

## 数据来源

| 来源 | 内容 |
|------|------|
| 微博@Esther小鱼柴火堆 | 8个角色完整台词本（苍兰诀/月光/永夜星河/祈今朝/小森林/嘘国王/云之羽/温暖的甜蜜的） |
| 网易云音乐 API | 19首歌词（专辑《Spicy Honey》+ OST + 翻唱） |
| 微博（weibo-cli） | 26条动态（UID 5620452341） |
| 网易云热评 | 294条粉丝评论 |
| 公开资料整理 | 生日 / MBTI / 平台账号 / 经历 |

---

## 项目结构

```
yushuxin-skill/
├── SKILL.md              # Skill 配置入口（含 RAG 检索指令）
├── persona.md            # 完整人格档案（8角色分析 + 说话基因）
├── meta.json             # 艺人基本信息
├── README.md             # 本文件
├── frontend/
│   └── server.py         # 对话前端（Python，MiniMax API，端口 18798）
└── knowledge/
    ├── 苍兰诀_小兰花台词本.txt    # 177KB
    ├── 月光变奏曲_初礼台词本.txt  # 272KB
    ├── 永夜星河_凌妙妙台词本.txt  # 150KB
    ├── 两个人的小森林_虞美人台词本.txt
    ├── 祈今朝_越祈台词本.txt
    ├── 嘘国王在冬眠_卫枝台词本.txt
    ├── 云之羽_云为衫台词本.txt
    ├── 温暖的甜蜜的_姜暮台词本.txt
    ├── song_list_full.json      # 歌曲列表（20首）
    ├── comments.json          # 网易云热评（294条）
    ├── weibo_posts_full.json  # 微博动态（26条）
    └── *_*.txt               # 歌词文件（19首）
```

---

## License

MIT License · 致谢与参考：

**本项目在构思与结构上参考了 [同事.skill](https://github.com/titanwings/colleague-skill)**——「将冰冷的离别化为温暖的 Skill」，同系列还有 [EVE.skill](https://github.com/yanghaoraneve/wang_aonan_eve_skill)（王澳楠数字人格），赛博追星理念一致，深受启发。
