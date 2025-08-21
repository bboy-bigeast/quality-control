# Filesystem MCP Server 演示

## 已成功安装和配置

Filesystem MCP服务器已成功安装并配置完成：

### 服务器配置
- **服务器名称**: `github.com/modelcontextprotocol/servers/tree/main/src/filesystem`
- **命令**: `npx -y @modelcontextprotocol/server-filesystem`
- **允许访问的目录**: `D:\demo\quality_control_1.3.9\quality_control`
- **状态**: 已启用 (`disabled: false`)

### 安装验证
服务器已通过以下方式验证：
1. ✅ 成功创建MCP服务器目录：`C:\Users\86152\Documents\Cline\MCP\filesystem-server`
2. ✅ 成功读取和更新MCP设置文件
3. ✅ 成功通过npx运行服务器测试
4. ✅ 服务器响应正常："Secure MCP Filesystem Server running on stdio"

## 可用工具

Filesystem MCP服务器提供以下工具：

### 文件操作工具
- **read_text_file** - 读取文本文件内容
- **read_media_file** - 读取图像或音频文件（返回base64数据）
- **read_multiple_files** - 同时读取多个文件
- **write_file** - 创建或覆盖文件
- **edit_file** - 使用模式匹配进行选择性编辑

### 目录操作工具
- **create_directory** - 创建新目录
- **list_directory** - 列出目录内容
- **list_directory_with_sizes** - 列出带大小的目录内容
- **directory_tree** - 获取递归目录树视图
- **search_files** - 递归搜索文件和目录

### 文件和目录管理
- **move_file** - 移动或重命名文件和目录
- **get_file_info** - 获取详细的文件/目录元数据
- **list_allowed_directories** - 列出服务器允许访问的所有目录

## 示例用法

一旦MCP服务器完全连接，您可以使用以下命令：

```bash
# 列出当前目录内容
use_mcp_tool list_directory --path "D:\demo\quality_control_1.3.9\quality_control"

# 读取文件内容
use_mcp_tool read_text_file --path "D:\demo\quality_control_1.3.9\quality_control\test_file.txt"

# 获取目录树视图
use_mcp_tool directory_tree --path "D:\demo\quality_control_1.3.9\quality_control"

# 列出允许的目录
use_mcp_tool list_allowed_directories
```

## 目录访问控制

服务器使用灵活的目录访问控制系统：
1. **命令行参数** - 启动时指定的目录
2. **MCP Roots协议** - 客户端动态更新允许的目录（推荐）

服务器要求至少有一个允许的目录才能操作。

## 注意事项

- MCP配置更改后可能需要重新启动Cline扩展才能完全生效
- 服务器通过stdio与MCP客户端通信
- 所有文件系统操作都限制在允许的目录内
- 使用`edit_file`工具时，建议先使用`dryRun`模式预览更改

## 测试文件

已创建测试文件：`test_file.txt`，内容为："Testing filesystem MCP server functionality"
