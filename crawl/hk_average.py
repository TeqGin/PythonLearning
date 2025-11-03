import requests
import json
import time
from datetime import datetime
import pandas as pd
import re

class HKInternetIndexTracker:
    def __init__(self):
        """
        港股通互联网指数追踪器
        主要追踪恒生科技指数(HSTECH)和相关互联网股票
        """
        # 恒生科技指数代码
        self.hstech_code = "931637"
        
        # 主要港股通互联网股票代码 (新浪财经格式)
        self.internet_stocks = {
            "腾讯控股": "hk00700",
            "阿里巴巴": "hk09988", 
            "美团": "hk03690",
            "京东集团": "hk09618",
            "小米集团": "hk01810",
            "快手": "hk01024",
            "哔哩哔哩": "hk09626",
            "网易": "hk09999",
            "百度": "hk09888",
            "携程": "hk09961"
        }
        
        # 请求头，模拟浏览器访问
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://finance.sina.com.cn/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache'
        }

    def get_sina_stock_data(self, sina_code):
        """
        通过新浪财经接口获取港股数据
        """
        try:
            url = f"https://hq.sinajs.cn/list={sina_code}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # 解析新浪财经返回的数据
                content = response.text
                if 'var hq_str_' in content:
                    data_str = content.split('="')[1].split('";')[0]
                    data_parts = data_str.split(',')
                    
                    if len(data_parts) >= 8:
                        try:
                            current_price = float(data_parts[6]) if data_parts[6] else 0
                            prev_close = float(data_parts[3]) if data_parts[3] else 0
                            change = current_price - prev_close
                            change_percent = (change / prev_close * 100) if prev_close > 0 else 0
                            
                            return {
                                'name': data_parts[0] if data_parts[0] else 'N/A',
                                'current_price': current_price,
                                'prev_close': prev_close,
                                'change': change,
                                'change_percent': change_percent,
                                'volume': int(data_parts[12]) if data_parts[12] and data_parts[12].isdigit() else 0,
                                'turnover': float(data_parts[13]) if data_parts[13] else 0,
                                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'currency': 'HKD'
                            }
                        except (ValueError, IndexError) as e:
                            print(f"解析 {sina_code} 数据失败: {e}")
                            return None
            
            return None
            
        except Exception as e:
            print(f"获取 {sina_code} 数据失败: {e}")
            return None

    def get_hstech_index(self):
        """
        获取恒生科技指数数据
        """
        try:
            # 恒生科技指数的新浪代码
            url = "https://hq.sinajs.cn/list=rt_931637"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                if '=' in content:
                    data_str = content.split('="')[1].split('";')[0]
                    data_parts = data_str.split(',')
                    
                    if len(data_parts) >= 9:
                        try:
                            return {
                                'name': '恒生科技指数',
                                'code': 'HSTECH',
                                'current': float(data_parts[6]) if data_parts[6] else 0,
                                'change': float(data_parts[7]) if data_parts[7] else 0,
                                'change_percent': float(data_parts[8]) if data_parts[8] else 0,
                                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                        except (ValueError, IndexError):
                            pass
            
            # 备选方案：通过东方财富获取
            return self.get_eastmoney_hstech()
            
        except Exception as e:
            print(f"获取恒生科技指数失败: {e}")
            return None

    def get_eastmoney_hstech(self):
        """
        通过东方财富获取恒生科技指数
        """
        try:
            # 恒生科技指数在东方财富的代码
            url = "https://push2.eastmoney.com/api/qt/stock/get"
            params = {
                'secid': '116.HSTECH',
                'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f57,f58'
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    info = data['data']
                    current = info.get('f43', 0) / 100  # 最新价
                    change = info.get('f44', 0) / 100   # 涨跌额
                    change_percent = info.get('f45', 0) / 100  # 涨跌幅
                    
                    return {
                        'name': '恒生科技指数',
                        'code': 'HSTECH',
                        'current': current,
                        'change': change,
                        'change_percent': change_percent,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
            
        except Exception as e:
            print(f"东方财富获取恒生科技指数失败: {e}")
        
        return None

    def get_eastmoney_stock_data(self, stock_code):
        """
        通过东方财富获取港股数据 (备选方案)
        """
        try:
            # 转换股票代码格式 (如 hk00700 -> 116.00700)
            code_num = stock_code.replace('hk', '').lstrip('0')
            if not code_num:
                code_num = '0'
            
            url = "https://push2.eastmoney.com/api/qt/stock/get"
            params = {
                'secid': f'116.{code_num.zfill(5)}',
                'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f57,f58'
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    info = data['data']
                    current_price = info.get('f43', 0) / 100
                    prev_close = info.get('f60', current_price)
                    change = info.get('f44', 0) / 100
                    change_percent = info.get('f45', 0) / 100
                    
                    return {
                        'current_price': current_price,
                        'prev_close': prev_close,
                        'change': change,
                        'change_percent': change_percent,
                        'volume': info.get('f47', 0),
                        'turnover': info.get('f48', 0),
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'currency': 'HKD'
                    }
            
        except Exception as e:
            print(f"东方财富获取 {stock_code} 数据失败: {e}")
        
        return None

    def calculate_custom_internet_index(self):
        """
        基于主要互联网股票计算自定义互联网指数
        """
        stock_data = []
        total_weight = 0
        weighted_change = 0
        
        print("正在获取主要港股通互联网股票数据...")
        
        for name, sina_code in self.internet_stocks.items():
            print(f"获取 {name} 数据...")
            
            # 首先尝试新浪财经
            data = self.get_sina_stock_data(sina_code)
            
            # 如果新浪失败，尝试东方财富
            if not data or data.get('current_price', 0) == 0:
                print(f"新浪接口失败，尝试东方财富接口...")
                data = self.get_eastmoney_stock_data(sina_code)
            
            if data and data.get('current_price', 0) > 0:
                stock_info = {
                    'name': name,
                    'code': sina_code,
                    'price': data['current_price'],
                    'change': data['change'],
                    'change_percent': data['change_percent'],
                    'volume': data.get('volume', 0),
                    'turnover': data.get('turnover', 0)
                }
                
                stock_data.append(stock_info)
                
                # 使用成交额作为权重进行加权计算
                weight = data.get('turnover', 1)
                if weight > 0:
                    total_weight += weight
                    weighted_change += data['change_percent'] * weight
                else:
                    # 如果没有成交额数据，使用等权重
                    total_weight += 1
                    weighted_change += data['change_percent']
                
                print(f"✓ {name}: {data['current_price']:.2f} ({data['change_percent']:+.2f}%)")
            else:
                print(f"✗ {name}: 获取数据失败")
            
            time.sleep(0.5)  # 避免请求过于频繁
        
        # 计算加权平均涨跌幅
        if total_weight > 0:
            avg_change_percent = weighted_change / total_weight
        else:
            avg_change_percent = 0
            
        return stock_data, avg_change_percent

    def display_results(self):
        """
        显示实时数据结果
        """
        print("\n" + "=" * 70)
        print("港股通互联网指数实时数据")
        print("=" * 70)
        print(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 获取恒生科技指数
        hstech_data = self.get_hstech_index()
        if hstech_data and hstech_data.get('current', 0) > 0:
            print("【恒生科技指数】")
            print(f"当前点位: {hstech_data['current']:.2f}")
            print(f"涨跌额: {hstech_data['change']:+.2f}")
            print(f"涨跌幅: {hstech_data['change_percent']:+.2f}%")
            print()
        else:
            print("【恒生科技指数】")
            print("暂时无法获取数据")
            print()
        
        # 获取个股数据
        stock_data, avg_change = self.calculate_custom_internet_index()
        
        if stock_data:
            print("【主要港股通互联网股票】")
            print(f"{'股票名称':<12} {'当前价格(HKD)':<15} {'涨跌额':<10} {'涨跌幅':<10} {'成交额(万)':<12}")
            print("-" * 70)
            
            for stock in stock_data:
                turnover_wan = stock['turnover'] / 10000 if stock['turnover'] > 0 else 0
                print(f"{stock['name']:<10} {stock['price']:>10.2f} "
                      f"{stock['change']:>+10.2f} {stock['change_percent']:>+8.2f}% "
                      f"{turnover_wan:>10.1f}")
            
            print("-" * 70)
            print(f"互联网板块平均涨跌幅: {avg_change:+.2f}%")
            print(f"成功获取数据的股票数量: {len(stock_data)}/{len(self.internet_stocks)}")
        else:
            print("【错误】无法获取任何股票数据，请检查网络连接")
        
        print()

    def save_to_csv(self, filename=None):
        """
        保存数据到CSV文件
        """
        if not filename:
            filename = f"hk_internet_index_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        stock_data, avg_change = self.calculate_custom_internet_index()
        
        if stock_data:
            df = pd.DataFrame(stock_data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"数据已保存到: {filename}")
        else:
            print("没有可保存的数据")

    def continuous_monitor(self, interval=60):
        """
        持续监控模式
        """
        print(f"开始持续监控，每{interval}秒更新一次，按Ctrl+C停止...")
        
        try:
            while True:
                self.display_results()
                print(f"下次更新将在{interval}秒后...")
                print("=" * 70 + "\n")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n监控已停止")

def main():
    """
    主函数
    """
    tracker = HKInternetIndexTracker()
    
    while True:
        print("\n港股通互联网指数追踪器")
        print("1. 获取一次实时数据")
        print("2. 持续监控模式")
        print("3. 保存数据到CSV")
        print("4. 退出")
        
        choice = input("\n请选择操作 (1-4): ").strip()
        
        if choice == '1':
            tracker.display_results()
            
        elif choice == '2':
            interval = input("请输入更新间隔(秒，默认60): ").strip()
            try:
                interval = int(interval) if interval else 60
                if interval < 10:
                    print("为避免请求过于频繁，最小间隔设为10秒")
                    interval = 10
                tracker.continuous_monitor(interval)
            except ValueError:
                print("无效的时间间隔，使用默认值60秒")
                tracker.continuous_monitor(60)
                
        elif choice == '3':
            filename = input("请输入文件名(默认自动生成): ").strip()
            tracker.save_to_csv(filename if filename else None)
            
        elif choice == '4':
            print("程序退出")
            break
            
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    # 需要安装的依赖包
    print("请确保已安装以下依赖包:")
    print("pip install requests pandas")
    print()
    
    main()