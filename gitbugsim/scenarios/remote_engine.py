import os
import shutil
from pathlib import Path
import json
from gitbugsim.utils.display import display
from gitbugsim.git_simulation.git_utils import run_git_command, get_current_branch

BUG_REMOTE_BASE = Path('./user_simulation/remote_teammate')

class RemoteEngine:

    def __init__(self, repo, bug, branch):
        self.user_repo = repo
        self.remote_path = BUG_REMOTE_BASE / 'remote_repos' / f'bug-{bug['id']}'
        self.teammate_path = BUG_REMOTE_BASE / 'teammate_repos' / f'bug-{bug['id']}'
        self.teammate_pushed = False
        self.remote_branch = branch  
    
    def setup(self):
        self.remote_path.mkdir(parents=True, exist_ok=True)

        git_refs = self.remote_path / 'refs'
        if not git_refs.exists():
           run_git_command(self.remote_path, ["init", "--bare"])
        
        remotes = run_git_command(self.user_repo, ["remote"])[1]
        if "origin" in remotes:
            run_git_command(self.user_repo, ["remote", "remove", "origin"])

        run_git_command(self.user_repo, ["remote", "add", "origin", self.git_path(self.remote_path)])
        run_git_command(self.user_repo, ["fetch", "origin"])
    
    
    def teammate_setup(self, file_path=None, original=None, change=None, commit_msg="Teammate:"):

        done_flag = self.teammate_path / ".teammate_pushed"
        if done_flag.exists():
            self.teammate_pushed = True
            return
       
        if not self.teammate_path.exists():
           run_git_command(None, ["clone", self.git_path(self.remote_path), self.git_path(self.teammate_path)])

        
        branches = run_git_command(self.teammate_path, ["branch"])[1]
        if "teammate/fix-alignment" not in branches:
            run_git_command(self.teammate_path, ["checkout", "-b", "teammate/fix-alignment"])
        else:
            run_git_command(self.teammate_path, ["checkout", "teammate/fix-alignment"])  

        
        if file_path and original and change:
            full_path = os.path.join(self.teammate_path, file_path)
            if not os.path.exists(full_path):
                display.print(f"[red]❌ Teammate file missing: {file_path}[/]")
                return
            
            with open(full_path, "r") as f:
                content = f.read()
            
            new_content = content.replace(original, change)
            if new_content != content:
                with open(full_path, "w") as f:
                   f.write(new_content)
                run_git_command(self.teammate_path, ["add", file_path])
                run_git_command(self.teammate_path, ["commit", "-m", commit_msg])
        
        
        merge_base = run_git_command(self.teammate_path, ["merge-base", self.remote_branch, "teammate/fix-alignment"])[1].strip()
        latest_commit = run_git_command(self.teammate_path, ["rev-parse", "teammate/fix-alignment"])[1].strip()
        
        if merge_base != latest_commit:
           run_git_command(self.teammate_path, ["checkout", self.remote_branch])
           run_git_command(self.teammate_path, ["merge", "teammate/fix-alignment"])
        
        run_git_command(self.teammate_path, ["push", "origin", self.remote_branch])
        done_flag.touch()
        self.teammate_pushed = True

    @staticmethod
    def git_path(p:Path):
        return str(p.resolve().as_posix())
    
    def cleanup(self):
        if self.teammate_path.exists():
            shutil.rmtree(self.teammate_path, ignore_errors=True)

        fetch_marker = os.path.join(self.user_repo, ".git", "FETCH_HEAD_CUSTOM")
        if os.path.exists(fetch_marker):
           os.remove(fetch_marker)

        display.print(f"""
        [yellow][INFO] 🧹 Remote exits but teammate repos cleaned up.
        You can manually [red]delete remote repo[/] whenever you want.
        As of know you can play around it.[/]
        """)




REMOTE_STATE_FILE = Path("./user_simulation/remote_teammate/remote_state.json")

class RemoteManager:
    _instance = None
    _initialized = False
    _instance_bug_id = None

    @classmethod
    def init(cls, repo, bug, branch):
        bug_id = f"bug-{bug['id']}"
        cls._instance = RemoteEngine(repo, bug, branch)
        cls._instance.setup()
        cls._initialized = True
        cls._instance_bug_id = bug_id

        state = cls._load_state()
        state[bug_id] = {
            "repo": str(repo),
            "bug": bug,
            "branch": branch
        }
        cls._save_state(state)


    @classmethod
    def get(cls, bug_id=None):
        if cls._initialized and cls._instance:
            return cls._instance

        if REMOTE_STATE_FILE.exists():
            try:
                state = cls._load_state()

                if not bug_id:
                   bug_id = list(state.keys())[-1]

                if bug_id not in state:
                   raise ValueError(f"No saved state for {bug_id}")
                
                bug_state = state[bug_id]
                bug = bug_state["bug"]
                branch = bug_state["branch"]
                repo = Path(bug_state["repo"])
                
                cls._instance = RemoteEngine(repo, bug, branch)
                cls._instance.setup()
                cls._initialized = True
                cls._instance_bug_id = bug_id
                
                return cls._instance
            
            except Exception as e:
                raise RuntimeError(f"[RemoteManager] Failed to restore state: {e}")

        raise RuntimeError("[RemoteManager] Not initialized. You must call init(repo, bug, branch) first.")

    
    @classmethod
    def reset(cls, bug_id=None):
        cls._instance = None
        cls._initialized = False
        cls._instance_bug_id = None

        state = cls._load_state()
        if not state:
            return

        if bug_id:
            state.pop(bug_id, None)
        else:
            state.clear()

        if state:
            cls._save_state(state)
        elif REMOTE_STATE_FILE.exists():
            REMOTE_STATE_FILE.unlink()
    

    @staticmethod
    def _load_state():
        if REMOTE_STATE_FILE.exists():
            try:
                return json.loads(REMOTE_STATE_FILE.read_text())
            except json.JSONDecodeError:
                return {}
        return {}


    @staticmethod
    def _save_state(state):
        REMOTE_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        REMOTE_STATE_FILE.write_text(json.dumps(state, indent=2))
