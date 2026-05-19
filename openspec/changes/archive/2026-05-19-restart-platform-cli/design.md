## Context

运维人员需要在本地运行一个 CLI 工具，通过 SSH 连接远程服务器并依次重启两个服务。工具面向内部使用，优先快速跑通，不需要生产级健壮性。

## Goals / Non-Goals

**Goals:**
- 交互式收集服务器地址、账号、密码，建立 SSH 连接
- 顺序执行两个重启步骤，流式输出远程命令日志
- 步骤间要求用户确认，防止误操作
- 固定路径配置通过 `~/.restart_platform/config.yaml` 管理

**Non-Goals:**
- 密码加密存储
- 多服务器并发操作
- 健康检查或自动回滚
- 生产级错误处理和重试

## Decisions

### 使用 paramiko 做 SSH 连接
选 paramiko 而非系统 `ssh` 命令，原因：Python 原生控制输入/输出流，密码认证无需 sshpass 等额外工具，跨平台一致。

### 使用 questionary 做交互提示
questionary 提供密码不回显输入，交互体验比 input() 好，且无需复杂配置。

### SSH 执行方式：exec_command + 流式读取 stdout
每条命令单独调用 `exec_command`，实时读取 stdout/stderr 并打印，用户能即时看到脚本输出。docker-compose down && up 作为一条 shell 命令执行（`bash -c "..."`)以保证同一会话。

### 配置文件仅存路径，不存凭证
密码运行时输入后仅保留在内存，不写入任何文件，降低安全风险。

## Risks / Trade-offs

- [SSH 密码认证被禁用] → 工具无法连接。缓解：文档说明前提条件，未来可扩展支持密钥
- [脚本执行超时] → 当前不设超时，长时间等待会阻塞。缓解：快速跑通阶段可接受
- [docker-compose down 失败后仍执行 up] → 使用 `&&` 串联，down 失败则 up 不执行
