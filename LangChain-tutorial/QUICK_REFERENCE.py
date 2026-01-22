"""
快速参考：LangChain 1.2.6 Agent 代码
直接复制到你的 Jupyter Notebook Cell 中
"""

# ============================================================
# 方案：使用 langchain_classic（推荐）
# ============================================================

from langchain.tools.retriever import create_retriever_tool
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

# 1. 创建检索器工具
retriever_tool = create_retriever_tool(
    retriever,
    "CivilCodeRetriever",
    "搜索有关中华人民共和国商事调解条例的信息。关于中华人民共和国商事调解条例的任何问题,您必须使用此工具!"
)

tools = [retriever_tool]

# 2. 定义 ReAct 提示词模板
react_prompt_template = """回答以下问题，尽你所能。你可以使用以下工具:

{tools}

使用以下格式:

Question: 你需要回答的输入问题
Thought: 你应该总是思考该做什么
Action: 要采取的行动，应该是 [{tool_names}] 中的一个
Action Input: 行动的输入
Observation: 行动的结果
... (这个 Thought/Action/Action Input/Observation 可以重复 N 次)
Thought: 我现在知道最终答案了
Final Answer: 对原始输入问题的最终答案

开始!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(react_prompt_template)

# 3. 创建 Agent
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

# 4. 创建 Agent Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)

# 5. 运行代理
result = agent_executor.invoke({"input": "设立商事调解组织的条件是什么"})
print(result['output'])
