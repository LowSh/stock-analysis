# Stock Analysis Skill 📈

OpenClaw 技能：股票市场分析和日志记录工具

## 功能特性

- ✅ **自动获取财经日历** - 从财联社、同花顺抓取重要事件
- ✅ **热门新闻追踪** - 实时获取市场热点
- ✅ **事件驱动分析** - 识别板块机会
- ✅ **技术分析** - MA均线、买入卖出建议
- ✅ **推荐股票** - 每个板块推荐3只股票（含技术指标）
- ✅ **持仓追踪** - 个人持仓分析和相关新闻

## 安装

### 方法1：下载 .skill 文件

1. 下载 `stock-analysis.skill` 文件
2. 放到 `~/.openclaw/skills/` 目录
3. 重启 OpenClaw

### 方法2：从源码安装

```bash
git clone https://github.com/你的用户名/stock-analysis.git
cd stock-analysis
# 使用 OpenClaw 打包
python3 /opt/homebrew/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py . ~/.openclaw/skills
```

## 使用方法

对 OpenClaw 说：
- "更新股票日志"
- "分析一下热门板块"
- "推荐几只股票"
- "今天的股票新闻也更新一下"

## 日志文件

默认位置：`~/Desktop/claw实验/股票分析日志.md`

## 数据来源

| 来源 | 用途 |
|------|------|
| 财联社 (cls.cn) | 财经日历、重要事件 |
| 同花顺 (10jqka.com.cn) | 热门新闻、点击排行 |
| akshare | 股票技术数据 |

## 技术分析

使用 `scripts/stock_analyzer.py` 自动获取：

- 现价、涨跌幅
- MA5/MA10/MA20 均线
- 支撑位、阻力位
- 买入区间、止损价、目标价
- 趋势判断（多头/空头/震荡）
- 操作建议

### 运行技术分析

```bash
python3 scripts/stock_analyzer.py
```

## 文件结构

```
stock-analysis/
├── SKILL.md              # 技能工作流程
├── README.md             # 说明文档
├── references/
│   ├── sectors.md        # 热门板块参考
│   └── stocks.md         # 股票代码参考
└── scripts/
    └── stock_analyzer.py # 技术分析脚本
```

## 自定义配置

### 修改持仓股票

编辑 `references/stocks.md`，在"用户持仓"部分添加你的股票。

### 修改日志位置

在 `SKILL.md` 中修改日志文件路径。

## 依赖

- Python 3.9+
- akshare (`pip3 install akshare`)

## 注意事项

⚠️ **风险提示**：以上分析基于公开事件和技术指标，不构成投资建议。投资有风险，入市需谨慎。

## License

MIT

## 作者

由 OpenClaw 创建

---

🦞 [OpenClaw](https://openclaw.ai) - Your AI Assistant
