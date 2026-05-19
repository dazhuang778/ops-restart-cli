## ADDED Requirements

### Requirement: SSH 密码认证连接
系统 SHALL 使用 paramiko 通过用户名+密码方式连接远程服务器，连接失败时输出错误信息并退出。

#### Scenario: 连接成功
- **WHEN** 用户提供正确的 host、user、password
- **THEN** 系统建立 SSH 连接并输出"SSH 连接成功"

#### Scenario: 连接失败
- **WHEN** 用户提供错误的凭证或服务器不可达
- **THEN** 系统输出错误信息并以非零状态退出

### Requirement: 流式命令输出
系统 SHALL 执行远程命令时实时将 stdout 和 stderr 输出到本地终端，不等命令完成后再输出。

#### Scenario: 脚本有输出
- **WHEN** 远程命令产生输出
- **THEN** 每行输出实时打印到本地终端

#### Scenario: 命令执行失败
- **WHEN** 远程命令返回非零退出码
- **THEN** 系统输出错误提示，当前步骤终止
