#!/usr/bin/env python3
"""
自動執行 git status -> add -> commit -> push 的工具腳本。

用法：
    python .github/auto_push.py
    python .github/auto_push.py --message "更新內容"
    python .github/auto_push.py --remote origin
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path


def run_command(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    """執行指令並回傳結果。"""
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def ensure_git_repo(repo_root: Path) -> None:
    result = run_command(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo_root)
    if result.returncode != 0 or result.stdout.strip() != "true":
        raise RuntimeError(f"{repo_root} 不是有效的 Git 專案。")


def get_current_branch(repo_root: Path) -> str:
    result = run_command(["git", "branch", "--show-current"], cwd=repo_root)
    if result.returncode != 0:
        raise RuntimeError(f"取得目前分支失敗：{result.stderr.strip()}")
    branch = result.stdout.strip()
    if not branch:
        raise RuntimeError("目前沒有可用的 Git 分支。")
    return branch


def main() -> int:
    parser = argparse.ArgumentParser(
        description="自動檢查變更、提交並推送到 Git 遠端。"
    )
    parser.add_argument(
        "--message",
        default=None,
        help="提交訊息；未提供時自動使用時間戳記。",
    )
    parser.add_argument(
        "--remote",
        default="origin",
        help="要推送的遠端名稱（預設：origin）。",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    ensure_git_repo(repo_root)

    # 先顯示目前狀態
    status = run_command(["git", "status", "--short"], cwd=repo_root)
    if status.returncode != 0:
        print(status.stderr, file=sys.stderr)
        return 1

    if status.stdout.strip():
        print("Detected changes:")
        print(status.stdout)
    else:
        print("No changes detected. Nothing to commit.")
        return 0

    # 加入所有變更
    add_result = run_command(["git", "add", "."], cwd=repo_root)
    if add_result.returncode != 0:
        print(add_result.stderr, file=sys.stderr)
        return 1

    # 產生提交訊息
    if args.message:
        commit_message = args.message
    else:
        now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"auto push: {now}"

    # 提交
    commit_result = run_command(
        ["git", "commit", "-m", commit_message],
        cwd=repo_root,
    )
    if commit_result.returncode != 0:
        if "nothing to commit" in commit_result.stdout or "nothing to commit" in commit_result.stderr:
            print("No changes to commit after staging.")
        else:
            print(commit_result.stderr or commit_result.stdout, file=sys.stderr)
            return 1

    # 推送目前分支
    branch = get_current_branch(repo_root)
    push_result = run_command(["git", "push", args.remote, branch], cwd=repo_root)
    if push_result.returncode != 0:
        print(push_result.stderr or push_result.stdout, file=sys.stderr)
        return 1

    print(push_result.stdout.strip())
    print(f"Successfully pushed to {args.remote}/{branch}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
