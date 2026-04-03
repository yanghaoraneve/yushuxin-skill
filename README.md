# 虞书欣 Esther 数字人格 Skill

> 「我是虞书欣，你们的小鱼～」

## 🌸 简介

虞书欣（Esther）数字人格对话系统，基于 MiniMax M2.7 模型驱动。

**功能：**
- 虞书欣本人人格对话（小鱼/欣欣风格）
- 8个角色人格切换（小兰花、初礼、凌妙妙、越祈等）
- 完整台词本知识库（177KB+角色台词）
- 网易云歌词 + 微博动态 + 热评数据

## 🚀 快速启动

### 1. 克隆仓库
```bash
git clone https://github.com/yanghaoraneve/yushuxin-skill.git
cd yushuxin-skill
```

### 2. 配置 API Key
```bash
# 方式1：复制环境变量示例文件
cp .env.example .env

# 方式2：直接设置环境变量
export MINIMAX_API_KEY=你的key
```

> 获取 API Key：https://platform.minimaxi.com

### 3. 启动对话前端
```bash
cd frontend
python3 server.py
```

然后打开浏览器访问：**http://localhost:18798**

## ⚠️ 重要说明

**API Key 需要自行提供**，本项目不包含 API Key。

获取方式：
1. 访问 [MiniMax 开放平台](https://platform.minimaxi.com)
2. 注册/登录账号
3. 在控制台创建 API Key

## 📁 目录结构

```
yushuxin-skill/
├── SKILL.md              # Skill 入口定义
├── meta.json             # 元数据
├── persona/
│   └── persona.md        # 完整人格描述（8角色分析）
├── frontend/
│   └── server.py        # 对话前端（需配API Key）
├── knowledge/           # 知识库
│   ├── 苍兰诀_小兰花台词本.txt
│   ├── 月光变奏曲_初礼台词本.txt
│   ├── 永夜星河_凌妙妙台词本.txt
│   └── ...（共8个角色台词 + 歌词 + 微博 + 评论）
├── .env.example        # 环境变量示例
└── .gitignore          # 保护敏感文件不上传
```

## 📖 角色列表

| 角色 | 剧集 | 风格 |
|------|------|------|
| 小兰花 | 苍兰诀 | 「本座」腔，软萌笨蛋仙女 |
| 初礼 | 月光变奏曲 | 元气追梦少女 |
| 虞美人 | 两个人的小森林 | 傲娇美妆博主 |
| 凌妙妙 | 永夜星河 | 系统播报腔穿书女主 |
| 越祈 | 祈今朝 | 「今朝」依赖症吃货 |
| 卫枝 | 嘘国王在冬眠 | 元气村花 |
| 云为衫 | 云之羽 | 神秘冷静刺客 |
| 姜暮 | 温暖的甜蜜的 | 都市成熟女性 |

## 🔒 安全说明

- `.env` 文件包含 API Key，**永远不会提交到 GitHub**
- `.gitignore` 已配置保护所有敏感文件
- 生产环境建议通过环境变量注入 API Key

## 📄 License

MIT
