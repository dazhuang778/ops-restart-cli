## ADDED Requirements

### Requirement: 交互式收集服务器信息
系统 SHALL 在启动时提示用户依次输入服务器地址、登录账号、登录密码（密码输入不回显）。若配置文件中存在 default_host 和 default_user，SHALL 作为默认值预填。

#### Scenario: 用户输入完整信息
- **WHEN** 用户依次输入 host、user、password
- **THEN** 系统使用这些信息建立 SSH 连接

#### Scenario: 配置文件存在默认值
- **WHEN** config.yaml 中有 default_host 或 default_user
- **THEN** 对应提示显示默认值，用户可直接回车使用

### Requirement: 步骤间用户确认
系统 SHALL 在步骤一完成后，提示用户确认是否继续执行步骤二，用户输入 n 则退出。

#### Scenario: 用户确认继续
- **WHEN** 用户在确认提示输入 y 或直接回车
- **THEN** 系统继续执行步骤二

#### Scenario: 用户取消
- **WHEN** 用户在确认提示输入 n
- **THEN** 系统输出"已取消"并正常退出

### Requirement: 加载配置文件
系统 SHALL 从 `~/.restart_platform/config.yaml` 加载配置，文件不存在时使用内置默认路径。

#### Scenario: 配置文件存在
- **WHEN** `~/.restart_platform/config.yaml` 存在
- **THEN** 系统使用配置中的 normandy script 路径和 sentinel workdir

#### Scenario: 配置文件不存在
- **WHEN** `~/.restart_platform/config.yaml` 不存在
- **THEN** 系统使用内置默认路径继续运行，不报错退出
