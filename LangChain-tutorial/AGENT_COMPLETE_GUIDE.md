# LangChain 1.2.6 Agent 完整解决方案

## 🎯 核心问题

LangChain 1.2.6 进行了重大重构：
- 旧的 agent 函数移到了 `langchain_classic` 包
- 新的推荐方式是使用 `langgraph` 包

## ✅ 解决方案 1：使用 langchain_classic（推荐，简单）

这是最简单的解决方案，使用传统的 ReAct Agent：

```python
from langchain.tools.retriever import create_retriever_tool
from langchain_classic.agents import create_react_agent, AgentExecutor  # 关键：从 langchain_classic 导入
from langchain_core.prompts import PromptTemplate

# 检索器工具
retriever_tool = create_retriever_tool(
    retriever,
    "CivilCodeRetriever",
    "搜索有关中华人民共和国商事调解条例的信息。关于中华人民共和国商事调解条例的任何问题,您必须使用此工具!"
)

tools = [retriever_tool]

# ReAct 提示词模板
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

# 创建 Agent
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)

# 运行
result = agent_executor.invoke({"input": "设立商事调解组织的条件是什么"})
print(result['output'])
```

## ✅ 解决方案 2：使用 LangGraph（现代化，推荐用于新项目）

这是 LangChain 1.x 的新推荐方式：

```python
from langchain.tools.retriever import create_retriever_tool
from langgraph.prebuilt import create_react_agent

# 检索器工具
retriever_tool = create_retriever_tool(
    retriever,
    "CivilCodeRetriever",
    "搜索有关中华人民共和国商事调解条例的信息。关于中华人民共和国商事调解条例的任何问题,您必须使用此工具!"
)

tools = [retriever_tool]

# 使用 LangGraph 创建 agent
agent_executor = create_react_agent(
    model=llm,
    tools=tools,
    state_modifier="你是一个专业的法律问答助手。请使用提供的工具来回答用户的问题。"
)

# 运行（注意：调用方式不同）
result = agent_executor.invoke(
    {"messages": [("user", "设立商事调解组织的条件是什么")]}
)

# 提取答案
final_message = result["messages"][-1]
print(final_message.content)
```

## 📊 两种方案对比

| 特性 | langchain_classic | LangGraph |
|------|-------------------|-----------|
| 难度 | ⭐ 简单 | ⭐⭐ 中等 |
| 兼容性 | ✅ 向后兼容 | ✅ 面向未来 |
| 功能 | 基础 Agent | 高级 Agent + 状态管理 |
| 推荐场景 | 快速原型、学习 | 生产环境、复杂应用 |
| 调用方式 | `invoke({"input": "..."})` | `invoke({"messages": [...]})` |

## 🔧 关键导入变化

### ❌ 错误的导入（会报错）

```python
from langchain.agents import create_react_agent, AgentExecutor  # ❌ 不存在
```

### ✅ 正确的导入

**方案 1 - Classic:**
```python
from langchain_classic.agents import create_react_agent, AgentExecutor  # ✅
```

**方案 2 - LangGraph:**
```python
from langgraph.prebuilt import create_react_agent  # ✅
```

## 📝 在 Jupyter Notebook 中使用

### 步骤 1: 重启 Kernel

在 Jupyter 中：`Kernel` → `Restart Kernel`

### 步骤 2: 选择一个方案

**推荐用方案 1（langchain_classic）**，因为：
- 更简单
- 与你的现有代码更接近
- 更容易理解和调试

### 步骤 3: 复制代码到 Notebook

将 `agent_working_solution.py` 的内容复制到你的 notebook cell 中。

## 🐛 故障排除

### 问题 1: 仍然报 ImportError

**解决方案：**
```bash
# 确认 langchain_classic 已安装
pip show langchain-classic

# 如果没有，重新安装
pip install --upgrade langchain langchain-classic
```

### 问题 2: Gemini 不理解 ReAct 格式

**解决方案：** 使用英文 prompt 模板

```python
react_prompt_template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""
```

### 问题 3: Agent 执行失败

**解决方案：**
1. 增加 `max_iterations=10`
2. 启用 `verbose=True` 查看详细日志
3. 使用 `handle_parsing_errors=True`

## 📚 参考文件

1. **`agent_working_solution.py`** ⭐ **强烈推荐** - 使用 langchain_classic
2. **`agent_langgraph_solution.py`** - 使用 LangGraph（高级）
3. **`agent_modern_code.py`** - 已过时，不要使用
4. **`agent_fixed_code.py`** - 已过时，不要使用

## 🎓 学习资源

- [LangChain Classic 文档](https://python.langchain.com/docs/langchain_classic/)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [Agent 迁移指南](https://python.langchain.com/docs/versions/migrating_agents/)

## 💡 最佳实践

1. **对于学习和原型开发**：使用 `langchain_classic`
2. **对于生产环境**：考虑迁移到 `langgraph`
3. **始终使用 `verbose=True`**：方便调试
4. **设置合理的 `max_iterations`**：防止无限循环
5. **启用 `handle_parsing_errors`**：提高鲁棒性
