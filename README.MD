# Systemd 服务创建工具

一个简单的 Python 脚本，用于快速创建和管理 Systemd 服务。

## 功能特点

- 交互式创建 Systemd 服务
- 支持自定义服务描述
- 可配置重启策略
- 支持设置工作目录
- 自动启用并启动服务

## 使用要求

- Python 3.6+
- Linux 系统
- Root 权限

## 安装

```bash
wget https://raw.githubusercontent.com/ours1505/systemdc/refs/heads/main/main.py -O /usr/bin/systemdc
chmod +x /usr/bin/systemdc
```

## 使用方法

1. 以 root 权限运行脚本：

```bash
systemdc
```

2. 按照提示输入以下信息：
   - 服务名称（支持字母、数字、连字符(-)、@符号和下划线(_)）
   - 服务描述（可选）
   - 执行命令（完整的命令行，如：`python3 /path/to/script.py`）
   - 工作目录（可选）
   - 重启策略（选择以下之一）：
     1. always（总是重启）
     2. on-failure（仅在失败时重启）
     3. no（不自动重启）

## 示例

创建一个 Python 脚本服务：
```bash
$ systemdc
欢迎使用 Systemd 服务创建工具
----------------------------------------
请输入服务名称: my-python-app
请输入服务描述 (可选): 我的 Python 应用
执行命令: python3 /root/apps/script.py
请输入工作目录 (可选): /root/apps
请选择重启策略:
1. always (总是重启)
2. on-failure (仅在失败时重启)
3. no (不自动重启)
请输入选项 (1-3) [默认: 1]: 1
```

## 服务管理

创建服务后，可以使用标准的 systemctl 命令管理服务：

```bash
# 查看服务状态
sudo systemctl status my-python-app

# 停止服务
sudo systemctl stop my-python-app

# 启动服务
sudo systemctl start my-python-app

# 禁用服务
sudo systemctl disable my-python-app

# 启用服务
sudo systemctl enable my-python-app
```

## 注意事项

- 脚本需要 root 权限才能运行
- 服务文件将被创建在 `/etc/systemd/system/` 目录下
- 确保执行命令中指定的程序路径正确且具有执行权限
- 建议在创建服务前测试执行命令是否可以正常运行
