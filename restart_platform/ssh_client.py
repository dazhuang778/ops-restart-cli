import sys
import threading
import paramiko
from rich.progress import Progress, SpinnerColumn, BarColumn, TimeElapsedColumn, TextColumn


class SSHClient:
    def __init__(self, host, user, password, port=22):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self._client = None

    def connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                hostname=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                timeout=10,
            )
        except Exception as e:
            print(f"SSH 连接失败：{e}")
            sys.exit(1)
        self._client = client
        print(f"✓ SSH 连接成功 ({self.user}@{self.host})")

    def run(self, command, description="执行中", estimated_secs=120):
        """执行命令，底部显示进度条，输出实时打印在进度条上方。"""
        done = threading.Event()
        exit_code = [None]

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            TextColumn("/ 预计 {task.fields[est]}"),
        ) as progress:
            task = progress.add_task(
                description, total=estimated_secs, est=f"{estimated_secs}s"
            )

            def _exec():
                _, stdout, _ = self._client.exec_command(command, get_pty=True)
                for line in iter(stdout.readline, ""):
                    progress.console.print(line, end="")
                exit_code[0] = stdout.channel.recv_exit_status()
                done.set()

            threading.Thread(target=_exec, daemon=True).start()

            while not done.wait(0.1):
                elapsed = progress.tasks[task].elapsed or 0
                progress.update(task, completed=min(elapsed, estimated_secs * 0.95))

            progress.update(task, completed=estimated_secs)

        if exit_code[0] != 0:
            print(f"命令退出码：{exit_code[0]}")
        return exit_code[0]

    def close(self):
        if self._client:
            self._client.close()
