import requests
from datetime import datetime, timedelta
import json
import pandas as pd
import time
from alertHS import send_email

def get_kline_data():
    # 生成动态日期参数
    today = datetime.now().strftime("%Y%m%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")

    # 构造请求参数
    params = {
        "cb": "jQuery35107831533019888618_1748249797069",
        #"secid": "2.931637",  # 港股通互联网指数
        "secid": "1.159568",  # 港股通互联网指数
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": "101",  # 日线
        "fqt": "1",    # 前复权
        "beg": today,
        "end": tomorrow,
        "smplmt": "460",
        "lmt": "1000000",
        "_": str(int(datetime.now().timestamp() * 1000))
    }

    # 发送请求
    url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # 提取JSON数据
        json_str = response.text.split("(", 1)[1].rstrip(");")
        data = json.loads(json_str)
        
        if data["rc"] != 0:
            print("接口返回错误:", data)
            return None
            
        return data["data"]
    except Exception as e:
        print("请求失败:", str(e))
        return None

def analyze_kline(data):
    if not data or "klines" not in data or len(data["klines"]) == 0:
        print("当日无交易数据")
        return

    # 定义字段映射（保持原样）
    columns = [
        "日期", "开盘", "收盘", "最高", "最低",
        "成交量", "成交额", "振幅", "涨跌幅", 
        "涨跌额", "换手率"
    ]
    
    # 解析K线数据
    kline_str = data["klines"][0]
    kline_data = kline_str.split(",")
    df = pd.DataFrame([kline_data], columns=columns)
    
    # 类型转换（修复部分：添加成交量、成交额到转换列表）
    numeric_cols = ["开盘", "收盘", "最高", "最低", 
                   "成交量", "成交额",  # 新增这两个字段
                   "振幅", "涨跌幅", "涨跌额", "换手率"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    
    # 基础分析
    analysis = {
        "日期": df["日期"].values[0],
        "收盘价": df["收盘"].values[0],
        "涨跌幅 (%)": df["涨跌幅"].values[0],
        "日内波动": df["最高"].values[0] - df["最低"].values[0],
        "成交量 (万)": round(df["成交量"].values[0] / 10_000, 2),
        "成交额 (亿)": round(df["成交额"].values[0] / 100_000_000, 2),
        "相对前日": "上涨" if df["涨跌幅"].values[0] > 0 else "下跌",
        "开盘": df["开盘"].values[0],
    }
    
    return analysis
  
  
  
convert = 0.001154


if __name__ == "__main__":
  while True:
    kline_data = get_kline_data()
    if kline_data:
        print("="*40)
        print("原始K线数据：")
        print(kline_data["klines"])
        
        print("\n" + "="*40)
        print("当日行情分析：")
        analysis = analyze_kline(kline_data)
        up = analysis.get("涨跌幅 (%)",0)
        if up <= -1.5 or up >= 1:
          content = f"""港股通指数
          实时数据：
          - 相对前日:  {analysis['相对前日']}
          - 涨跌幅(%): {analysis['涨跌幅 (%)']}
          - 更新时间：  {analysis['日期']}
          - 当前价格:   {analysis['收盘价']}
          - 成本价/当前价: 1.1405/{analysis['收盘价'] * convert}
          请及时关注市场变化！"""
          send_email("港股通互联网指数",content)
        for k, v in analysis.items():
            print(f"{k:>12}: {v}")
    time.sleep(600)
