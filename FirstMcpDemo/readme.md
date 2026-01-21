## 通过装饰器模式添加工具，和add_tool方法效果相同
# @mcp.tool()
# def foo():
#     return ""

def main():
    ## 启动MCP服务，stdio模式和sse模式区别是：stdio是标准输入输出模式，sse是服务器发送事件模式（基于HTTP协议，可以部署到任何支持HTTP的服务器上）
    mcp.run("stdio") # sse

claude desktop\cline


测试过程：
1. 启动MCP服务
2. 打开Claude Desktop：左上角菜单->setting->developer->edit config

测试的时候注意，如果在claude desktop中找不到hostInfoMcp，需要重启claude desktop（彻底退出，托盘也要退出）