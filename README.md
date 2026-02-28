# Stock WeChat Skill

微信公众号版股票分析日报生成器

## 📦 功能特点

- ✅ **公众号优化格式** - 标题吸睛、分段清晰、emoji丰富
- ✅ **无个人持仓** - 自动去除个人持仓信息，适合公开分享
- ✅ **简洁内容** - 重点突出，适合移动端阅读
- ✅ **热点聚焦** - 突出当日重大事件和热门板块
- ✅ **定时更新** - 支持自动定时更新（可开启/关闭）
- ✅ **夜间模式** - 00:00-08:00 不自动更新

## 🚀 安装

### 方法 1：直接下载

```bash
cd ~/.openclaw/skills
git clone -b stock-wechat https://github.com/LowSh/stock-analysis.git stock-wechat
```

### 方法 2：手动安装

```bash
# 下载文件
cd ~/.openclaw/skills
mkdir -p stock-wechat
cd stock-wechat

# 下载 SKILL.md
curl -O https://raw.githubusercontent.com/LowSh/stock-analysis/stock-wechat/SKILL.md

# 下载脚本
mkdir -p scripts
curl -o scripts/schedule_manager.sh https://raw.githubusercontent.com/LowSh/stock-analysis/stock-wechat/scripts/schedule_manager.sh
chmod +x scripts/schedule_manager.sh
```

## 📖 使用方法

### 生成公众号版股票分析

**用户说：**
- "生成公众号版股票分析"
- "更新公众号内容"
- "帮我生成适合微信发布的股票日报"

### 定时任务管理

**查看状态：**
```bash
~/.openclaw/skills/stock-wechat/scripts/schedule_manager.sh status
```

**开启定时（每4小时）：**
```bash
~/.openclaw/skills/stock-wechat/scripts/schedule_manager.sh enable
```

**关闭定时：**
```bash
~/.openclaw/skills/stock-wechat/scripts/schedule_manager.sh disable
```

**设置频率：**
```bash
# 每2小时
~/.openclaw/skills/stock-wechat/scripts/schedule_manager.sh set-frequency 2h

# 每天9点
~/.openclaw/skills/stock-wechat/scripts/schedule_manager.sh set-frequency "0 9 * * *"
```

## 📂 文件结构

```
stock-wechat/
├── SKILL.md                      # Skill 说明文件
├── scripts/
│   └── schedule_manager.sh       # 定时任务管理脚本
└── README.md                     # 本文件
```

## 🔗 相关 Skill

- **stock-analysis** (main 分支) - 完整版股票分析（含个人持仓）
- **stock-wechat** (当前分支) - 公众号版（无个人持仓）

## 📊 与 stock-analysis 的关系

| Skill | 功能 | 包含个人持仓 | 用途 |
|-------|------|-------------|------|
| **stock-analysis** | 完整日志 | ✅ 是 | 个人参考 |
| **stock-wechat** | 公众号版 | ❌ 否 | 公开分享 |

**推荐工作流：**
1. 先运行 `stock-analysis` 更新完整日志
2. 再运行 `stock-wechat` 生成公众号版本

## 🌙 夜间模式

为了避免打扰，定时任务在 **00:00-08:00** 不自动更新。

如果在此期间手动触发，会自动延迟到 08:00 执行。

## 📅 输出示例

**标题：**
```
📈 股票日报 | 2月28日：中东冲突升级，这些板块要火！
```

**内容结构：**
1. 🔥 今日大事
2. 📅 明天重点关注
3. 🚀 近期热门板块
4. 💰 买入卖出建议
5. 📅 重要事件日历
6. ⚠️ 风险提示

## 🔧 依赖

**必需：**
- OpenClaw (内置 `web_fetch` 和 `openclaw cron` 命令)

**可选：**
- stock-analysis (如需技术分析数据)

## 📝 更新日志

### v1.0.0 (2026-02-28)
- ✅ 初始版本
- ✅ 公众号优化格式
- ✅ 定时任务管理
- ✅ 夜间模式
- ✅ 避免个人持仓泄露

## 📄 许可证

MIT License

## 👤 作者

- GitHub: [@LowSh](https://github.com/LowSh)
- Skill by OpenClaw 🦞

---

**觉得有用？给个 Star ⭐ 吧！**
