import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header
import requests
import time
from datetime import datetime

# 邮件配置（通过环境变量获取敏感信息）
SINA_EMAIL = os.getenv('SINA_EMAIL')  # 你的新浪邮箱地址
SINA_PASSWORD = os.getenv('SINA_PASSWORD')  # 邮箱密码/授权码
SMTP_SERVER = 'smtp.sina.com'
SMTP_PORT = 465
RECIPIENT = 'xudafengabc@gmail.com'  # 改为实际接收邮箱
ALERT_THRESHOLD = 3900
ALERT_THRESHOLD_MAX = 4000
last_alert_time = None  # 记录上次发送时间

def send_email(subject, content):
    """发送邮件通知"""
    global last_alert_time
    
    # 防止频繁发送（至少间隔1小时）
    if last_alert_time and (time.time() - last_alert_time) < 3600:
        print("警报发送间隔太短，已忽略")
        return
    
    try:
        # 创建邮件内容
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = Header(SINA_EMAIL)
        message['To'] = Header(RECIPIENT)
        message['Subject'] = Header(subject, 'utf-8')

        # 连接SMTP服务器
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SINA_EMAIL, SINA_PASSWORD)
            server.sendmail(SINA_EMAIL, [RECIPIENT], message.as_string())
        
        last_alert_time = time.time()
        print("警报邮件已发送")
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")

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

def check_and_alert():
    """检查指数并触发警报"""
    data = get_hs300_v2()
    if not data:
        return
    
    print(f"\n当前指数: {data['price']} ({data['time']})")
    
    if data['price'] < ALERT_THRESHOLD or data['price'] >= ALERT_THRESHOLD_MAX:
        subject = f"沪深300指数警报 - 当前值 {data['price']}"
        content = f"""沪深300指数已跌破警戒线！
        
实时数据：
- 指数名称：{data['name']}
- 当前点数：{data['price']}
- 更新时间：{data['time']}

请及时关注市场变化！"""
        send_email(subject, content)

if __name__ == "__main__":
    # 验证邮箱配置
    if not all([SINA_EMAIL, SINA_PASSWORD]):
        print("请设置环境变量：")
        print("export SINA_EMAIL='your_email@sina.com'")
        print("export SINA_PASSWORD='your_password'")
        exit(1)

    # 测试警报功能
    print("=== 沪深300监控系统（带邮件警报）===")
    while True:
        try:
            check_and_alert()
            time.sleep(30)  # 每5s检查一次
        except KeyboardInterrupt:
            print("\n监控已停止")
            break
        except Exception as e:
            print(f"监控异常: {str(e)}")
            time.sleep(30)
