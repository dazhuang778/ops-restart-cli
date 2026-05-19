# restart-platform

运维平台重启 CLI 工具，通过 SSH 依次重启 Normandy 和 Nova-OMP-Sentinel。

## 安装

```bash
cd restart_platform
pip install -r requirements.txt
```

## 配置（可选）

```bash
mkdir -p ~/.restart_platform
cp config.example.yaml ~/.restart_platform/config.yaml
# 按需编辑 default_host、default_user 和路径
```

## 使用

```bash
python main.py
```

启动后依次输入服务器地址、账号、密码，工具将自动完成两步重启流程。
