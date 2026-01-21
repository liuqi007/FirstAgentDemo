from mcp.server.fastmcp import FastMCP
import tools

mcp = FastMCP("host info mcp")
mcp.add_tool(tools.get_host_info)

## 通过装饰器模式添加工具，和add_tool方法效果相同
@mcp.tool()
def foo():
    return ""

def main():
    # print("host info mcp is running")
    # 不要使用 print！会干扰 stdio 通信
    ## 启动MCP服务，stdio模式和sse模式区别是：stdio是标准输入输出模式，sse是服务器发送事件模式（基于HTTP协议，可以部署到任何支持HTTP的服务器上）
    mcp.run("stdio") # sse


if __name__ == "__main__":
    main()