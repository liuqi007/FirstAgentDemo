"""
Modern LangChain 1.2.6 Agent Example
Using the new create_react_agent approach
"""

from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

# 检索器工具
retriever_tool = create_retriever_tool(
    retriever,
    "CivilCodeRetriever",
    "搜索有关中华人民共和国商事调解条例的信息。关于中华人民共和国商事调解条例的任何问题,您必须使用此工具!"
)

tools = [retriever_tool]

# Define a ReAct-style prompt template
# ReAct = Reasoning + Acting pattern
template = """你是一个问答助手。你可以使用以下工具来回答问题:

{tools}

工具名称: {tool_names}

使用以下格式:

Question: 你需要回答的问题
Thought: 你应该思考要做什么
Action: 要采取的行动，应该是 [{tool_names}] 中的一个
Action Input: 行动的输入
Observation: 行动的结果
... (这个 Thought/Action/Action Input/Observation 可以重复N次)
Thought: 我现在知道最终答案了
Final Answer: 对原始输入问题的最终答案

开始!

Question: {input}
Thought: {agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template)

# Create the ReAct agent
agent = create_react_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    handle_parsing_errors=True,  # Handle parsing errors gracefully
    max_iterations=5  # Limit iterations to prevent infinite loops
)

# 运行代理
result = agent_executor.invoke({"input": "设立商事调解组织的条件是什么"})
print("\n" + "="*50)
print("最终答案:")
print("="*50)
print(result['output'])
