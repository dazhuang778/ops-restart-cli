## Why

运维人员需要手动 SSH 登录服务器并依次执行多条命令来重启 Normandy 和 Nova-OMP-Sentinel 两个服务，步骤繁琐且容易出错。需要一个简单的 CLI 工具来自动化这个流程。

## What Changes

- 新增 `restart-platform` Python CLI 工具
- 工具启动后交互式提示输入服务器地址、账号、密码（密码不回显）
- 通过 SSH 密码认证连接服务器
- 步骤一：执行 normandy 重启脚本，流式输出日志
- 用户确认后执行步骤二：在 sentinel 目录执行 docker-compose down && docker-compose up -d
- 配置文件（`~/.restart_platform/config.yaml`）存储固定路径信息，密码不落盘

## Capabilities

### New Capabilities

- `ssh-connection`: 基于 paramiko 的 SSH 密码认证连接，支持流式命令输出
- `restart-steps`: 两个重启步骤的封装（normandy 脚本、sentinel docker-compose）
- `cli-entrypoint`: 交互式 CLI 入口，包含服务器信息提示和步骤间确认

### Modified Capabilities

## Impact

- 新增依赖：`paramiko`、`questionary`、`pyyaml`
- 新增配置文件路径：`~/.restart_platform/config.yaml`
- 不影响任何现有代码
