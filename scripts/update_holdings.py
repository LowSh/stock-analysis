#!/usr/bin/env python3

"""
更新持仓股票实时数据
用法: python3 update_holdings.py
"""

import akshare as ak
import pandas as pd
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# 持仓股票列表
HOLDINGS = [
    {"code": "002738", "name": "中矿资源"},
    {"code": "600821", "name": "金开新能"},
    {"code": "601975", "name": "招商南油"},
]

def get_stock_data(code, name):
    """获取单只股票的最新数据"""
    import time
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 添加延迟避免请求过快
            if attempt > 0:
                time.sleep(2)
                print(f"  重试 {attempt}/{max_retries}...")
            
            # 获取历史数据（包含最新一天）
            df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")
            
            if len(df) == 0:
                return None
            
            # 获取最新数据
            latest = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else latest
            
            # 计算涨跌幅
            change_pct = ((latest['收盘'] - prev['收盘']) / prev['收盘'] * 100)
            
            # 计算均线
            df['MA5'] = df['收盘'].rolling(window=5).mean()
            df['MA10'] = df['收盘'].rolling(window=10).mean()
            df['MA20'] = df['收盘'].rolling(window=20).mean()
            
            ma5 = df['MA5'].iloc[-1]
            ma10 = df['MA10'].iloc[-1]
            ma20 = df['MA20'].iloc[-1]
            
            # 判断趋势
            if ma5 > ma10 > ma20:
                trend = "多头排列"
            elif ma5 < ma10 < ma20:
                trend = "空头排列"
            else:
                trend = "震荡"
            
            return {
                "code": code,
                "name": name,
                "date": latest['日期'],
                "close": round(latest['收盘'], 2),
                "change_pct": round(change_pct, 2),
                "volume": int(latest['成交量']),
                "ma5": round(ma5, 2),
                "ma10": round(ma10, 2),
                "ma20": round(ma20, 2),
                "trend": trend,
            }
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"❌ {name} ({code}) 获取失败: {e}")
                return None
            continue

def main():
    import time
    
    print(f"📊 更新持仓数据 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    print("=" * 80)
    
    results = []
    for i, stock in enumerate(HOLDINGS):
        # 添加延迟避免请求过快
        if i > 0:
            time.sleep(1)
        
        data = get_stock_data(stock['code'], stock['name'])
        if data:
            results.append(data)
            print(f"\n✅ {data['name']} ({data['code']})")
            print(f"  日期: {data['date']}")
            print(f"  收盘: {data['close']} ({data['change_pct']:+.2f}%)")
            print(f"  均线: MA5={data['ma5']} | MA10={data['ma10']} | MA20={data['ma20']}")
            print(f"  趋势: {data['trend']}")
    
    if results:
        # 保存到CSV
        df = pd.DataFrame(results)
        output_file = "/Users/zhenghao/Desktop/claw实验/持仓数据.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ 数据已保存到: {output_file}")
        
        # 返回JSON格式供其他脚本使用
        import json
        json_output = json.dumps(results, ensure_ascii=False, indent=2)
        print("\n📋 JSON格式:")
        print(json_output)
    else:
        print("\n❌ 没有成功获取任何数据")

if __name__ == "__main__":
    main()
