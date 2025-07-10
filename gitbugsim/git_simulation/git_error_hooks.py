from gitbugsim.utils.display import display

check_error = {}

def git_error(keywords, command):
    """Decorator to register Git error functions."""
    def decorator(func):
        for cmd in command.split("/"):
            check_error.setdefault(cmd.strip(), []).append({
                "matchers": [kw.lower() for kw in keywords],
                "handler": func
            })
        return func
    return decorator


@git_error(["nothing to commit", "working tree clean","untracked files",'changes not staged for commit'],'commit')
def error_git_add(stderr):
    display.panel('[red]Nothing to Commit[/]', f"""
[red]❌ Git O/P[/] {stderr}

[cyan]🧠 Git couldn't find any staged changes to commit.[/]

[green]💡 Solution:[/]
    [yellow]git add <file>[/]  to stage your work first.

[cyan]🛠️ Example:[/]
    git add hello.py
    git commit -m "Added hello.py"

[magenta]📌 Note: Only staged changes are committed![/]
""", border_style='red')


@git_error(["pathspec", "did not match any file"], "commit")
def error_commit_message_not_quoted(stderr):
    display.panel("[red]Commit Message Not Quoted[/]", f"""
[red]❌ Git O/P[/] {stderr}

🧠 Git expected a filename but got unquoted text.

💡 Likely cause: You forgot quotes in your message.

[green]✅ Fix:[/]
   [yellow]git commit -m "fix: broken layout"[/]

[red]❌ Wrong:[/]
    [yellow]git commit -m fix broken layout[/]

[magenta]🛠️ Without quotes, Git treats `fix` and `broken` as a file name, not part of the message.[/]
""", border_style="red")


@git_error(["nothing specified, nothing added"], "add")
def error_git_add_nothing(stderr):
    display.panel('[red]Nothing added or specified[/]',"""
[red]❌ Git warning:[/] Nothing specified, nothing added.

💡 You ran `git add` without specifying what to add.

[yellow]👉 Try: `git add .` to stage everything in your working directory. or `git add <file-name>`[/]
""",border_style='red')


@git_error(["pathspec", 
   "did not match any file",
    "invalid reference",
    "ambiguous argument",
    "unknown revision",
    "bad revision"
], "checkout/switch/reset/revert/cherry-pick")
def error_branch_not_found(stderr):
    display.panel('[red]Invalid Branch or Commit[/]',f"""
[red]❌ Git O/P[/] {stderr}

[red]💡 Git couldn't find the branch, tag, or commit you're referring to. It doesn't exist[/]

[yellow]👉 Common fixes:[/]
    • Check for typos in branch/commit names
      • Use `git branch` to see existing branches
      • Use `git log` or `git log --oneline` to see commit history [cyan][For reset, revert, cherry-pick][/]
 
    • For [magenta]history-based[/] commands:
        git log --oneline
        git reset --soft HEAD~1

    • To create a [magenta]new branch[/] and switch to it:
        git checkout -b <branch-name>
                  OR
        git switch -c <branch-name>
""",border_style='red')


@git_error(["merge conflict"], "merge")
def error_merge_conflict(stderr):
    display.panel("[red]Merge Conflict Detected[/]", f"""
[red]❌ Git O/P[/] {stderr}

⚠️ A merge conflict occurred while merging branches.

[yellow]👉 Steps to resolve:[/]
    1. Open conflicted files (look for <<<<<<< markers)
    2. Edit and keep the correct code
    3. Run: git add <file>
    4. Run: git commit -m "Resolve conflict"

[magenta]🧠 Conflicts happen when both branches modify the same lines.[/]
""", border_style="red")


@git_error(["usage: git revert","usage: git cherry-pick"], "revert/cherry-pick")
def error_revert_usage(stderr):
    display.panel("[red]Missing Commit in cmd[/]", f"""
[red]❌ Git O/P :[/] {stderr}

[cyan]🧠 You tried to run [yellow]`git revert`[/] or [yellow]`git cherry-pick`[/] without specifying a commit.[/]

[yellow]👉 Correct usage:[/]
    git <cmd_name> <commit-hash>

[green]🛠️ Example:[/]
    git log --oneline
    git <cmd_name> abc1234
""", border_style="red")


