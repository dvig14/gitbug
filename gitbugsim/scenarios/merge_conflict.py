import os, re
from gitbugsim.git_simulation.git_utils import run_git_command, get_commit_log, get_current_branch
from gitbugsim.utils.display import display
from .remote_engine import RemoteManager  


def clean_commit_msg(commits):
    clean = set()
    for commit in commits:
        parts = commit.split(':',1)
        if len(parts) > 1:
            clean.add(parts[1].strip())
    return clean


def check_fetched(repo,cmd):
    custom_fetch_path = os.path.join(repo, '.git/FETCH_HEAD_CUSTOM')
    
    if not os.path.exists(custom_fetch_path):
        run_git_command(repo,['fetch','origin'])
        with open(custom_fetch_path, "w") as f:
            f.write('fetched')
        
        if cmd != 'fetch':
            return True 

    return False


def setup_merge_conflict(bug, repo):
    css_path = os.path.join(repo, "login.css")
    initial_css = """
    .login-button {
       position: relative;
       padding: 10px 20px;
       background-color: #4CAF50;
       color: white;
    }"""

    with open(css_path, "w") as f:
        f.write(initial_css)

    
    remote_branch = get_current_branch(repo)
    RemoteManager.init(repo, bug, remote_branch)
    remote = RemoteManager.get(f'bug-{bug['id']}') 
    
    commits = clean_commit_msg(get_commit_log(repo))
    if 'Initial button styles' not in commits:
      run_git_command(repo, ["add", "login.css"])
      run_git_command(repo, ["commit", "-m", "Initial button styles"])
      run_git_command(repo, ["push", "origin", remote_branch])

    
    return f"""
  [green]🐞 BUG ASSIGNED[/]
  > You 🧑‍💻 : {bug['assigned_to']}
  > [red]Bug#{bug['id']}[/] [magenta]'{bug['title']}'[/] assigned 
  > Follow the [cyan]objectives[/] to complete the scenario
   
  > [yellow]📄 login.css[/] file and here it's current state which is causing alignment issue:
      {initial_css}

  > [magenta]Remote simulation enabled[/]:
      - A fake remote repo has been created
      - Teammate repo initialized
      - Initial commit already done 
      - Intial login.css file Pushed to remote.

  > 💡 To understand merge, merge_conflict run: 
        [yellow]git> explain merge[/] 
                or 
        [yellow]git> explain merge_conflict[/]
"""


def check_branch_created(command, output, repo, parts):
    return ("checkout" in command) or ("switch" in command)


def check_commit_with_fix(command, output, repo, parts):
    if "commit" not in command:
        return False
    
    returncode, stdout, stderr = run_git_command(repo, ["show", "--pretty=format:", "--name-only", "HEAD"])
    if returncode != 0 or 'login.css' not in stdout:
        display.panel("[red]❌ login.css Not Committed[/]",
    f"""
The file [yellow]login.css[/] was not included in your last commit!

[green]✅ How to fix:[/]
1. Make change to file and then see: [yellow]git status[/].
2. Add the file: [yellow]git add login.css[/]
3. Amend your commit: [yellow]git commit --amend[/]
   [magenta]Note: The simulation doesn't support this command directly[/]
   [dim]💡 To understand how amending works: [yellow]git> explain commit --amend[/][/]
4. Keep the same commit message when amending

[green]📝 Alternative approach:[/]
If amending doesn't work in this simulation:
1. Create a new commit with the file:
   [yellow]git add login.css[/]
   [yellow]git commit -m 'fix: add missing login.css'[/]
""","dim")
        return False

    
    returncode, content, stderr = run_git_command(repo, ["show", "HEAD:login.css"])
    absolute = re.search(r"position\s*:\s*absolute", content, re.IGNORECASE)
    
    if not absolute:
        display.panel(
            "[red]⚠️ Missing Required Changes[/]",
            f"""
 > The committed version of login.css doesn't contain the required changes!
 > [magenta]🎯 Expected to find: 'position: absolute'[/]

 > 💡 Fix it by:
    1. Reset your changes: [yellow]git reset --soft HEAD~1[/]
       - [cyan]💡 This unstages the commit, but keeps your edits intact[/]

    2. Add the position: absolute style to login.css
    
    3. Run [yellow]git status[/] to inspect changes:
       - [cyan]Working directory:[/] Your latest modifications
       - [green]Staging area:[/] Currently holds the old version
    
    4. Stage the file: [yellow]git add login.css[/]
       - [cyan]💡 This replaces the staged version with the latest one[/]

    5. Re-commit: [yellow]git commit -m 'fix: apply correct button position'[/]

---
[magenta]💡 To Know how reset works? Run: [yellow]git> explain reset[/][/]
""","dim")
        return False

    
    remote = RemoteManager.get('bug-1')
    if not remote.teammate_pushed:
        remote.teammate_setup(
            file_path="login.css",
            original="position: relative",
            change="position: fixed",
            commit_msg="Teammate: change to fixed"
        )

    return True



