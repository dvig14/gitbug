from .git_utils import run_git_command
from .visualizer import show_graph_comparision
from gitbugsim.utils.display import display

class GraphManager:

    def __init__(self):
       self.before_graph = None
       self.before_commit = None
       self.last_cmd = None

    def get_commit_hash(self,repo):
        returncode, stdout, stderr = run_git_command(repo, ["rev-parse", "HEAD"])
        if returncode == 0:
            return stdout

    def get_graph(self,repo):
        returncode, stdout, stderr = run_git_command(repo, ["log", "--graph", "--all", "--oneline", '--decorate'])
        if returncode == 0:
            return stdout
    
    def capture_if_needed(self, cmd, repo):
        graph_cmds = {'merge','rebase','reset','revert'}

        if cmd in graph_cmds:
            if self.last_cmd != cmd or self.before_graph is None:
              self.before_graph = self.get_graph(repo)
              self.before_commit = self.get_commit_hash(repo)
              self.last_cmd = cmd
    
    def show_if_changed(self, cmd, repo):
        if self.before_graph:
            after_commit = self.get_commit_hash(repo)

            if self.before_commit != after_commit:
                after_graph = self.get_graph(repo)
                show_graph_comparision(self.before_graph, after_graph, cmd)
            
            self.reset() 
            
    def reset(self):
        self.before_graph = None
        self.before_commit = None
        self.last_cmd = None

graph_tracker = GraphManager()