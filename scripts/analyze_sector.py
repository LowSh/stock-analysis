#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
板块分析脚本
结合新闻、政策、龙头股等多维度分析板块
"""

import sys
import json
from datetime import datetime
from typing import Dict, List, Optional

class SectorAnalyzer:
    """板块分析器"""

    def __init__(self, sector_name: str):
        self.sector_name = sector_name
        self.sector_data = self._get_sector_mapping()

    def _get_sector_mapping(self) -> Dict:
        """板块映射（包含龙头股、ETF等）"""
        sectors = {
            "AI": {
                "全名": "人工智能",
                "龙头股": [
                    {"股票": "寒武纪", "代码": "688256", "说明": "AI芯片龙头"},
                    {"股票": "中科曙光", "代码": "603019", "说明": "算力基础设施"},
                    {"股票": "科大讯飞", "代码": "002230", "说明": "语音识别"},
                ],
                "ETF": "515070 (AI龙头ETF)",
                "政策支持": "✅ 国家战略新兴产业",
                "市场空间": "万亿级",
                "关键词": ["GPT", "大模型", "算力", "AI芯片"]
            },
            "半导体": {
                "全名": "半导体/集成电路",
                "龙头股": [
                    {"股票": "中芯国际", "代码": "688981", "说明": "晶圆代工"},
                    {"股票": "北方华创", "代码": "002371", "说明": "半导体设备"},
                    {"股票": "韦尔股份", "代码": "603501", "说明": "芯片设计"},
                ],
                "ETF": "512480 (半导体ETF)",
                "政策支持": "✅ 国产替代",
                "市场空间": "5000亿+",
                "关键词": ["芯片", "晶圆", "设备", "国产替代"]
            },
            "新能源汽车": {
                "全名": "新能源汽车",
                "龙头股": [
                    {"股票": "比亚迪", "代码": "002594", "说明": "整车制造"},
                    {"股票": "宁德时代", "代码": "300750", "说明": "动力电池"},
                    {"股票": "恩捷股份", "代码": "002812", "说明": "隔膜"},
                ],
                "ETF": "516390 (新能源汽车ETF)",
                "政策支持": "✅ 补贴+免税",
                "市场空间": "万亿级",
                "关键词": ["电动车", "动力电池", "充电桩"]
            },
            "消费电子": {
                "全名": "消费电子/苹果链",
                "龙头股": [
                    {"股票": "立讯精密", "代码": "002475", "说明": "苹果供应商"},
                    {"股票": "歌尔股份", "代码": "002241", "说明": "声学/AR"},
                    {"股票": "京东方A", "代码": "000725", "说明": "面板"},
                ],
                "ETF": "561100 (消费电子ETF)",
                "政策支持": "✅ 以旧换新",
                "市场空间": "千亿级",
                "关键词": ["苹果", "华为", "手机", "AR/VR"]
            },
            "通信": {
                "全名": "通信/5G",
                "龙头股": [
                    {"股票": "中兴通讯", "代码": "000063", "说明": "5G设备"},
                    {"股票": "烽火通信", "代码": "600498", "说明": "光通信"},
                    {"股票": "华工科技", "代码": "000988", "说明": "光模块"},
                ],
                "ETF": "515880 (通信ETF)",
                "政策支持": "✅ 新基建",
                "市场空间": "千亿级",
                "关键词": ["5G", "6G", "光通信", "MWC"]
            },
            "石油": {
                "全名": "石油/能源",
                "龙头股": [
                    {"股票": "中国石油", "代码": "601857", "说明": "石油龙头"},
                    {"股票": "中国石化", "代码": "600028", "说明": "石化龙头"},
                    {"股票": "海油发展", "代码": "600968", "说明": "油服"},
                ],
                "ETF": "无",
                "政策支持": "✅ 能源安全",
                "市场空间": "万亿级",
                "关键词": ["原油", "OPEC", "油价", "地缘政治"]
            },
            "军工": {
                "全名": "军工/国防",
                "龙头股": [
                    {"股票": "中航沈飞", "代码": "600760", "说明": "战斗机"},
                    {"股票": "航发动力", "代码": "600893", "说明": "航空发动机"},
                    {"股票": "中航西飞", "代码": "000768", "说明": "运输机"},
                ],
                "ETF": "512660 (军工ETF)",
                "政策支持": "✅ 国防建设",
                "市场空间": "千亿级",
                "关键词": ["国防", "军费", "地缘政治"]
            },
            "稀土": {
                "全名": "稀土/有色",
                "龙头股": [
                    {"股票": "北方稀土", "代码": "600111", "说明": "稀土龙头"},
                    {"股票": "盛和资源", "代码": "600392", "说明": "稀土"},
                    {"股票": "五矿稀土", "代码": "000831", "说明": "稀土"},
                ],
                "ETF": "无",
                "政策支持": "✅ 战略资源",
                "市场空间": "百亿级",
                "关键词": ["稀土", "磁材", "出口管制"]
            },
            "低空经济": {
                "全名": "低空经济/飞行汽车",
                "龙头股": [
                    {"股票": "万丰奥威", "代码": "002085", "说明": "飞行汽车龙头"},
                    {"股票": "山河智能", "代码": "002097", "说明": "通用航空"},
                    {"股票": "中信海直", "代码": "000099", "说明": "通航服务"},
                ],
                "ETF": "暂无专门ETF",
                "政策支持": "✅ 2026年国家战略新兴产业",
                "市场空间": "万亿级",
                "关键词": ["eVTOL", "飞行汽车", "通航", "低空旅游"]
            },
            "一体化压铸": {
                "全名": "一体化压铸/汽车零部件",
                "龙头股": [
                    {"股票": "广东鸿图", "代码": "002101", "说明": "一体化压铸"},
                    {"股票": "文灿股份", "代码": "603348", "说明": "一体化压铸"},
                    {"股票": "旭升集团", "代码": "603305", "说明": "汽车零部件"},
                ],
                "ETF": "无",
                "政策支持": "✅ 新能源车轻量化",
                "市场空间": "300亿+",
                "关键词": ["一体化压铸", "轻量化", "特斯拉"]
            }
        }

        # 模糊匹配
        for key, data in sectors.items():
            if key.lower() in self.sector_name.lower() or self.sector_name.lower() in key.lower():
                return {"简称": key, **data}
        
        # 未找到，生成智能建议
        return self._generate_generic_sector()

    def _generate_generic_sector(self) -> Dict:
        """为任意板块生成分析框架"""
        return {
            "简称": self.sector_name,
            "全名": self.sector_name,
            "龙头股": [
                {"股票": "建议查询", "代码": "000000", "说明": "使用东方财富/同花顺查询板块龙头"}
            ],
            "ETF": "建议查询 ETF 代码",
            "政策支持": "建议查询相关政策",
            "市场空间": "建议查询行业报告",
            "关键词": [self.sector_name],
            "is_generic": True  # 标记为通用板块
        }

    def analyze(self) -> Dict:
        """执行完整分析"""
        result = {
            "板块名称": self.sector_name,
            "分析时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "基本信息": {},
            "龙头股分析": [],
            "板块趋势": {},
            "新闻驱动": [],
            "综合评估": {},
            "投资建议": ""
        }

        print(f"\n{'='*60}")
        print(f"📊 {self.sector_name} 板块分析")
        print(f"{'='*60}\n")

        # 1. 基本信息
        print("1️⃣ 正在获取板块基本信息...")
        result["基本信息"] = self._get_basic_info()

        # 2. 龙头股分析
        print("\n2️⃣ 正在分析龙头股...")
        result["龙头股分析"] = self._analyze_leading_stocks()

        # 3. 板块趋势
        print("\n3️⃣ 正在分析板块趋势...")
        result["板块趋势"] = self._analyze_trend()

        # 4. 新闻驱动
        print("\n4️⃣ 正在获取新闻驱动...")
        result["新闻驱动"] = self._get_news_drivers()

        # 5. 综合评估
        print("\n5️⃣ 正在生成综合评估...")
        result["综合评估"] = self._evaluate(result)

        # 6. 投资建议
        result["投资建议"] = self._generate_suggestion(result["综合评估"])

        return result

    def _get_basic_info(self) -> Dict:
        """获取板块基本信息"""
        return {
            "板块全名": self.sector_data.get("全名", "未知"),
            "板块简称": self.sector_data.get("简称", "未知"),
            "ETF代码": self.sector_data.get("ETF", "无"),
            "政策支持": self.sector_data.get("政策支持", "待查询"),
            "市场空间": self.sector_data.get("市场空间", "待查询"),
            "关键词": ", ".join(self.sector_data.get("关键词", []))
        }

    def _analyze_leading_stocks(self) -> List[Dict]:
        """分析龙头股"""
        leaders = self.sector_data.get("龙头股", [])

        results = []
        for stock in leaders[:3]:  # 只分析前3只
            print(f"   分析 {stock['股票']} ({stock['代码']})...")
            result = {
                "股票": stock["股票"],
                "代码": stock["代码"],
                "说明": stock["说明"],
                "技术分析": "建议运行 analyze_stock.py 获取详细数据",
                "重要性": "⭐⭐⭐"
            }
            results.append(result)

        return results

    def _analyze_trend(self) -> Dict:
        """分析板块趋势"""
        # 简化版，实际应获取板块指数数据
        return {
            "趋势判断": "请查看板块指数走势",
            "建议": "关注龙头股走势，龙头强则板块强",
            "关键指标": "板块涨幅、成交量、龙头股表现"
        }

    def _get_news_drivers(self) -> List[Dict]:
        """获取新闻驱动因素"""
        keywords = self.sector_data.get("关键词", [])

        return [
            {
                "类型": "事件驱动",
                "说明": f"关注包含关键词 {', '.join(keywords[:3])} 的新闻",
                "来源建议": "财联社、同花顺、东方财富",
                "分析方法": "利好/利空/中性"
            },
            {
                "类型": "政策驱动",
                "说明": "关注国家政策、行业规划、补贴政策",
                "来源建议": "发改委、工信部官网",
                "分析方法": "政策力度、执行时间"
            }
        ]

    def _evaluate(self, result: Dict) -> Dict:
        """综合评估"""
        # 基于基本信息评估
        policy_support = result["基本信息"].get("政策支持", "")
        market_size = result["基本信息"].get("市场空间", "")

        # 政策评分
        if "✅" in policy_support:
            policy_score = 5
        elif "⚠️" in policy_support:
            policy_score = 3
        else:
            policy_score = 2

        # 市场空间评分
        if "万亿" in market_size:
            market_score = 5
        elif "千亿" in market_size:
            market_score = 4
        elif "百亿" in market_size:
            market_score = 3
        else:
            market_score = 2

        # 综合评分
        total_score = (policy_score + market_score) / 2

        # 热度评级
        if total_score >= 4.5:
            heat = "🔥🔥🔥🔥🔥"
            rating = "极热"
        elif total_score >= 4:
            heat = "🔥🔥🔥🔥"
            rating = "热门"
        elif total_score >= 3:
            heat = "🔥🔥🔥"
            rating = "温热"
        else:
            heat = "🔥🔥"
            rating = "冷门"

        return {
            "政策支持评分": f"{policy_score}/5",
            "市场空间评分": f"{market_score}/5",
            "综合评分": f"{total_score:.1f}/5.0",
            "热度评级": f"{rating} {heat}",
            "投资价值": "高" if total_score >= 4 else "中" if total_score >= 3 else "低"
        }

    def _generate_suggestion(self, evaluation: Dict) -> str:
        """生成投资建议"""
        score = float(evaluation.get("综合评分", "3.0").split("/")[0])

        if score >= 4.5:
            return "✅ 强烈推荐 | 重点配置，关注龙头股和ETF"
        elif score >= 4:
            return "✅ 推荐 | 适度配置，优选龙头股"
        elif score >= 3:
            return "⚠️ 中性 | 观望为主，等待催化事件"
        else:
            return "❌ 不推荐 | 暂时回避，缺乏催化剂"

    def print_report(self, result: Dict):
        """打印分析报告"""
        print(f"\n{'='*60}")
        print(f"📊 {result['板块名称']} 板块分析报告")
        print(f"{'='*60}\n")

        # 检查是否为通用板块
        is_generic = self.sector_data.get("is_generic", False)

        if is_generic:
            print("⚠️  这是一个自定义板块，以下是分析建议：\n")

        # 基本信息
        print("📋 基本信息:")
        for k, v in result["基本信息"].items():
            print(f"  {k}: {v}")

        # 龙头股
        print(f"\n🏆 龙头股:")
        if is_generic:
            print("  💡 如何查找板块龙头股：")
            print("  1. 访问东方财富板块行情：https://quote.eastmoney.com/center/")
            print("  2. 搜索板块名称，查看板块涨幅榜")
            print("  3. 选择涨幅前3-5只股票作为龙头")
            print("  4. 关注市值大、成交活跃的股票")
            print()
            print("  📊 龙头股特征：")
            print("  - 市值较大（通常板块内前3）")
            print("  - 成交量活跃")
            print("  - 题材纯正，主营业务契合")
            print("  - 技术走势强于板块")
        else:
            for stock in result["龙头股分析"]:
                print(f"  {stock['股票']} ({stock['代码']}) - {stock['说明']} {stock['重要性']}")

        # 板块趋势
        print(f"\n📈 板块趋势:")
        trend = result["板块趋势"]
        print(f"  {trend['趋势判断']}")
        print(f"  建议: {trend['建议']}")

        # 新闻驱动
        print(f"\n📰 新闻驱动:")
        for driver in result["新闻驱动"]:
            print(f"  [{driver['类型']}] {driver['说明']}")

        if is_generic:
            print()
            print("  💡 分析建议：")
            print("  1. 搜索板块相关新闻（财联社、同花顺）")
            print("  2. 查看板块指数走势（东方财富）")
            print("  3. 关注政策文件和行业规划")
            print("  4. 研究龙头企业财报和业务布局")

        # 综合评估
        print(f"\n📊 综合评估:")
        eval_data = result["综合评估"]
        print(f"  政策支持: {eval_data['政策支持评分']}")
        print(f"  市场空间: {eval_data['市场空间评分']}")
        print(f"  综合评分: {eval_data['综合评分']}")
        print(f"  热度评级: {eval_data['热度评级']}")
        print(f"  投资价值: {eval_data['投资价值']}")

        if is_generic:
            print()
            print("  💡 评估建议：")
            print("  - 政策支持：查询是否有国家级/省级政策支持")
            print("  - 市场空间：参考行业研究报告")
            print("  - 热度评级：观察板块成交量和涨幅")

        # 投资建议
        print(f"\n💡 投资建议:")
        print(f"  {result['投资建议']}")

        # 操作策略
        print(f"\n📋 操作策略:")
        if is_generic:
            print("  1. 先确认板块龙头股（建议3-5只）")
            print("  2. 分析龙头股的技术走势和基本面")
            print("  3. 查找板块ETF（如果有）")
            print("  4. 关注板块催化剂（政策、事件、业绩）")
            print("  5. 设置止损，控制风险（建议-10%）")
        else:
            etf_code = result["基本信息"].get("ETF代码", "无")
            print(f"  1. 优选板块ETF（如 {etf_code}）")
            print(f"  2. 关注龙头股表现，龙头强则板块强")
            print(f"  3. 注意催化事件（政策、业绩、行业大会）")
            print(f"  4. 设置止损，控制风险")

        # 风险提示
        print(f"\n⚠️  风险提示:")
        print(f"  板块轮动快，追高需谨慎")
        print(f"  政策变化可能影响板块表现")
        print(f"  建议分散投资，不要单一板块过度集中")

        if is_generic:
            print()
            print("📝 自定义板块分析清单：")
            print("  □ 确认板块定义和范围")
            print("  □ 找到板块龙头股（3-5只）")
            print("  □ 查看板块指数走势")
            print("  □ 分析政策支持和市场空间")
            print("  □ 研究新闻催化剂")
            print("  □ 制定投资策略和止损计划")

        print(f"\n{'='*60}\n")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 analyze_sector.py <板块名称>")
        print("\n预设板块（有完整数据）：")
        print("  AI/人工智能")
        print("  半导体")
        print("  新能源汽车")
        print("  消费电子/苹果链")
        print("  通信/5G")
        print("  石油/能源")
        print("  军工")
        print("  稀土")
        print("  低空经济/飞行汽车")
        print("  一体化压铸")
        print("\n✨ 支持任意板块分析！")
        print("  示例: python3 analyze_sector.py \"光伏\"")
        print("       python3 analyze_sector.py \"医美\"")
        print("       python3 analyze_sector.py \"元宇宙\"")
        print("\n提示：自定义板块会提供分析框架和查找建议")
        sys.exit(1)

    sector_name = sys.argv[1]

    # 创建分析器
    analyzer = SectorAnalyzer(sector_name)

    # 执行分析
    result = analyzer.analyze()

    # 打印报告
    analyzer.print_report(result)

    # 保存为JSON
    output_file = f"/tmp/{sector_name}_sector_analysis.json"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"📁 分析结果已保存: {output_file}")
    except:
        pass

if __name__ == "__main__":
    main()
