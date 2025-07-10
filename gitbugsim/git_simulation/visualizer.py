import subprocess, os, time, re
from .git_utils import get_staged_files, get_modified_files, get_commit_log, get_transitions, run_git_command
from .git_feedback_hooks import feedback_hooks
from collections import defaultdict
from gitbugsim.utils.display import display
from rich.table import Table
import shutil 


def get_git_state(repo_path):   
    return {
        "working_dir": get_modified_files(repo_path),
        "staging_area": get_staged_files(repo_path),
        "commit_history": get_commit_log(repo_path)
    }


def get_clean_files(file_list):
    clean = set()

    for f in file_list:
        stripped = f.lstrip()
        if stripped.startswith(('•')):
            parts = stripped.split(maxsplit=1)
            if len(parts) > 1:
                clean.add(parts[1].strip())

    return clean


def animate_git_transition(cmd_type, parts, repo_path, pre_state):
    
    if cmd_type == 'add':
        files = [p.strip() for p in parts[1:] if not p.startswith('-')]
        target_files = set(files)
        working = get_clean_files(pre_state)

        if files == ["."]:
            if not working:
                display.print("⚠️  No untracked or unstaged files to add.",style='red')
                return
        else:
            missing_file = target_files - working
            if missing_file:
                display.print(f"[red]❌ Can't add: file [magenta]{missing_file}[/] not in working directory.[/]")
                return

    flow = get_transitions(parts).get(cmd_type)
    if not flow:
        return
    
    print("\n🎬 Transition")
    for f in flow:
        display.print(f)
        time.sleep(0.5)

    feedback_func = feedback_hooks.get(cmd_type)
    if feedback_func:
        print(feedback_func(parts, repo_path)) 



def show_git_state(repo_path):
    state = get_git_state(repo_path)

    working = state["working_dir"]
    staging = state["staging_area"]
    commits = state["commit_history"]

    max_len = max(len(working), len(staging), len(commits))
    terminal_width = shutil.get_terminal_size().columns
    col_width = terminal_width // 3 - 4
    print('\n')
    if display.rich_available:  
        table = Table(
            title="📊 Git State Visualization [yellow][For Explanation run : git> explain git-state][/]",
            show_header=True,
            show_lines=False,
            border_style="dim"
        )
        table.add_column("📁 Working Directory",header_style='dim',justify="center", width=col_width)
        table.add_column("📥  Staging Area",justify="center",header_style='green', style='green', width=col_width)
        table.add_column("🗃  Commit History",justify="center",header_style='blue', style='blue', width=col_width)

        for i in range(max_len):
            wd = working[i] if i < len(working) else ""
            st = staging[i] if i < len(staging) else ""
            ch = commits[i] if i < len(commits) else ""
            table.add_row(wd, st, ch)

        display.rprint(table)
    else:
        col_width = max((total_width - 6) // 3, 20)  
        header = f"{'📁 Working Dir'.ljust(col_width)} {'📥  Staging Area'.ljust(col_width)} {'🗃  Commit History'}"
        sep = "─" * (terminal_width)
        lines = [header, sep]
        for i in range(max_len):
            wd = working[i] if i < len(working) else ""
            st = staging[i] if i < len(staging) else ""
            ch = commits[i] if i < len(commits) else ""
            lines.append(f"{wd.ljust(col_width)}  {st.ljust(col_width)}  {ch}")
        display.panel("📊 Git State Visualization [For Explanation run : git> explain git-state]", "\n".join(lines), border_style="dim")



def show_graph_comparision(before, after, cmd):

    before_lines = before.strip().splitlines()
    after_lines = after.strip().splitlines()

    max_len = max(len(before_lines), len(after_lines))
    width = shutil.get_terminal_size().columns // 2 - 5

    lines = []
    header = f"{f'Before {cmd}'.ljust(width)} | {f'After {cmd}'.ljust(width)}"
    divider = f"\n{'-'*width} | {'-'*width}"
    lines.append(header)
    lines.append(divider)

    for i in range(max_len):
        left = before_lines[i] if i < len(before_lines) else ""
        right = after_lines[i] if i < len(after_lines) else ""
        lines.append(f"{left.ljust(width)} | {right.ljust(width)}")

    content = "\n".join(lines)
    print('\n')
    display.panel(
        f"📈 Git Graph Before vs After {cmd} [yellow][For Graph Explanation: git> explain git-log][/]\n",
        f"\n{content}\n",
        'dim'
    )
    


def list_git_dir(path):
    content_lines = []
    try:
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            emoji = "📁" if os.path.isdir(full_path) else "📄"
            content_lines.append(f"{emoji} {entry}")
        display.panel(f"📁 Contents from *.git* of {path}", "\n" + "\n".join(content_lines), border_style="dim")
    except Exception as e:
        display.print(f"❌ Could not list directory: {e}", style="red")
        exit(1)
