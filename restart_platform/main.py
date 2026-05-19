import os
import sys
import yaml
import questionary
from ssh_client import SSHClient
from steps import run_normandy_restart, run_sentinel_restart
from server_history import list_servers, save_server, get_password

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_CONFIG = {
    "steps": {
        "normandy": {"script": "/data/app/normandy-5101/bin/normandy_restart.sh"},
        "sentinel": {"workdir": "/data/workspace/nova-omp-sentinel"},
    },
}

NEW_SERVER_OPTION = "+ 新服务器"


def load_config():
    config_path = os.path.expanduser("~/.restart_platform/config.yaml")
    if not os.path.exists(config_path):
        return DEFAULT_CONFIG
    with open(config_path, "r", encoding="utf-8") as f:
        user_cfg = yaml.safe_load(f) or {}
    cfg = DEFAULT_CONFIG.copy()
    steps = user_cfg.get("steps", {})
    cfg["steps"]["normandy"]["script"] = (
        steps.get("normandy", {}).get("script") or DEFAULT_CONFIG["steps"]["normandy"]["script"]
    )
    cfg["steps"]["sentinel"]["workdir"] = (
        steps.get("sentinel", {}).get("workdir") or DEFAULT_CONFIG["steps"]["sentinel"]["workdir"]
    )
    return cfg


def prompt_credentials():
    """选择已保存服务器或输入新服务器，返回 (host, user, password)。"""
    saved = list_servers()

    if saved:
        choices = [s["key"] for s in saved] + [NEW_SERVER_OPTION]
        choice = questionary.select("选择服务器:", choices=choices).ask()
        if choice is None:
            return None, None, None

        if choice != NEW_SERVER_OPTION:
            server = next(s for s in saved if s["key"] == choice)
            host, user = server["host"], server["user"]
            password = get_password(host, user)
            if password:
                print(f"  使用已保存的密码")
                return host, user, password
            # 密码丢失（如系统重装），重新输入
            print("  未找到已保存的密码，请重新输入")
            password = questionary.password("登录密码:").ask()
            return host, user, password

    # 新服务器
    host = questionary.text("服务器地址:").ask()
    if not host:
        return None, None, None
    user = questionary.text("登录账号:").ask()
    if not user:
        return None, None, None
    password = questionary.password("登录密码:").ask()
    if password is None:
        return None, None, None

    save = questionary.confirm("保存此服务器？", default=True).ask()
    if save:
        save_server(host, user, password)
        print(f"  已保存 {user}@{host}")

    return host, user, password


def main():
    print("\n┌─────────────────────────────────────┐")
    print("│        运维平台重启工具              │")
    print("└─────────────────────────────────────┘\n")

    cfg = load_config()

    host, user, password = prompt_credentials()
    if not host:
        print("已取消")
        sys.exit(0)

    ssh = SSHClient(host=host, user=user, password=password)
    ssh.connect()

    try:
        normandy_script = cfg["steps"]["normandy"]["script"]
        run_normandy_restart(ssh, normandy_script)

        confirmed = questionary.confirm("继续重启 Nova-OMP-Sentinel？", default=True).ask()
        if not confirmed:
            print("已取消")
            sys.exit(0)

        sentinel_workdir = cfg["steps"]["sentinel"]["workdir"]
        run_sentinel_restart(ssh, sentinel_workdir)

        print("\n✓ 全部完成")
    finally:
        ssh.close()


if __name__ == "__main__":
    main()
