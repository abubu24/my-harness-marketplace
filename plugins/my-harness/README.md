# my-harness

practice-m3 하네스에서 프로젝트 전용 내용을 뺀 플러그인.

## 들어 있는 것
- `agents/verifier.md`: spec 기준 검증. 고치지 않고 보고만 한다.
- `agents/cleaner.md`: 죽은 코드 · 중복 · 어긋난 문서 정리. 기능은 추가하지 않는다.
- `hooks/hooks.json`
  - PreToolUse `guard.py`: rm -rf, 재귀 강제 삭제, git push --force, `.env` 읽기를 막는다.
  - PostToolUse `post_edit_lint.py`: 프로젝트에 `scripts/arch_lint.py`가 있으면 실행한다.

## 프로젝트 쪽에서 채울 것
에이전트는 spec 위치, 테스트 · 린트 명령, 종료 조건을 프로젝트의 CLAUDE.md에서 찾는다.
린트 규칙은 각 프로젝트의 `scripts/arch_lint.py`에 둔다. (위반 시 exit 2 + stderr에 수정 지침)

## 설치
```
/plugin marketplace add abubu24/my-harness-marketplace
/plugin install my-harness@my-harness-marketplace
```

Hook은 `python` 명령으로 실행되므로 PATH에 파이썬이 있어야 한다.
