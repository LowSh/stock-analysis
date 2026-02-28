#!/usr/bin/env python3
"""
股票技术分析脚本
获取股票实时数据并生成买入卖出建议
"""

import akshare as ak
import sys
from datetime import datetime

def analyze_stock(code, name=None):
    """分析单只股票"""
    try:
        # 获取历史数据
        df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")
        
        if df.empty:
            return None
        
        # 最新数据
        latest = df.iloc[-1]
        
        # 计算均线
        df['MA5'] = df['收盘'].rolling(5).mean()
        df['MA10'] = df['收盘'].rolling(10).mean()
        df['MA20'] = df['收盘'].rolling(20).mean()
        
        ma5 = df['MA5'].iloc[-1]
        ma10 = df['MA10'].iloc[-1]
        ma20 = df['MA20'].iloc[-1]
        
        close = latest['收盘']
        high = latest['最高']
        low = latest['最低']
        
        # 计算支撑位和阻力位
        recent_20 = df.tail(20)
        support = recent_20['最低'].min()
        resistance = recent_20['最高'].max()
        
        # 计算止损价（近期最低点下方3%）
        stop_loss = round(low * 0.97, 2)
        
        # 计算目标价（阻力位或+10%）
        target = round(max(resistance, close * 1.10), 2)
        
        # 买入区间（MA5-MA20之间）
        buy_low = round(min(ma5, ma20), 2)
        buy_high = round(max(ma5, ma20), 2)
        
        # 生成建议
        if close > ma5 > ma10 > ma20:
            trend = "多头排列"
            action = "持有/回调加仓"
            strength = "强"
        elif close > ma5 and close > ma20:
            trend = "偏多"
            action = "轻仓试探"
            strength = "中"
        elif close < ma5 < ma10 < ma20:
            trend = "空头排列"
            action = "观望/减仓"
            strength = "弱"
        elif close < ma5 and close < ma20:
            trend = "偏空"
            action = "观望"
            strength = "弱"
        else:
            trend = "震荡"
            action = "观望"
            strength = "中"
        
        return {
            'code': code,
            'name': name or latest.get('名称', code),
            'close': round(close, 2),
            'change': round(latest['涨跌幅'], 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'ma5': round(ma5, 2),
            'ma10': round(ma10, 2),
            'ma20': round(ma20, 2),
            'support': round(support, 2),
            'resistance': round(resistance, 2),
            'buy_range': f"{buy_low}-{buy_high}",
            'stop_loss': stop_loss,
            'target': target,
            'trend': trend,
            'action': action,
            'strength': strength
        }
        
    except Exception as e:
        print(f"Error analyzing {code}: {e}", file=sys.stderr)
        return None

def analyze_stocks(stock_list):
    """分析多只股票"""
    results = []
    for code, name in stock_list:
        result = analyze_stock(code, name)
        if result:
            results.append(result)
    return results

def print_markdown_table(results):
    """打印 Markdown 格式的表格"""
    print("\n## 💰 买入卖出建议\n")
    print("| 股票 | 代码 | 现价 | 涨跌% | 买入区间 | 止损价 | 目标价 | 趋势 | 建议 |")
    print("|------|------|------|-------|---------|--------|--------|------|------|")
    
    for r in results:
        change_str = f"+{r['change']}" if r['change'] > 0 else str(r['change'])
        print(f"| {r['name']} | {r['code']} | {r['close']} | {change_str}% | {r['buy_range']} | {r['stop_loss']} | {r['target']} | {r['trend']} | {r['action']} |")

def main():
    # 推荐股票列表 (代码, 名称)
    stocks = [
        # 用户持仓
        ('002738', '中矿资源'),
        ('600410', '华胜天成'),
        ('002156', '通富微电'),
        # AI/算力
        ('688256', '寒武纪'),
        ('601138', '工业富联'),
        ('603019', '中科曙光'),
        # 半导体
        ('605111', '新洁能'),
        ('600460', '士兰微'),
        ('300373', '扬杰科技'),
        # 通信
        ('000063', '中兴通讯'),
        ('600498', '烽火通信'),
        ('000988', '华工科技'),
        # 消费电子
        ('002475', '立讯精密'),
        ('002241', '歌尔股份'),
        ('300433', '蓝思科技'),
        # 政策
        ('601766', '中国中车'),
        ('601669', '中国电建'),
        ('600737', '中粮糖业'),
        # 资源
        ('600111', '北方稀土'),
        ('002460', '赣锋锂业'),
        ('600362', '江西铜业'),
        ('601857', '中国石油'),
        ('002267', '陕天然气'),
    ]
    
    print("正在分析股票...")
    results = analyze_stocks(stocks)
    print_markdown_table(results)
    
    # 技术分析说明
    print("\n### 📊 技术分析说明")
    print("\n**趋势判断：**")
    print("- 多头排列：MA5 > MA10 > MA20，股价在均线上方")
    print("- 空头排列：MA5 < MA10 < MA20，股价在均线下方")
    print("- 震荡：均线交织，方向不明")
    print("\n**操作建议：**")
    print("- 买入区间：MA5-MA20之间的价格区间")
    print("- 止损价：近期低点下方3%")
    print("- 目标价：近期阻力位或+10%")

if __name__ == "__main__":
    main()
