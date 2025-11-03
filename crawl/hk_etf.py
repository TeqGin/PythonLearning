import requests
import json
import time
from alertHS import send_email

def get_stock_quote(secid):
    """
    获取股票/基金实时行情数据
    :param secid: 证券代码（格式：市场.代码，例如深市基金'0.159568'）
    :return: 包含行情数据的字典
    """
    # 基础URL（已移除cb参数避免JSONP格式）
    base_url = "https://push2.eastmoney.com/api/qt/stock/get"
    
    # 构造请求参数
    params = {
        "invt": 2,
        "fltt": 1,
        "fields": "f58,f57,f43,f60,f169,f170,f44,f45,f47,f48",
        "secid": secid,
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "wbp2u": "|0|0|0|web",
        "dect": 1,
        "_": int(time.time() * 1000)  # 添加时间戳防止缓存
    }
    
    try:
        # 发送请求
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # 检查HTTP错误
        
        # 解析JSON数据
        data = json.loads(response.text)
        
        # 检查API返回状态
        if data.get("rc") != 0:
            return {"error": f"API returned error: {data.get('rt')}"}
        
        # 提取核心数据
        quote_data = data.get("data", {})
        if not quote_data:
            return {"error": "No market data found"}
        
        # 转换价格单位（原始数据为1000倍实际值）
        def convert_price(value):
            return round(value / 1000, 3) if value != 0 else 0.0
        
        # 组织返回数据
        return {
            "代码": quote_data.get("f57", "N/A"),
            "名称": quote_data.get("f58", "N/A"),
            "最新价": convert_price(quote_data.get("f43", 0)),
            "昨收价": convert_price(quote_data.get("f60", 0)),
            "涨跌额": convert_price(quote_data.get("f169", 0)),
            "涨跌幅": round(quote_data.get("f170", 0) / 10000, 4),  # 转换为百分比
            "最高价": convert_price(quote_data.get("f44", 0)),
            "最低价": convert_price(quote_data.get("f45", 0)),
            "成交量(手)": quote_data.get("f47", 0),
            "成交额(元)": quote_data.get("f48", 0)
        }
        
    except Exception as e:
        return {"error": str(e)}

# 使用示例
if __name__ == "__main__":
    # 输入证券代码（示例：港股互联网ETF）
		while True:
			secid = "0.159568"
			quote = get_stock_quote(secid)
			
			# 打印行情数据
			if "error" in quote:
					print(f"获取数据失败: {quote['error']}")
			else:
					print("=" * 40)
					print(f"{quote['名称']}({quote['代码']}) 实时行情")
					print("=" * 40)
					print(f"最新价: {quote['最新价']} 元")
					print(f"涨跌额: {'+' if quote['涨跌额'] > 0 else ''}{quote['涨跌额']} 元")
					print(f"涨跌幅: {'+' if quote['涨跌幅'] > 0 else ''}{quote['涨跌幅']:.2%}")
					print(f"昨收价: {quote['昨收价']} 元")
					print(f"今日波动: {quote['最低价']} ~ {quote['最高价']} 元")
					print(f"成交量: {quote['成交量(手)']} 手")
					print(f"成交额: {quote['成交额(元)']} 元")
			if quote['涨跌幅'] <= -1 or quote['涨跌幅'] >= 1:
					content = f"""港股通指数
					实时数据：
					- 涨跌幅(%): {(f"涨跌幅: {'+' if quote['涨跌幅'] > 0 else ''}{quote['涨跌幅']:.2%}")}
					- 当前价: {quote['最新价']}
					请及时关注市场变化！"""
					send_email("港股通互联网指数",content)
			time.sleep(600)
