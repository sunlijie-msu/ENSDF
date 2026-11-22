hooks:
  preToolUse:
    - type: command
      command: "python .github/hooks/scripts/block-root-file-creation.py"
      timeoutSec: 30
    - type: command
      command: "python .github/hooks/scripts/block-git-revert.py"
      cwd: "."
      timeoutSec: 30
    - type: command
      command: "python .github/hooks/scripts/guard_ens_edit.py"
      timeoutSec: 30
  postToolUse:
    - type: command
      command: "python .github/hooks/scripts/verify_ens_edit.py"
      timeoutSec: 30
  postToolUseFailure:
    - type: command
      command: "python .github/hooks/scripts/verify_ens_edit.py"
      timeoutSec: 30