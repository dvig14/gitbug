from .git_utils import load_explanation

command_hooks = {}

def git_explainer(command):
    """Decorator to register Git command explainer functions."""
    def decorator(func):
        command_hooks[command.lower()] = func
        return func
    return decorator

@git_explainer("init")
def explain_git_init(): 
    load_explanation("init/main",'init')

@git_explainer("add")
def explain_git_add():
    load_explanation("add/main",'add')

@git_explainer("add -p")
def explain_git_add_p():
    load_explanation("add/patch",'add -p')

@git_explainer("status")
def explain_git_status():
    load_explanation("status/main", 'status')

@git_explainer("commit")
def explain_git_commit():
    load_explanation("commit/main", 'commit')

@git_explainer("commit --amend")
def explain_git_commit_amend():
    load_explanation("commit/amend", 'commit --amend')

@git_explainer('log')
def explain_git_log_visual():
    load_explanation("log/main", 'log')

@git_explainer('diff')
def explain_git_log_visual():
    load_explanation("diff/main", 'diff')

@git_explainer('git-log')
def explain_git_log_visual():
    load_explanation("visuals/git_log", 'git-log-visual')

@git_explainer('git-state')
def explain_git_log_visual():
    load_explanation("visuals/git_state", 'git-state-visual')

@git_explainer("branch")
def explain_git_branch():
    load_explanation("branch/main", 'branch')

@git_explainer("checkout")
def explain_git_checkout():
    load_explanation("branch/checkout", 'checkout')

@git_explainer("merge")
def explain_git_merge():
    load_explanation("branch/merge", 'merge')

@git_explainer("merge_conflict")
def explain_git_merge_conflict():
    load_explanation("branch/merge_conflict", 'merge conflict')

@git_explainer("merge_conflict")
def explain_git_merge_conflict():
    load_explanation("branch/merge_conflict", 'merge conflict')

@git_explainer("remote")
def explain_git_merge_conflict():
    load_explanation("remote/main", 'Git Upstream, Push, Remote & Fetch')

@git_explainer("reset")
def explain_git_merge_conflict():
    load_explanation("reset/main", 'reset')

@git_explainer("local_remote")
def explain_git_merge_conflict():
    load_explanation("branch/local_remote", 'local vs remote')