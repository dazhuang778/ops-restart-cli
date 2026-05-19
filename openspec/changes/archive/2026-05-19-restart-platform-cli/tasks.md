## 1. 项目初始化

- [x] 1.1 创建项目目录结构（restart_platform/）
- [x] 1.2 创建 requirements.txt，添加 paramiko、questionary、pyyaml
- [x] 1.3 创建示例配置文件 config.example.yaml

## 2. SSH 连接模块

- [x] 2.1 实现 ssh_client.py：paramiko 密码认证连接
- [x] 2.2 实现流式命令执行方法（实时输出 stdout/stderr）
- [x] 2.3 实现连接失败时的错误处理和退出

## 3. 重启步骤模块

- [x] 3.1 实现 steps.py：run_normandy_restart()，执行 normandy_restart.sh
- [x] 3.2 实现 steps.py：run_sentinel_restart()，执行 docker-compose down && docker-compose up -d

## 4. CLI 入口

- [x] 4.1 实现 main.py：加载 ~/.restart_platform/config.yaml，文件不存在时用内置默认值
- [x] 4.2 实现交互提示：host、user、password（questionary，密码不回显），支持默认值预填
- [x] 4.3 调用步骤一，步骤完成后询问用户是否继续
- [x] 4.4 用户确认后调用步骤二，完成后输出汇总结果

## 5. 收尾

- [x] 5.1 本地测试：验证 SSH 连接和命令执行流程
- [x] 5.2 补充 README，说明安装和使用方式
