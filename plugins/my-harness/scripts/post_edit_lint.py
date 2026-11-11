"""파일을 고친 뒤 프로젝트의 린터를 돌리는 PostToolUse Hook.

린트 규칙은 프로젝트마다 다르므로 이 플러그인에는 넣지 않는다.
프로젝트에 scripts/arch_lint.py 가 있으면 그것을 실행하고, 없으면 아무것도 하지 않는다.
  - pyproject.toml 과 uv 가 있으면 `uv run python scripts/arch_lint.py`
  - 아니면 지금 파이썬으로 실행

린터가 exit 2 로 끝나면 stderr 의 수정 지침을 그대로 에이전트에게 돌려준다.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

LINT_SCRIPT = Path("scripts") / "arch_lint.py"


def main() -> int:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    sys.stdin.read()
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
    script = root / LINT_SCRIPT
    if not script.is_file():
        return 0

    if (root / "pyproject.toml").is_file() and shutil.which("uv"):
        cmd = ["uv", "run", "--project", str(root), "python", str(script)]
    else:
        cmd = [sys.executable, str(script)]

    result = subprocess.run(cmd, cwd=root, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        sys.stderr.write(result.stderr or result.stdout)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
