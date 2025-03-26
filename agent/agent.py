import os
import sys
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
import requests
from datetime import datetime

# 加载环境变量
load_dotenv()

# 1. 创建工具集
def create_tools():
    search = SerpAPIWrapper()  # 需要 SERPAPI_API_KEY

    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="用于搜索最新信息，比如当前事件、天气等"
        ),
        Tool(
            name="Calculator",
            func=lambda x: str(eval(x)),  # 简单计算器
            description="用于数学计算，输入数学表达式如 '3 * 5'"
        ),
        Tool(
            name="hs300",
            func=get_hs300_v2,
            description="获取实时沪深300指数"
        ),
        Tool(
            name="CurrentDate",
            func=get_current_date,
            description="获取当前的日期时间信息，包括具体日期、时间、星期几等"
        )
    ]
    return tools


def get_hs300_v2(x :str):
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

def get_current_date(x: str) -> str:
    """获取当前日期时间"""
    current_time = datetime.now()
    return {
        'date': current_time.strftime("%Y-%m-%d"),
        'time': current_time.strftime("%H:%M:%S"),
        'weekday': current_time.strftime("%A"),
        'full': current_time.strftime("%Y-%m-%d %H:%M:%S")
    }

# 2. 初始化 DeepSeek 模型
def create_llm():
    return ChatOpenAI(
        model_name="deepseek-reasoner",
        openai_api_base="https://api.deepseek.com/v1",
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0.8,
        max_tokens=4000
    )

# 3. 创建 ReAct Agent
def create_agent():
    # 从 LangChain Hub 获取预设提示模板
    prompt = hub.pull("hwchase17/react")
    
    return create_react_agent(
        llm=create_llm(),
        tools=create_tools(),
        prompt=prompt
    )

# 4. 运行 Agent
if __name__ == "__main__":
    agent = create_agent()
    agent_executor = AgentExecutor(
        agent=agent,
        tools=create_tools(),
        verbose=True,  # 显示详细执行过程
        max_iterations=10,  # 增加最大迭代次数
        max_execution_time=120,  # 设置最大执行时间（秒）
    )

    # 获取查询内容：优先使用命令行参数，如果没有则使用默认查询
    default_query = "请详细介绍大冰是谁，深入分析他的文学功底，并全面介绍他的主要作品。请尽可能详细。"
    query = sys.argv[1] if len(sys.argv) > 1 else default_query
    
    result = agent_executor.invoke({"input": query})
    print("\n最终答案:", result["output"])
