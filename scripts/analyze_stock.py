#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个股综合分析脚本（增强版）
结合新闻、股价、趋势等多维度分析单只股票
支持从财经网站抓取新闻
"""

import sys
import json
import re
from datetime import datetime
from typing import Dict, List, Optional

class StockNewsAnalyzer:
    """个股分析器（含新闻抓取）"""

    def __init__(self, stock_code: str, stock_name: str = ""):
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.news_items = []

    def analyze(self) -> Dict:
        """执行完整分析"""
        result = {
            "股票代码": self.stock_code,
            "股票名称": self.stock_name,
            "分析时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "基本信息": {},
            "技术指标": {},
            "新闻分析": [],
            "综合评估": {},
            "操作建议": ""
        }

        # 1. 基本信息分析
        print(f"\n{'='*60}")
        print(f"📊 {self.stock_name} ({self.stock_code}) 个股分析")
        print(f"{'='*60}\n")

        print("1️⃣ 正在获取基本信息...")
        basic_info = self._get_basic_info()
        result["基本信息"] = basic_info

        # 2. 技术指标分析
        print("\n2️⃣ 正在分析技术指标...")
        tech_analysis = self._analyze_technical()
        result["技术指标"] = tech_analysis

        # 3. 新闻分析
        print("\n3️⃣ 正在获取相关新闻...")
        print("   提示：新闻分析需要使用 OpenClaw 的 web_fetch 工具")
        print("   建议新闻来源：财联社、同花顺、新浪财经")
        news = self._get_news_hints()
        result["新闻分析"] = news

        # 4. 综合评估
        print("\n4️⃣ 正在生成综合评估...")
        evaluation = self._evaluate(result)
        result["综合评估"] = evaluation

        # 5. 操作建议
        result["操作建议"] = self._generate_suggestion(evaluation)

        return result

    def _get_basic_info(self) -> Dict:
        """获取基本信息"""
        try:
            import akshare as ak

            # 获取个股信息
            try:
                stock_info = ak.stock_individual_info_em(symbol=self.stock_code)
                info_dict = {}
                for _, row in stock_info.iterrows():
                    info_dict[row['item']] = row['value']

                return {
                    "行业": info_dict.get("行业", "未知"),
                    "市值": info_dict.get("总市值", "未知"),
                    "PE(TTM)": info_dict.get("市盈率(动态)", "未知"),
                    "PB": info_dict.get("市净率", "未知"),
                    "主营业务": info_dict.get("经营范围", "未知")[:50] + "..."
                }
            except:
                return {
                    "行业": "待查询",
                    "市值": "待查询",
                    "PE": "待查询",
                    "PB": "待查询",
                    "主营业务": "待查询（请访问财经网站）"
                }

        except Exception as e:
            return {
                "错误": f"获取基本信息失败: {str(e)}",
                "建议": "请检查 akshare 是否正确安装"
            }

    def _analyze_technical(self) -> Dict:
        """技术指标分析"""
        try:
            import akshare as ak

            # 获取历史数据
            hist_data = ak.stock_zh_a_hist(
                symbol=self.stock_code,
                period="daily",
                adjust="qfq"
            )

            if hist_data.empty or len(hist_data) < 20:
                return {"错误": "历史数据不足（少于20天）"}

            # 最新数据
            latest = hist_data.iloc[-1]
            closes = hist_data['收盘'].astype(float).tail(20)

            # 计算均线
            ma5 = closes.tail(5).mean()
            ma10 = closes.tail(10).mean()
            ma20 = closes.tail(20).mean()

            latest_price = float(latest['收盘'])
            high = float(latest['最高'])
            low = float(latest['最低'])
            volume = float(latest['成交量'])

            # 涨跌幅
            change_pct = float(latest.get('涨跌幅', 0))

            # 趋势判断
            if ma5 > ma10 > ma20 and latest_price > ma5:
                trend = "多头排列"
                trend_emoji = "📈"
                strength = 5
                suggestion_short = "持有/加仓"
            elif ma5 > ma10 and latest_price > ma5:
                trend = "偏多"
                trend_emoji = "↗️"
                strength = 4
                suggestion_short = "持有/轻仓加仓"
            elif ma5 < ma10 < ma20 and latest_price < ma5:
                trend = "空头排列"
                trend_emoji = "📉"
                strength = 1
                suggestion_short = "观望/减仓"
            elif ma5 < ma10 and latest_price < ma5:
                trend = "偏空"
                trend_emoji = "↘️"
                strength = 2
                suggestion_short = "观望"
            else:
                trend = "震荡"
                trend_emoji = "↔️"
                strength = 3
                suggestion_short = "观望"

            # 支撑阻力位
            recent_high = closes.max()
            recent_low = closes.min()

            # 成交量分析
            avg_volume = hist_data['成交量'].astype(float).tail(20).mean()
            volume_ratio = volume / avg_volume if avg_volume > 0 else 1

            return {
                "最新价": f"{latest_price:.2f}",
                "涨跌幅": f"{change_pct:+.2f}%",
                "成交量": f"{volume/10000:.2f}万手",
                "量比": f"{volume_ratio:.2f}",
                "MA5": f"{ma5:.2f}",
                "MA10": f"{ma10:.2f}",
                "MA20": f"{ma20:.2f}",
                "趋势": f"{trend} {trend_emoji}",
                "趋势强度": strength,
                "短期建议": suggestion_short,
                "强支撑": f"{low:.2f}",
                "弱支撑": f"{min(ma5, ma10):.2f}",
                "弱阻力": f"{high:.2f}",
                "强阻力": f"{recent_high:.2f}",
                "买入区间": f"{min(ma5, ma10, ma20):.2f} - {max(ma5, ma10, ma20):.2f}",
                "止损价": f"{recent_low * 0.97:.2f}",
                "目标价1": f"{recent_high:.2f}",
                "目标价2": f"{latest_price * 1.10:.2f}"
            }

        except Exception as e:
            return {
                "错误": f"技术分析失败: {str(e)}",
                "建议": "请检查网络连接或稍后重试"
            }

    def _get_news_hints(self) -> List[Dict]:
        """获取新闻提示（不直接抓取，返回建议）"""
        return [
            {
                "提示": "建议使用 OpenClaw web_fetch 工具抓取新闻",
                "来源1": f"https://finance.sina.com.cn/realstock/company/{self._get_sina_code()}/nc.shtml",
                "来源2": f"https://www.cls.cn/search?keyword={self.stock_name}",
                "来源3": f"https://www.10jqka.com.cn/",
                "分析建议": "关注：股东增减持、业绩预告、重大合同、行业政策等"
            }
        ]

    def _get_sina_code(self) -> str:
        """获取新浪财经格式的股票代码"""
        if self.stock_code.startswith('6'):
            return f"sh{self.stock_code}"
        else:
            return f"sz{self.stock_code}"

    def _evaluate(self, result: Dict) -> Dict:
        """综合评估"""
        tech = result.get("技术指标", {})

        # 技术面评分
        tech_score = tech.get("趋势强度", 3)

        # 成交量评分
        volume_ratio = float(tech.get("量比", "1.0").replace(" ", ""))
        if volume_ratio > 2:
            volume_score = 5  # 放量
        elif volume_ratio > 1.5:
            volume_score = 4  # 温和放量
        elif volume_ratio > 0.8:
            volume_score = 3  # 正常
        else:
            volume_score = 2  # 缩量

        # 综合评分（技术面权重60%，成交量权重40%）
        total_score = tech_score * 0.6 + volume_score * 0.4

        # 风险等级
        if total_score >= 4:
            risk = "低风险"
            risk_emoji = "🟢"
        elif total_score >= 3:
            risk = "中等风险"
            risk_emoji = "🟡"
        else:
            risk = "高风险"
            risk_emoji = "🔴"

        return {
            "技术面评分": f"{tech_score}/5",
            "成交量评分": f"{volume_score}/5",
            "综合评分": f"{total_score:.1f}/5.0",
            "风险等级": f"{risk} {risk_emoji}",
            "投资周期建议": "中长期" if tech_score >= 4 else "短期观望",
            "适合投资者": "激进型+稳健型" if total_score >= 4 else "仅激进型" if total_score >= 3 else "不建议"
        }

    def _generate_suggestion(self, evaluation: Dict) -> str:
        """生成操作建议"""
        score = float(evaluation.get("综合评分", "3.0").split("/")[0])

        if score >= 4.5:
            return "✅ 强烈推荐 | 逢低加仓，中长期持有，设置止损"
        elif score >= 4.0:
            return "✅ 推荐 | 支撑位附近建仓，设置止损，分批买入"
        elif score >= 3.5:
            return "⚠️ 谨慎 | 观望为主，可轻仓试探，严格止损"
        elif score >= 3.0:
            return "⚠️ 观望 | 等待更好入场点，关注支撑位企稳信号"
        elif score >= 2.0:
            return "❌ 不推荐 | 空头趋势，建议回避或减仓"
        else:
            return "❌ 强烈不推荐 | 风险较大，不建议介入"

    def print_report(self, result: Dict):
        """打印分析报告"""
        print(f"\n{'='*60}")
        print(f"📊 {result['股票名称']} ({result['股票代码']}) 分析报告")
        print(f"{'='*60}\n")

        # 基本信息
        print("📋 基本信息:")
        basic = result["基本信息"]
        if "错误" in basic:
            print(f"  ⚠️  {basic['错误']}")
        else:
            for k, v in basic.items():
                print(f"  {k}: {v}")

        # 技术指标
        print(f"\n📈 技术指标:")
        tech = result["技术指标"]
        if "错误" in tech:
            print(f"  ❌ {tech['错误']}")
            if "建议" in tech:
                print(f"  💡 {tech['建议']}")
        else:
            print(f"  最新价: {tech.get('最新价', 'N/A')} ({tech.get('涨跌幅', 'N/A')})")
            print(f"  成交量: {tech.get('成交量', 'N/A')} (量比: {tech.get('量比', 'N/A')})")
            print(f"  趋势: {tech.get('趋势', 'N/A')}")
            print(f"  MA5: {tech.get('MA5', 'N/A')} | MA10: {tech.get('MA10', 'N/A')} | MA20: {tech.get('MA20', 'N/A')}")
            print(f"  买入区间: {tech.get('买入区间', 'N/A')}")
            print(f"  止损价: {tech.get('止损价', 'N/A')}")
            print(f"  目标价: {tech.get('目标价1', 'N/A')} / {tech.get('目标价2', 'N/A')}")
            print(f"  短期建议: {tech.get('短期建议', 'N/A')}")

        # 新闻提示
        print(f"\n📰 新闻分析提示:")
        for news in result["新闻分析"]:
            if "提示" in news:
                print(f"  {news['提示']}")
                print(f"  来源1: {news['来源1']}")
                print(f"  来源2: {news['来源2']}")
                print(f"  分析建议: {news['分析建议']}")

        # 综合评估
        print(f"\n📊 综合评估:")
        eval_data = result["综合评估"]
        print(f"  技术面: {eval_data['技术面评分']}")
        print(f"  成交量: {eval_data['成交量评分']}")
        print(f"  综合评分: {eval_data['综合评分']}")
        print(f"  风险等级: {eval_data['风险等级']}")
        print(f"  投资周期: {eval_data['投资周期建议']}")
        print(f"  适合投资者: {eval_data['适合投资者']}")

        # 操作建议
        print(f"\n💡 操作建议:")
        print(f"  {result['操作建议']}")

        # 风险提示
        print(f"\n⚠️  风险提示:")
        print(f"  以上分析基于技术指标，不构成投资建议")
        print(f"  股市有风险，投资需谨慎")
        print(f"  建议结合基本面和新闻面综合判断")

        print(f"\n{'='*60}\n")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 analyze_stock.py <股票代码> [股票名称]")
        print("示例: python3 analyze_stock.py 002101 广东鸿图")
        print("      python3 analyze_stock.py 601857 中国石油")
        sys.exit(1)

    stock_code = sys.argv[1]
    stock_name = sys.argv[2] if len(sys.argv) > 2 else ""

    # 创建分析器
    analyzer = StockNewsAnalyzer(stock_code, stock_name)

    # 执行分析
    result = analyzer.analyze()

    # 打印报告
    analyzer.print_report(result)

    # 可选：保存为JSON
    output_file = f"/tmp/{stock_code}_analysis.json"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"📁 分析结果已保存: {output_file}")
    except:
        pass

if __name__ == "__main__":
    main()
