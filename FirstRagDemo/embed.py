import chunk
import chromadb
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

google_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
## 引入Google的embeding模型
EMBEDDING_MODEL = "gemini-embedding-001"
## 引入Google的LLM模型
LLM_MODEL = "gemini-3-flash-preview"

chroma_client = chromadb.PersistentClient(path="./chroma.db")
collection = chroma_client.get_or_create_collection(name="linghuchong")



def embed(text: str, store: bool) -> list[float]:
    result = google_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config={
            "task_type": "retrieval_document" if store else "retrieval_query"
        }
    )

    # assert result.embeddings
    # assert result.embeddings[0].values
    return result.embeddings[0].values

def create_db(chunks: list[str]):
    for idx, c in enumerate(chunks):
        print(f"embed chunk {c}")
        embedding: list[float] = embed(c, store=True)
        collection.upsert(
            ids = str(idx),
            documents=c,
            embeddings=embedding
        )

def query_db(question: str) -> list[str]:
    question_embedding = embed(question, store=False)
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=5
    )
    assert results["documents"]
    return results["documents"][0]

if __name__ == "__main__":
    # 测试1： 分块
    # chunks: list[str] = chunk.get_chunks()
    # print(embed(chunks[0], True))


    # 测试2： 保持到向量数据库
    #  create_db(chunk.get_chunks())

     # 测试3： 从向量数据库中查询
     question = "令狐冲有领悟了什么魔法？"
     chunks = query_db(question)
   
     # 测试4： 从向量数据库中查询结果并组装prompt
     prompt = f"please answer the question based on the context. \n question: {question}."
     prompt += f" context: \n"
     for c in chunks:
        prompt += f"{c} \n"
        prompt += "============================\n "

    #  print(prompt)

     # 测试5： 发送prompt到LLM模型
     resp = google_client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt
     )
     print(resp)


