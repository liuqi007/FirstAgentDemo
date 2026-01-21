import os
from dotenv import load_dotenv
from pydantic_ai.models.google import GoogleModel
from pydantic_ai import Agent
from tools import read_file, list_files, rename_file

load_dotenv()

model = GoogleModel("gemini-3-flash-preview")

agent = Agent(model, system_prompt="You are an experienced software engineer.", tools=[read_file, list_files, rename_file])

def main():
    history = []
    while True:
        user_input = input("input: ")
        resp = agent.run_sync(user_input, message_history=history)
        history.append(resp)
        print(resp.output)

## 输入：list and read file. base on you knowledg tell me what language each file use.
if __name__ == "__main__":
    main()
