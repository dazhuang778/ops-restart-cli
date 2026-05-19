# ops-restart-cli

> 通过 SSH 一键重启 Normandy 与 Nova-OMP-Sentinel 的运维 CLI 工具，支持服务器账号记忆与分步骤确认。

## 功能特性

- **交互式登录** — 启动后提示输入服务器地址、账号、密码（密码不回显）
- **服务器记忆** — 登录过的服务器自动保存，下次直接选择，密码存入系统密钥链（Windows Credential Manager）
- **分步骤执行** — 先重启 Normandy，确认后再重启 Nova-OMP-Sentinel，防止误操作
- **实时进度条** — 命令执行期间显示进度条与预计剩余时间，日志实时滚动输出
- **一键启动** — Windows 双击 `restart.bat` 即可运行，无需手动输入路径

## 目录结构

```
ops-restart-cli/
├── restart.bat                  # Windows 一键启动脚本
└── restart_platform/
    ├── main.py                  # CLI 入口
    ├── ssh_client.py            # SSH 连接与命令执行
    ├── steps.py                 # 重启步骤封装
    ├── server_history.py        # 服务器记忆与密码管理
    ├── requirements.txt         # Python 依赖
    └── config.example.yaml      # 配置文件模板
```

## 环境要求

- Python 3.10+
- Windows / macOS / Linux
- 目标服务器开启 SSH 密码认证

## 安装

```bash
# 1. 克隆仓库
git clone git@github.com:dazhuang778/ops-restart-cli.git
cd ops-restart-cli

# 2. 安装依赖
pip install -r restart_platform/requirements.txt
```

## 配置（可选）

不配置也能运行，每次启动时手动输入即可。如需预填默认值：

```bash
mkdir -p ~/.restart_platform
cp restart_platform/config.example.yaml ~/.restart_platform/config.yaml
```

编辑 `~/.restart_platform/config.yaml`：

```yaml
# 可选：预填默认值，节省每次输入
default_host: 10.0.1.5
default_user: ops

steps:
  normandy:
    script: /data/app/normandy-5101/bin/normandy_restart.sh
  sentinel:
    workdir: /data/workspace/nova-omp-sentinel
```

## 使用方式

### Windows（推荐）

双击根目录下的 `restart.bat`，或在终端运行：

```
restart.bat
```

### 命令行

```bash
cd restart_platform
python main.py
```

## 交互流程

**首次运行**

```
┌─────────────────────────────────────┐
│        运维平台重启工具              │
└─────────────────────────────────────┘

? 服务器地址: 10.0.1.5
? 登录账号: ops
? 登录密码: ********
? 保存此服务器？ (Y/n): y
  已保存 ops@10.0.1.5

✓ SSH 连接成功 (ops@10.0.1.5)

步骤 1：重启 Normandy
⠸ Normandy 重启中  ████████░░░░  0:01:02 / 预计 120s

✓ Normandy 重启完成

? 继续重启 Nova-OMP-Sentinel？ (Y/n): y

步骤 2：重启 Nova-OMP-Sentinel
⠸ Sentinel 重启中  ██████░░░░░░  0:00:45 / 预计 120s

✓ Sentinel 重启完成
✓ 全部完成
```

**再次运行（已有记录）**

```
? 选择服务器:
  > ops@10.0.1.5
    + 新服务器

  使用已保存的密码
✓ SSH 连接成功 (ops@10.0.1.5)
```

## 依赖说明

| 包 | 用途 |
|----|------|
| `paramiko` | SSH 连接与命令执行 |
| `questionary` | 交互式终端提示 |
| `PyYAML` | 配置文件解析 |
| `rich` | 进度条与终端美化 |
| `keyring` | 系统密钥链密码存储 |
