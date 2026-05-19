import os
import yaml
import keyring

HISTORY_PATH = os.path.expanduser("~/.restart_platform/servers.yaml")
KEYRING_SERVICE = "restart_platform"


def _load() -> list[dict]:
    if not os.path.exists(HISTORY_PATH):
        return []
    with open(HISTORY_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("servers", [])


def _save(servers: list[dict]):
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        yaml.dump({"servers": servers}, f, allow_unicode=True)


def list_servers() -> list[dict]:
    return _load()


def save_server(host: str, user: str, password: str):
    servers = _load()
    key = f"{user}@{host}"
    existing = next((s for s in servers if s["key"] == key), None)
    if existing:
        servers.remove(existing)
    servers.insert(0, {"key": key, "host": host, "user": user})
    _save(servers)
    keyring.set_password(KEYRING_SERVICE, key, password)


def get_password(host: str, user: str) -> str | None:
    return keyring.get_password(KEYRING_SERVICE, f"{user}@{host}")


def delete_server(host: str, user: str):
    key = f"{user}@{host}"
    servers = [s for s in _load() if s["key"] != key]
    _save(servers)
    try:
        keyring.delete_password(KEYRING_SERVICE, key)
    except keyring.errors.PasswordDeleteError:
        pass
