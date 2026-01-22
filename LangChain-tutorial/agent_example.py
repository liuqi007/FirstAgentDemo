"""
LangChain Agent 示例 - 使用 Gemini 大模型
这个示例展示如何使用 Gemini 创建一个具有工具调用能力的 Agent
"""

import os
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.tools.retriever import create_retriever_tool

# 加载环境变量
dotenv.load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv("GEMINI_API_KEY")

# ============================================
# 1. 初始化 Gemini 大模型
# ============================================
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # 或使用 gemini-3-flash-preview
    temperature=0.7,
    verbose=True
)

# ============================================
# 2. 定义自定义工具
# ============================================

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

# ============================================
# 3. 创建向量检索工具（可选）
# ============================================
def create_vector_retriever_tool():
    """创建基于 FAISS 的检索工具"""
    # 初始化嵌入模型
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        task_type="retrieval_document"
    )
    
    # 示例文档（实际使用时替换为你的文档）
    from langchain_core.documents import Document
    documents = [
        Document(page_content="LangChain 是一个用于开发由语言模型驱动的应用程序的框架。"),
        Document(page_content="Gemini 是 Google 开发的多模态大语言模型。"),
        Document(page_content="FAISS 是 Facebook 开发的高效相似性搜索库。"),
        Document(page_content="Agent 可以使用工具来完成复杂任务。"),
    ]
    
    # 创建向量存储
    vector_store = FAISS.from_documents(documents, embeddings)
    
    # 创建检索器
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    
    # 创建检索工具
    retriever_tool = create_retriever_tool(
        retriever,
        name="knowledge_base_search",
        description="搜索关于 LangChain、Gemini 和 AI 工具的知识库。当需要回答关于这些主题的问题时使用此工具。"
    )
    
    return retriever_tool

# ============================================
# 4. 创建网络搜索工具（可选）
# ============================================
try:
    search_tool = DuckDuckGoSearchRun(
        name="web_search",
        description="在互联网上搜索最新信息。当需要实时信息或最新新闻时使用。"
    )
    has_search = True
except Exception as e:
    print(f"网络搜索工具不可用: {e}")
    has_search = False

# ============================================
# 5. 组装所有工具
# ============================================
tools = [multiply, add, get_word_length]

# 添加检索工具
try:
    retriever_tool = create_vector_retriever_tool()
    tools.append(retriever_tool)
    print("✓ 向量检索工具已添加")
except Exception as e:
    print(f"向量检索工具创建失败: {e}")

# 添加网络搜索工具
if has_search:
    tools.append(search_tool)
    print("✓ 网络搜索工具已添加")

# ============================================
# 6. 创建 Agent Prompt
# ============================================
prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个有用的 AI 助手，可以使用多种工具来帮助用户。

你有以下能力：
- 执行数学计算（加法、乘法）
- 计算文本长度
- 搜索知识库
- 在互联网上搜索信息（如果可用）

请根据用户的问题选择合适的工具，并提供准确的答案。
如果不确定，可以使用多个工具来验证答案。"""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),  # Agent 的思考过程
])

# ============================================
# 7. 创建 Agent
# ============================================
agent = create_tool_calling_agent(llm, tools, prompt)

# ============================================
# 8. 创建 Agent Executor
# ============================================
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # 显示详细的执行过程
    handle_parsing_errors=True,  # 处理解析错误
    max_iterations=5,  # 最大迭代次数
)

# ============================================
# 9. 测试 Agent
# ============================================
def test_agent():
    """测试 Agent 的各种能力"""
    
    test_cases = [
        # 测试数学计算
        "计算 25 乘以 4，然后加上 10",
        
        # 测试文本处理
        "单词 'LangChain' 有多少个字母？",
        
        # 测试知识库检索
        "什么是 Gemini？",
        
        # 测试复杂推理
        "如果我有 3 个苹果，每个苹果重 0.5 公斤，总共多重？然后告诉我 'apple' 这个单词有几个字母。",
    ]
    
    print("\n" + "="*60)
    print("开始测试 Agent")
    print("="*60 + "\n")
    
    for i, question in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"测试 {i}: {question}")
        print(f"{'='*60}\n")
        
        try:
            response = agent_executor.invoke({"input": question})
            print(f"\n✓ 回答: {response['output']}\n")
        except Exception as e:
            print(f"\n✗ 错误: {e}\n")

# ============================================
# 10. 交互式对话模式
# ============================================
def interactive_mode():
    """启动交互式对话"""
    print("\n" + "="*60)
    print("Gemini Agent 交互模式")
    print("输入 'quit' 或 'exit' 退出")
    print("="*60 + "\n")
    
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("\n再见！👋")
                break
            
            if not user_input:
                continue
            
            response = agent_executor.invoke({"input": user_input})
            print(f"\nAgent: {response['output']}")
            
        except KeyboardInterrupt:
            print("\n\n再见！👋")
            break
        except Exception as e:
            print(f"\n错误: {e}")

# ============================================
# 主程序
# ============================================
if __name__ == "__main__":
    # 运行测试
    test_agent()
    
    # 启动交互模式（可选）
    # interactive_mode()
