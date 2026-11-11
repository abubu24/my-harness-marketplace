"""위험한 명령을 실행 전에 막는 PreToolUse Hook.

막는 것
  - rm -rf, PowerShell Remove-Item -Recurse -Force, rmdir /s
  - git push --force / -f
  - .env 파일 읽기 (Read 도구)

Bash, PowerShell, Read 도구에 건다(matcher "Bash|PowerShell|Read").
Hook 입력(JSON, stdin)의 tool_input 을 검사하고,
막을 때는 exit 2 와 함께 이유를 stderr 로 돌려준다.
"""
import json
import re
import sys
from pathlib import PurePath

RULES = [
    (r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f|\brm\s+-[a-zA-Z]*f[a-zA-Z]*r",
     "rm -rf 는 막혀 있습니다. 지울 파일을 사람에게 확인받으세요."),
    (r"(?i)\bRemove-Item\b(?=.*-Recurse)(?=.*-Force)|\brmdir\s+/s\b",
     "재귀 강제 삭제는 막혀 있습니다. 지울 파일을 사람에게 확인받으세요."),
    (r"\bgit\s+push\b.*(--force\b|\s-f\b)",
     "git push --force 는 막혀 있습니다. 일반 push 를 쓰세요."),
]

ENV_FILE = re.compile(r"^\.env(\..+)?$")
ENV_ALLOWED = {".env.example", ".env.sample", ".env.template"}


def main() -> int:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    tool_input = data.get("tool_input") or {}

    file_path = tool_input.get("file_path", "")
    if file_path:
        name = PurePath(file_path.replace("\\", "/")).name
        if ENV_FILE.match(name) and name not in ENV_ALLOWED:
            print(f"[guard] 차단: Read {file_path}\n이유: .env 파일은 읽지 않습니다.", file=sys.stderr)
            return 2

    command = tool_input.get("command", "")
    for pattern, reason in RULES:
        if re.search(pattern, command):
            print(f"[guard] 차단: {command}\n이유: {reason}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
