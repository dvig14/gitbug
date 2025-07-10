import os, re, subprocess
from pathlib import Path  
from .not_supported_cmds import no_sup_cmd_hooks  
from gitbugsim.utils.display import display
from gitbugsim.utils.common import false_errors , warning_phrases
from .git_error_hooks import check_error  


BUG_REPO_BASE = Path("./user_simulation/local_repos")
EXPLANATION_PATH = Path(__file__).resolve().parent.parent / "explanations"


def load_explanation(command_path, cmd_name):
    filepath = EXPLANATION_PATH / Path(*command_path.split("/")).with_suffix(".md")
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            display.panel(cmd_name,file.read(),border_style='cyan')
    except FileNotFoundError:
        display.print(f"❌ Explanation for `{command_path}` not found.", style="red")



def explain_cmd(parts, command_hooks):
    if len(parts) < 2:
        display.print("⚠️  Usage: explain <git_command>", style="yellow")
        return

    cmd_name = parts[1].lower()
    flag = parts[2].lower() if len(parts) > 2 and parts[2].startswith('-') else None
    full_key = f"{cmd_name} {flag}" if flag else cmd_name

    if full_key in command_hooks:
        command_hooks[full_key]()
    else:
        display.print(f"❌ No explainer available for *{full_key}*", style="red")
    return
  


def check_supported_cmds(parts):
    cmd_name = parts[0].lower()
    flags = [p.lower() for p in parts[1:] if p.startswith('-')] if len(parts) > 1 else None
    
    if cmd_name in no_sup_cmd_hooks:
        display.panel('❌ Not supported command',no_sup_cmd_hooks[cmd_name](),border_style='red')
        return False

    if flags:
        full_cmd = f"{cmd_name} {' '.join(flags)}"
        if full_cmd in no_sup_cmd_hooks:
            display.panel('❌ Not supported command',no_sup_cmd_hooks[full_cmd](),border_style='red')
            return False

    return True



def get_git_status(repo_path, cmd):
    try:
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        display.print(f"❌ Unexpected Error: {str(e)}", style="red")
        return []


def get_modified_files(repo_path):
    lines = get_git_status(repo_path,["git", "status", "--short"])
    symbols = {
        "?": "[red]?? - Untracked files (new)[/]" , 
        "M": "[red]M - Modified/Unstaged (already tracked)[/]", 
        "U": "[red]U - Unmerged files (conflict)[/]",
        "D": "[red]D - Deleted files (already tracked)[/]"
    }
    files = {
        "[red]?? - Untracked files (new)[/]": [],
        "[red]M - Modified/Unstaged (already tracked)[/]": [],
        "[red]U - Unmerged files (conflict)[/]": [],
        "[red]D - Deleted (already tracked)[/]": []
    }

    for line in lines:
        working_status, filename = line[1:2].strip(), line[3:].strip()  
        if working_status not in symbols:
            continue

        label = symbols.get(working_status)
        files[label].append(filename)

    files_flat = []
    for category, f in files.items():
        if f:
            files_flat.append(f"\n{category}")
            for file in f:
                files_flat.append(f" • {file}")

    return files_flat if len(files_flat) != 0 else ["(no untracked, unstaged files)"]


def get_staged_files(repo_path):
    files = get_git_status(repo_path,["git", "diff", "--cached", "--name-only"])
    return [f"\n📥  {file.strip()}" for file in files] if len(files) != 0 else ["(no files staged for commits)"]


def get_commit_log(repo_path,max_count=5):
    commits = get_git_status(repo_path,["git", "log", f"--pretty=format:%h: %s", f"--max-count={max_count}"])
    return [f"\n{commit.strip()}" for commit in commits] if len(commits) != 0 else ["(no commits)"]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def git_valid_cmds(repo_dir):
    try:
        result = subprocess.run(
            ["git", "--list-cmds=main,others,alias,nohelpers"],
            cwd=repo_dir,
            capture_output=True,
            text=True
        )
        cmds = set(result.stdout.strip().splitlines())
        return cmds
    except Exception as e:
        display.print(f"⚠️  Could not load Git commands: {e}", style="red")
        return {"init", "status", "add", "commit", "log", "merge", "checkout", "branch"}



