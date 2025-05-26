# 学习记录
***
## 原理讲解
### MCP
1. 分为client/server两端，并且是1对1的
2. 客户端准备工具的名称、使用的方法(npx/uvx/pip)、远程地址或远程仓库名称
3. 客户端连接到服务端，传递上面的信息给服务端，然后本地安装执行服务
4. 这里面的实现很粗糙，强制在本地安装和运行所有工具

### Agent
1. 调用大模型，传入prompt、模型类型、tool列表 参数
2. 负责大模型与mcp之间的交互，根据大模型的输出调用mcp，获取结果再传给大模型
3. 这里面的实现也很粗糙，使用静态的工具列表

### RAG
1. Retrieve检索、Augmented增强、Generation生成
2. 将用户的prompt与外部知识库**检索**获取外部知识、**增强**输入给模型的prompt、获得更好的模型**生成**内容
3. 为了检索匹配，将外部知识库文本通过embedding模型转换成语义向量，并存入向量数据库
4. 对于用户的prompt，检索时同样通过embedding模型转成向量后，在数据库利用余弦相似度检索获取top-k文本片段，再拼接作为上下文放入prompt中

***
## 配置环境
- python3.12
- dotenv
- openai
- mcp
- rich

***
## 路线
1. 配置API KEY和BASE URL实现基本的调用chat功能
2. 新增console格式输出、实现异步chat
3. 配置justfile文件，需要安装just(命令行工具just由Rust编写，专门用于管理和运行项目脚本)，配置到系统环境中
4. 实现mcp功能，成功连接到mcp server并进行demo测试