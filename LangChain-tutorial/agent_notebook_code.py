# ============================================
# 6、使用 Agent（Gemini 版本）
# ============================================

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

# 步骤1: 定义工具
@tool
def multiply(a: float, b: float) -> float:
    """将两个数字相乘"""
    return a * b

@tool
def add(a: float, b: float) -> float:
    """将两个数字相加"""
    return a + b

@tool
def get_word_length(word: str) -> int:
    """返回单词的长度"""
    return len(word)

# 步骤2: 创建工具列表
tools = [multiply, add, get_word_length]

# 步骤3: 创建 Agent 提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有用的助手，可以使用工具来帮助用户解决问题。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),  # Agent 的思考过程
])

# 步骤4: 创建 Agent（使用已有的 llm）
agent = create_tool_calling_agent(llm, tools, prompt)

# 步骤5: 创建 Agent Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # 显示执行过程
    handle_parsing_errors=True
)

# 步骤6: 测试 Agent
response = agent_executor.invoke({
    "input": "计算 25 乘以 4，然后加上 10。另外，告诉我 'LangChain' 这个单词有多少个字母？"
})

print("\n最终答案:")
print(response['output'])
