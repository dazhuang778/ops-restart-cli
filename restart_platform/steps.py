import sys


def run_normandy_restart(ssh, script_path, estimated_secs=120):
    print(f"\n步骤 1：重启 Normandy  ({script_path})")
    exit_code = ssh.run(
        f"bash {script_path}",
        description="Normandy 重启中",
        estimated_secs=estimated_secs,
    )
    if exit_code != 0:
        print(f"✗ Normandy 重启失败（退出码 {exit_code}）")
        sys.exit(exit_code)
    print("✓ Normandy 重启完成")


def run_sentinel_restart(ssh, workdir, estimated_secs=120):
    print(f"\n步骤 2：重启 Nova-OMP-Sentinel  ({workdir})")
    exit_code = ssh.run(
        f"cd {workdir} && docker-compose down && docker-compose up -d",
        description="Sentinel 重启中",
        estimated_secs=estimated_secs,
    )
    if exit_code != 0:
        print(f"✗ Sentinel 重启失败（退出码 {exit_code}）")
        sys.exit(exit_code)
    print("✓ Sentinel 重启完成")
