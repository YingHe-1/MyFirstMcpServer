# MyFirstMcpServer
[![smithery badge](https://smithery.ai/badge/@YingHe-1/yhfirstmcpserver)](https://smithery.ai/server/@YingHe-1/yhfirstmcpserver)

基于MCP框架的桌面TXT文件管理工具，提供以下功能：

1. 统计桌面上的TXT文件数量
2. 列出桌面上的所有TXT文件
3. 在桌面创建新的TXT文件（带用户交互确认）

## 安装

### Installing via Smithery

To install MyFirstMcpServer for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@YingHe-1/yhfirstmcpserver):

```bash
npx -y @smithery/cli install @YingHe-1/yhfirstmcpserver --client claude
```

### Manual Installation
```bash
# 克隆仓库
git clone https://github.com/YingHe-1/MyFirstMcpServer.git
cd MyFirstMcpServer

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

```bash
python add_num.py
```

## 工具函数

- `count_desktop_txt_files()`: 统计桌面TXT文件数量
- `list_desktop_txt_files()`: 列出桌面TXT文件
- `create_desktop_txt_file(filename, content)`: 创建桌面TXT文件

## 技术栈

- Python 3
- MCP (Model-Context-Protocol) 框架
