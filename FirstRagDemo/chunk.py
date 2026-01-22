from ast import List
import os


def read_data() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "data.md")
    with open(data_path, "r", encoding="utf-8") as f:
        data = f.read()
    return data

def get_chunks() -> list[str]:
    data: str = read_data()
    chunks: list[str] = data.split("\n\n")

    result: List[Any] = []
    header: str = ""
    for chunk in chunks:
        if chunk.startswith("# "):
            header += f"{chunk}\n"
        else:
            result.append(f"{header}{chunk}")
            header = ""
    return result

if __name__ == "__main__":
    ## 将文件分块
    chunks: list[str] = get_chunks()
    for chunk in chunks:
        print(chunk)
        print("===========================================================================")