def check_merge_attempted(command, output, repo, parts):
    if command not in {'merge','fetch'} or 'not something we can merge' in output:
        return False   

    remote = RemoteManager.get('bug-1')
    current_branch = get_current_branch(repo)

    if check_fetched(repo,command):
        display.panel(f"⚠️ Detected: Your local `{remote.remote_branch}` is outdated!",
    f"""
We Ran [green]git fetch origin[/] and checked that your branch is outdated.

[yellow]📍 Result:[/]
Your local `{remote.remote_branch}` is behind `origin/{remote.remote_branch}` — new commits exist remotely!
---

✅ [cyan]Why this matters:[/]
Merging with an outdated `{remote.remote_branch}` can cause:
   [red]❌ Merge conflicts[/] that could've been caught earlier
   [red]❌ Broken features[/] when you push
   [red]❌ PR rejections[/] due to stale base branches
---

✅ [cyan]Best Practice Before You Merge:[/]
    [yellow]git checkout {remote.remote_branch}[/]
    [yellow]git pull origin {remote.remote_branch}[/]  ← brings in latest remote commits
    [yellow]git checkout feature[/]
    [yellow]git merge {remote.remote_branch}[/]        ← now safe to merge

💡[cyan] Alternative shortcut:[/]
    [yellow]git fetch origin[/]
    [yellow]git merge origin/{remote.remote_branch}[/]  ← merges remote tracking branch directly

---
[cyan]To learn more about this, run:[/] [yellow]git> explain local_remote[/]
""","yellow")
        return False
    

    
    if 'merge' in command:
        if len(parts) < 2 or f"origin/{remote.remote_branch}" not in parts[1].strip():
           display.panel(f"[red]❌ Incomplete Merge Command[/]",
f"""
You ran [yellow]merge[/], but didn't specify the correct remote branch to merge from. 🤔

🔍 [cyan]Why this matters:[/cyan]
- If you just run [yellow]git merge[/yellow] or [yellow]git merge {remote.remote_branch}[/yellow], Git tries to merge your [green]local {remote.remote_branch}[/green], which might be outdated.
- But your real teammate's work is on [yellow]origin/{remote.remote_branch}[/yellow] — the **remote** version.

---

🧠 [cyan]Clarifying the Confusion: Local vs Remote[/cyan]

| Situation                                 | What Happens                                                                                                 |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| ✅ `git pull origin {remote.remote_branch}` is run         | Your local `{remote.remote_branch}` is now up to date. Merging it into `{current_branch}` is safe.                                    |
| ❌ Only `git fetch origin` is run          | Your local `{remote.remote_branch}` is still outdated. If you merge just `{remote.remote_branch}`, you'll miss changes from `origin/{remote.remote_branch}`. |
| ⚠️ You merge `{remote.remote_branch}` without updating it | You might avoid a merge conflict, but also miss important teammate changes.                                  |
| ✅ You merge `origin/{remote.remote_branch}` directly      | This is safest after fetch — no need to touch local `{remote.remote_branch}`.                                                |

---

✅ [cyan]Correct Merge Command (after fetch):[/cyan]

    [yellow]git merge origin/{remote.remote_branch}[/]

This ensures you're merging the **latest remote teammate commits**, not stale local history.
""",'dim')        
           return False
    else:
        return False  

    
    
    css_path = os.path.join(repo, "login.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            content = f.read()
        
        if '<<<<<<<' in content and '>>>>>>>' in content:
            display.panel(
                "[red]⚠️ Merge Conflict Detected![/]",
                f"""
[green]✅ How to resolve:[/]
1. Open [yellow]login.css[/] and resolve conflicts:
   - Keep your `position: absolute` change
   - Remove conflict markers: <<<<<<<, =======, >>>>>>>

2. Save the file and mark as resolved:
   [yellow]git add login.css[/]

3. Commit the result:
   [yellow]git commit -m 'Merge: resolve conflict'[/]


[blue]💡 Why did this conflict happen?[/]
- You and your teammate both edited the [yellow]position[/] property in the same line.
- Since you didn't integrate their change on your branch before making your edit, Git can't automatically merge


[yellow]💡 Best Practices to Avoid Future Conflicts:[/]

1. [cyan]Always update before starting work:[/]
   - Before creating a new branch: 
        [yellow]git checkout {remote.remote_branch}
        git pull origin {remote.remote_branch}[/]
   - This ensures you're working with the latest code

2. [cyan]Regularly merge {remote.remote_branch} into your branch:[/]
   - While working on your feature:
        [yellow]git checkout {current_branch}
        git merge {remote.remote_branch}[/]
   - This catches conflicts early when they're smaller

3. [cyan]Communicate with teammates:[/]
   - Let your team know what files you're working on
   - Coordinate on shared files

4. [cyan]Smaller, focused changes:[/]
   - Make smaller PRs with focused changes
   - Avoid large, long-running branches

5. [cyan]Consider [yellow]rebase[/] workflow:[/]
   - Instead of merging, you can rebase:
        [yellow]git checkout {current_branch}
        git rebase {remote.remote_branch}[/]
   
   - This rewrites your history to apply your changes *after* {remote.remote_branch}'s latest commits
   - It helps avoid messy merge commits


[magenta]💡 Bonus Tip:[/]
In a future scenario, you'll face a similar conflict —
but you'll solve it using [yellow]git rebase[/] instead of merge.

This helps keep your history linear and cleaner — and teaches another powerful Git technique.
""","red")
    
    return True



def check_conflict_resolved(command, output, repo, parts):
    
    if "commit" not in command and not ("add" in command and parts[1].strip() in {'login.css','.'}):
        return False

    is_commit_cmd = "commit" in command
    remote = RemoteManager.get('bug-1')

    source = "HEAD:login.css" if is_commit_cmd else ":login.css"
    returncode, content, stderr = run_git_command(repo, ["show", source])

    if returncode != 0:
        if is_commit_cmd:
            display.panel("[red]❌ login.css not found in last commit[/]", 
                      "Make sure you committed the resolved file.", "red")
        return False
       
    absolute = re.search(r"position\s*:\s*absolute", content, re.IGNORECASE)
    fixed = re.search(r"position\s*:\s*fixed", content, re.IGNORECASE) 
   
    if absolute and not fixed:
        returncode, head_content, _ = run_git_command(repo, ["show", "HEAD:login.css"])
        
        absolute_found = re.search(r"position\s*:\s*absolute", head_content, re.IGNORECASE)
        fixed_found = re.search(r"position\s*:\s*fixed", head_content, re.IGNORECASE)
           
        if returncode == 0 and absolute_found and not fixed_found:
            if command == 'add':
               display.panel("[blue]💡 Git Insight: Why `login.css` disappeared after `git add`[/]",
        f"""
You ran [yellow]git add login.css[/], but Git still shows a clean state — nothing to commit. 🤔

🧠 What's happening?

- In your **previous commit for login.css**, you changed [green]'position: relative;'[/] to [green]'position: absolute;'[/].
- Now, after resolving the merge conflict, you changed it again — back to [green]'position: absolute;'[/].
- And now, you made the **exact same change** again.
- Since there's no difference compared to what's already in history, Git treats this as a [cyan]no-op add[/].

> Git tracks commits as [green]snapshots of the entire file tree[/] at the time of each commit.

> Under the hood, Git stores each file as a blob object, and commits reference these blobs in a tree.
    - Each commit represents a full snapshot of the project.
    - If files don’t change, Git reuses the same blob hash and won't re-stage.
    - That’s why when your working tree, staging area, and HEAD all match — Git shows:
      [green]"nothing to commit, working tree clean"[/]

----
  
  [yellow]"Great job![/]
  [green]✅ Conflict Resolved Correctly![/] 🎉
  
  Your working tree and history already reflect the correct fix

----

[magenta]🛠️ To complete the merge process anyway:[/]

Since Git sees nothing new to commit, but the merge still needs to be finalized, run this to **force a merge commit**:

> [yellow]git commit --allow-empty -m "Merge: resolved conflict (duplicate of earlier change)"[/]
> Now you can run: `merge origin/{remote.remote_branch}` 

----

[green]✅ Success:[/green] You've just learned an advanced Git behavior!
Git is smart enough to skip redundant history — and now, so are you. 🧠
""",'dim')  
            
            remote.cleanup()
            RemoteManager.reset(1)
            return True      
    
    
    if is_commit_cmd:
        display.panel("[red]❌ Incorrect Resolution[/]", 
f"""
The committed version of [yellow]login.css[/] is incorrect —  
it does not contain the required fix: [green]'position: absolute'[/].

🧠 You likely committed the wrong version after resolving the merge conflict.

---

✅ [green]How to fix it (recommended):[/]

1. Edit [yellow]login.css[/] and change it to use [green]'position: absolute'[/]
2. Stage the file again: [yellow]git add login.css[/]
3. Commit the corrected resolution: [yellow]git commit -m "fix: correct resolution"[/]
4. Then after that simply can do [yellow]`merge origin/{remote.remote_branch}`[/]

> This is the safest and cleanest way to fix a bad conflict resolution.

---

⚠️ [magenta]Avoid using:[/] [yellow]git reset --soft HEAD~1[/]

Reset can break Git's internal merge state and make future merges more confusing.

> 💡 You'll learn about [yellow]`reset`[/] safely in a future scenario. For now, stick to a new commit on top.
""", "red")

    return False


