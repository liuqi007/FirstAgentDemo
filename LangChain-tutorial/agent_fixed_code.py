from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain.agents import create_tool_calling_agent, AgentExecutor

# 检索器工具
retriever_tool = create_retriever_tool(
    retriever,
    "CivilCodeRetriever",
    "搜索有关中华人民共和国商事调解条例的信息。关于中华人民共和国商事调解条例的任何问题,您必须使用此工具!"
)

tools = [retriever_tool]

# Use a prompt compatible with tool-calling agents
# Alternative prompts you can try:
# - "hwchase17/structured-chat-agent"
# - "hwchase17/react-chat"
prompt = hub.pull("hwchase17/structured-chat-agent")

# Create the agent using create_tool_calling_agent (replaces create_openai_functions_agent)
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 运行代理
result = agent_executor.invoke({"input": "设立商事调解组织的条件是什么"})
print(result)