@git_error(["cannot do a partial commit during a merge"], "commit")
def error_merge_not_concluded(stderr):
    display.panel("[red]Merge Not Finished[/]", f"""
❌ Git O/P {stderr}

[red]💡 You're in the middle of a merge and must complete it.[/]

- You're trying to commit only some files (a partial commit) while a merge is in progress.
- But Git requires you to commit all conflict resolutions together, not partially.

[yellow]👉 After resolving conflicts:[/]
    git add <file>
    git commit

❌ To cancel the merge entirely:
    git merge --abort
""", border_style="red")


@git_error(["no upstream branch"], "push")
def error_push_no_upstream(stderr):
    display.panel("[red]⛔ Push Rejected: No Upstream Branch Set[/]", f"""
[red]❌ Git O/P[/] {stderr}


[magenta]🧠 This happens when your local branch is not connected to any remote branch (upstream).
    Git doesn't know *where* to push by default.[/]


[cyan]💡 You can fix this by setting the upstream:[/]
    
    [yellow]git push --set-upstream origin main[/]

> This command links your local `main` to `origin/main`, so future `git push` and `git pull` will work **without arguments**.


[cyan]🚀 Did you know?[/]
   
    [green]git push origin main[/] also works,

> But you'll have to **type it every time** since it doesn't store the remote link.

🔍 To understand how remotes and upstreams work: [yellow]explain remote[/]
""", border_style="red")


@git_error(["ambiguous argument 'HEAD'", 
    "unknown revision or path not in the working tree"
], "log/show/diff/checkout")
def error_head_ambiguous(stderr):
    display.panel("[red]⛔ HEAD is Ambiguous: No Commits Yet[/]", f"""
[red]❌ Git O/P[/] {stderr}


[magenta]🧠 This happens when your repository has been initialized with [bold]git init[/], but [cyan]no commits[/] have been made yet.
    Git can't resolve [yellow]HEAD[/] because there's nothing to point to.[/]


[cyan]💡 You can fix this by making the first commit:[/]

    [yellow]echo "# My Project" > README.md
    git add README.md
    git commit -m "Initial commit"[/]

> After this, HEAD will point to the first commit, and commands like [yellow]git log[/], [yellow]git show HEAD[/], etc. will work properly.

[cyan]🚨 Reminder:[/]
> You're in a special state called the [yellow]"unborn branch"[/]. Until your first commit, HEAD is not a real reference.

🔍 To learn what HEAD actually is: [yellow]explain branch[/]
""", border_style="red")


@git_error([
    "Updates were rejected because the tip of your current branch is behind",
    "failed to push some refs",
    "non-fast-forward"
], "push")
def error_push_non_fast_forward(stderr):
    display.panel("[red]⛔ Push Rejected: Non-Fast-Forward[/]", f"""
[red]❌ Git O/P[/] {stderr}

[magenta]🧠 What happened?[/]
Your [yellow]git push[/] failed because the [green]remote branch[/] has commits that your local branch doesn’t.

Git protects the branch from being overwritten accidentally.  
This is known as a [cyan]non-fast-forward[/] error.

---

[cyan]✅ You have two options to fix this:[/]

📦 Option 1: Integrate remote changes (recommended)

    [yellow]git pull origin master --rebase
    git push origin master[/]

This safely rebases your local commits on top of the latest remote ones.

---

⚠️ Option 2: Force Push (only in simulations or if you're 100% sure)

    [yellow]git push --force origin master[/]

> ⚠️ Warning: This rewrites remote history and may disrupt others' work.  
> Use only if you're in a learning environment or working solo.

---

🔍 Learn More:
- [cyan]Fast-forward vs non-fast-forward pushes[/]: [yellow]explain push[/]
- [cyan]Safe rebasing[/]: [yellow]explain rebase[/]

""", border_style="red")

