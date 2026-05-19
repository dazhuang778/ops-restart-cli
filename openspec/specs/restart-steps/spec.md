### Requirement: 执行 Normandy 重启脚本
系统 SHALL 通过 SSH 执行 `/data/app/normandy-5101/bin/normandy_restart.sh`，并流式输出执行日志。

#### Scenario: 脚本执行成功
- **WHEN** 步骤一被触发
- **THEN** 系统执行 normandy_restart.sh 并实时输出日志，完成后提示成功

#### Scenario: 脚本执行失败
- **WHEN** normandy_restart.sh 返回非零退出码
- **THEN** 系统输出失败信息，不继续执行步骤二

### Requirement: 执行 Sentinel docker-compose 重启
系统 SHALL 在 `/data/workspace/nova-omp-sentinel` 目录下执行 `docker-compose down && docker-compose up -d`，并流式输出日志。

#### Scenario: docker-compose 重启成功
- **WHEN** 步骤二被触发
- **THEN** 系统先执行 down，成功后执行 up -d，实时输出日志

#### Scenario: docker-compose down 失败
- **WHEN** docker-compose down 返回非零退出码
- **THEN** 系统不执行 docker-compose up -d，输出失败信息