def handle_git_error(stderr, command):
    stderr_lower = stderr.lower()
    handlers = check_error.get(command, [])

    for hook in handlers:
        if any(keyword in stderr_lower for keyword in hook["matchers"]):
            hook["handler"](stderr)
            return True

    return False  


def check_output(returncode, stdout, stderr, git_cmd):
    stderr_lower = stderr.lower()
    stdout_lower = stdout.lower()

    for cmd, phrase in false_errors:
        if git_cmd == cmd and phrase in stdout_lower:
            if handle_git_error(stdout, git_cmd):
                return False, None
            if stdout:
                display.print(f"\n{stdout}")
            return False, None
    
    for cmd, phrase in warning_phrases:
        if git_cmd == cmd and phrase in stderr_lower:
            if handle_git_error(stderr, git_cmd):
                return False, None
            display.print(f"[yellow]Git says:[/]\n{stderr}")
            return False, None
  
    if returncode != 0:
        if handle_git_error(stderr, git_cmd):
            return False, None
        display.print(f"[red]Git error:[/]\n{stderr}")
        return False, None

    from .git_feedback_hooks import feedback_hooks 
    feedback = None 
    if not stdout:
        if git_cmd in feedback_hooks and git_cmd not in {'add','commit'}:
           feedback = feedback_hooks[git_cmd](parts='',repo_path='')
    else:
        feedback = stdout
    return True , feedback


def run_git_command(repo_dir, command_list):
    try:
        result = subprocess.run(["git"] + command_list, cwd=repo_dir, capture_output=True, text=True)
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        return result.returncode, stdout, stderr
    except FileNotFoundError:
        display.print("❌ Git is not installed or not found in PATH.", style="red")
        exit(1)
    except Exception as e:
        display.print(f"❌ Unexpected Error: {str(e)}", style="red")
        return False, '', str(e)



def setup_git_repo_for_bug(bug_id,bug_title):
    repo_path = BUG_REPO_BASE / f"bug_{bug_id}"
    repo_path.mkdir(parents=True, exist_ok=True)
    
    sanitized_title = re.sub(r'[^a-zA-Z0-9_-]', '', bug_title.lower().replace(" ", "-"))
    file1_path = repo_path / f"{sanitized_title}.py"
    file1_path.touch(exist_ok=True)

    file2_path = repo_path / "main.py"
    file2_path.touch(exist_ok=True)

    git_dir = repo_path / ".git"
    if not git_dir.exists():
        subprocess.run(["git", "init"], cwd=repo_path, check=True)
    return repo_path


def get_current_branch(repo):
    returncode, stdout, stderr = run_git_command(repo, ["symbolic-ref", "--short", "HEAD"])
    if returncode == 0:
        return stdout
    else:
        return 'detach-head'

def display_branch_prompt(repo , bug_id):
    branch = get_current_branch(repo)
    branch_display = f"(🌿 {branch})"
   
    if 'detach-head' in branch:
        branch_display = "HEAD-detached"
        warning = f"\n[yellow]⚠ WARNING : Detached HEAD — commits here may be lost if not saved by creating branch![/]"
        display.print(warning)

    return input(f"(bug-{bug_id}) {branch_display} git> ").strip()



def get_transitions(parts):
    join_parts = (' ').join(parts) 
    transitions = {
        "add": [
            "[red]🗂  Working Directory[/]",
           f"[yellow]↓  git {join_parts}[/]",
            "[green]📥  Staging Area[/]"
        ],
        "commit": [
            "[green]📥  Staging Area[/]",
           f"[yellow]↓  git {join_parts}[/]",
            "[blue]🗃  Commit History[/]"
        ]
    }
    return transitions


def check_cmd_syntax(git_cmd,parts):
    
    if git_cmd == 'commit' and len(parts) == 1:
        display.print(f""" 
 > This simulation doesnt have interactive mode.
 > [red]Don't support[/] [magenta]vim/nano[/]
 > [yellow]💡 Alternative: Use `git commit -m "your message"` instead.[/]
 """)
        return False
    
    elif git_cmd == 'checkout' and len(parts) == 1:
        display.print(f""" 
 > Must have given branch name. It's missing.
 > [yellow]💡 Use: `git checkout -b branch-name`.[/]
 """)
        return False

    return True