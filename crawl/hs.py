import requests
import json
import time
from datetime import datetime

def get_hs300_v1():
    """方法1：使用新浪财经接口（新版本）"""
    try:
        url = "https://hq.sinajs.cn/rn=xxx42&list=s_sh000300"
        headers = {
            'Referer': 'https://finance.sina.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        response.encoding = 'gbk'
        
        if response.status_code == 200:
            data_str = response.text.split('="')[1].strip('";\n')
            data = data_str.split(',')
            return {
                'name': '沪深300',
                'price': float(data[1]),
                'change': float(data[2]),
                'percent': f"{float(data[3])}%",
                'time': f"{data[0]} {data[4]}"
            }
        return None
    except Exception as e:
        print(f"[新浪接口] 错误：{str(e)}")
        return None

def get_hs300_v2():
    """方法2：使用腾讯财经接口"""
    try:
        url = "https://qt.gtimg.cn/q=s_sh000300"
        response = requests.get(url, timeout=5)
        response.encoding = 'gbk'
        
        if response.status_code == 200:
            data = response.text.split('~')
            return {
                'name': data[1],
                'price': float(data[3]),
                'change': float(data[4]),
                'percent': data[5],
                'volume': f"{round(float(data[6])/10000, 2)}万手",
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        return None
    except Exception as e:
        print(f"[腾讯接口] 错误：{str(e)}")
        return None

def get_hs300_v3():
    """方法3：使用东方财富网接口"""
    try:
        url = "https://push2.eastmoney.com/api/qt/stock/get"
        params = {
            'secid': '1.000300',
            'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
            'fields': 'f43,f44,f45,f46,f60,f84,f169,f170',
            'invt': 2
        }
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()['data']
            return {
                'name': '沪深300',
                'price': data['f43']/100,
                'change': data['f170']/100,
                'percent': f"{data['f44']/100}%",
                'volume': f"{data['f84']/10000:.2f}万手",
                'time': datetime.fromtimestamp(data['f60']).strftime("%Y-%m-%d %H:%M:%S")
            }
        return None
    except Exception as e:
        print(f"[东财接口] 错误：{str(e)}")
        return None

def get_hs300():
    """自动尝试多个数据源"""
    for func in [get_hs300_v2]:
        data = func()
        if data:
            return data
    return None

def print_data(data):
    """格式化打印数据"""
    if not data:
        print("所有数据源获取失败，请检查网络或稍后重试")
        return
    
    print("\n=== 沪深300实时行情 ===")
    print(f"指数名称: {data['name']}")
    print(f"当前点数: {data['price']:.2f}")
    print(f"涨跌金额: {data['change']:.2f}")
    print(f"涨跌幅度: {data['percent']}")
    if 'volume' in data:
        print(f"成交量: {data['volume']}")
    print(f"更新时间: {data['time']}")

if __name__ == "__main__":
    while True:
        try:
            data = get_hs300()
            print_data(data)
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n程序已终止")
            break
        except Exception as e:
            print(f"发生未知错误: {str(e)}")
            time.sleep(10)
