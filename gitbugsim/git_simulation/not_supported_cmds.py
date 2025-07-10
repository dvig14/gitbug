no_sup_cmd_hooks = {}

def no_support_cmd(cmd):
    def decorator(func):
        no_sup_cmd_hooks[cmd] = func
        return func
    return decorator


@no_support_cmd('add -p')
def block_add_patch():
    return """
🚫 `git add -p` (patch mode) is not supported in this simulation.
🧭 Why? Interactive prompts are disabled in this environment.

✅ Try Instead:
• Stage everything → `git add .`
• Stage a file → `git add <filename>`
"""


@no_support_cmd("commit --amend")
def block_commit_amend():
    return """
⚠️  Interactive `git commit --amend` without -m is not supported here.
💡 Try: git commit --amend -m "New message"
"""


@no_support_cmd("rebase -i")
def block_rebase_interactive():
    return """
🚫 `git rebase -i` (interactive rebase) is not supported in this simulation.

🧠 Why?
• Interactive editors are disabled in CLI simulation.
• Rebase alters commit history — not safe to simulate blindly.

✅ What You Can Do:
• Use `git log` to view history
• Use `git reset` or `git revert` for safe changes
"""


@no_support_cmd("commit --interactive")
def block_commit_interactive():
    return """
🚫 `git commit --interactive` is not supported here.

💡 Alternative:
Use `git commit -m "your message"` instead.
"""


@no_support_cmd("merge --edit")
def block_merge_edit():
    return """
🚫 `git merge --edit` is not supported in simulation.

💡 Use:
`git merge <branch>` — commit message will auto-generate.
"""


@no_support_cmd("config --global")
def block_global_config():
    return """
❌ `git config --global` is not allowed in simulation mode.
🛡️ Reason: It changes your real Git config (~/.gitconfig), affecting ALL your real repositories.

✅ Allowed: git config user.name "Your Name"
            modifies only local repo's (i.e. this test repo only) .git/config
"""


@no_support_cmd("config --global --edit")
def block_global_edit():
    return """
🚫 `git config --global --edit` is not allowed in simulation mode.
🛡️ Reason: This opens and edits your real ~/.gitconfig file, which affects all Git projects on your system.

✅ Tip: Practice Git config safely using local-only:
   git config user.name "Simulated User"
   git config user.email "sim@example.com"
"""


@no_support_cmd("config --system")
def block_system_config():
    return """
🚫 `git config --system` is blocked for safety.
❌ This is beyond the scope of simulation and could cause unexpected behavior.
"""