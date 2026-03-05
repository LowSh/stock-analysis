# Stock Analysis Skill - 使用指南

## 📋 目录结构

```
~/.openclaw/skills/stock-analysis/
├── SKILL.md                    # 主文档（工作流程、数据源、板块分析）
├── TECHNICAL_DATA.md           # 技术数据获取说明（akshare接口问题）
├── scripts/
│   ├── analyze_sector.py       # 板块分析框架
│   └── update_holdings.py      # 更新持仓数据脚本
└── README.md                   # 本文档
```

## 🚀 快速开始

### 1. 更新股票分析日志

**对我说：**
- "更新股票分析日志"
- "今天的股票新闻也更新一下"

**我会：**
1. 抓取最新财经新闻
2. 分析热门板块
3. 更新日志文件（`~/Desktop/claw实验/股票分析日志.md`）

### 2. 更新持仓数据

**手动运行：**
```bash
python3 ~/.openclaw/skills/stock-analysis/scripts/update_holdings.py
```

**输出：**
- 控制台：JSON格式数据
- 文件：`~/Desktop/claw实验/持仓数据.csv`

### 3. 分析板块

**对我说：**
- "分析一下AI板块"
- "帮我看看黄金板块"

**我会：**
1. 运行板块分析脚本
2. 抓取实时新闻
3. 生成完整分析报告

## ⚠️ 已知问题

### akshare接口不稳定

**症状：**
- 连接中断（`RemoteDisconnected`）
- 实时行情接口失败
- 需要多次重试

**解决方案：**
1. **方案1：** 使用 `update_holdings.py` 脚本（自动重试）
2. **方案2：** 手动查询（东方财富/同花顺网站）
3. **方案3：** 浏览器自动化（待实现）

**详细说明：** 查看 `TECHNICAL_DATA.md`

### 不要使用昨天的涨幅数据

**重要提醒：**
- ✅ 只更新今日的新闻和事件
- ✅ 实时涨幅需要盘中获取
- ❌ 不要把昨天的涨幅数据用于今日日志

## 📊 输出文件

| 文件 | 位置 | 说明 |
|------|------|------|
| 股票分析日志 | `~/Desktop/claw实验/股票分析日志.md` | 完整日志（含持仓、新闻、板块分析） |
| 公众号版本 | `~/Desktop/claw实验/股票分析日志_公众号版.md` | 公众号优化版（无个人持仓） |
| 持仓数据 | `~/Desktop/claw实验/持仓数据.csv` | 持仓股票实时数据 |
| 核心内容存档 | `~/Desktop/claw实验/公众号核心内容存档.md` | 持续跟踪的重大事件 |

## 🔧 配置

### 持仓股票

**文件：** `scripts/update_holdings.py`

**修改方法：**
```python
HOLDINGS = [
    {"code": "002738", "name": "中矿资源"},
    {"code": "600821", "name": "金开新能"},
    {"code": "601975", "name": "招商南油"},
]
```

### 数据源

**主要数据源：**
- 财联社 (cls.cn)
- 同花顺 (10jqka.com.cn)
- 东方财富 (eastmoney.com)
- akshare（技术数据）

## 📱 相关Skill

- **stock-analysis** - 股票分析日志（完整版，含个人持仓）
- **stock-wechat** - 公众号版本（无个人持仓，自动推送）

## 📞 技术支持

**文档：**
- 主文档：`SKILL.md`
- 技术数据：`TECHNICAL_DATA.md`
- 本文档：`README.md`

**日志文件：**
- `~/Desktop/claw实验/股票分析日志.md`
- `~/.openclaw/workspace/memory/2026-03-03.md`

---

_最后更新：2026-03-03 12:50_
