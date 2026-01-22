"""
Modern LangChain 1.2.6 Agent using LangGraph
This is the new recommended approach for LangChain 1.x
"""

from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_agent
from langgraph.prebuilt import create_react_agent

# 检索器工具
retriever_tool = create_retriever_tool(
    retriever,
    "CivilCodeRetriever",
    "搜索有关中华人民共和国商事调解条例的信息。关于中华人民共和国商事调解条例的任何问题,您必须使用此工具!"
)

tools = [retriever_tool]

# 使用 LangGraph 的 create_react_agent (新方法)
# 这是 LangChain 1.x 推荐的方式
agent_executor = create_react_agent(
    model=llm,
    tools=tools,
    state_modifier="你是一个专业的法律问答助手。请使用提供的工具来回答用户的问题。"
)

# 运行代理
print("开始执行 Agent (使用 LangGraph)...")
print("="*60)

# LangGraph agents use a different invoke pattern
result = agent_executor.invoke(
    {"messages": [("user", "设立商事调解组织的条件是什么")]}
)

print("\n" + "="*60)
print("【最终答案】")
print("="*60)

# Extract the final answer from messages
final_message = result["messages"][-1]
print(final_message.content)
