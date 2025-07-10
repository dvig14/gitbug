from .git_utils import get_commit_log

feedback_hooks={}

def git_feedback(cmd):
    """Decorator to register Git feedback functions."""
    def decorator(func):
      feedback_hooks[cmd] = func
      return func
    return decorator

@git_feedback("add")
def feedback_git_add(parts, repo_path):
    return f"\n✅ Staged {'all' if '.' in parts else f'{len(parts[1:])}'} file(s)."

@git_feedback("commit")
def feedback_git_commit(parts, repo_path):
    last_commit = get_commit_log(repo_path, 1)
    return f"\n💾 Saved commit: {last_commit[0] if last_commit else 'unknown'}"

@git_feedback('diff')
def feedback_git_diff(parts='',repo_path=''):
    return """
🔍 Nothing to show — there are no changes in this diff.

[green]✔️ Everything is up-to-date in this context.[/]
"""

