from gitbugsim.git_simulation.git_utils import run_git_command, get_current_branch
from gitbugsim.utils.display import display
from gitbugsim.utils.common import currtime
from gitbugsim.utils.file_ops import save_bugs
from .scenario_hook import scenario_hook

class ScenarioEngine:

    def __init__(self, bug, repo, steps, bugs):
        self.bug = bug
        self.repo = repo
        self.steps = steps
        self.bugs = bugs
        self.current_step = self.bug['scenario_status']['current_step']
        self.now = currtime()
      
    def start(self, scenario_name, icon, scenario_title):
        scenario_setup = scenario_hook.get(scenario_name)
        setup_message = scenario_setup(self.bug, self.repo) if scenario_setup and self.current_step == 0 else ""

        display.panel(
            f"[red]🧩 SCENARIO MODE[/]: [magenta]{icon} {scenario_title}[/]", 
    f"""
  > You'll experience a real {scenario_name} while fixing a bug
  {setup_message}  {self.show_current_step()}
    ""","dim")


    def show_current_step(self):
        step = self.steps[self.current_step]
        return f"""
  🎯 OBJECTIVE [green]{self.current_step+1}[/]/[yellow]{len(self.steps)}[/] : [cyan]{step['name']}[/]
     > 📝{step["description"]}
   
  💡 Type [yellow]hint[/] for help with current objective."""


    def show_hint(self):
        step = self.steps[self.current_step]
        display.print(f"💡 Hint: {step['hint']}", style="yellow")


    def check_progress(self, command, output, parts):
        step = self.steps[self.current_step]
        check_func_name = step.get('check_func', '')
        
        if not check_func_name:
            return ''
        
        check_func = scenario_hook.get(check_func_name)
        if not check_func:
            display.print(f"❌ Check function {check_func_name} not found", style="red")
            return ''
       
        if check_func(command, output, self.repo, parts):
            self.current_step += 1
            self.bug_history_update('in-progress') if self.current_step == 1 else None
            self.bug['scenario_status']['current_step'] = self.current_step 
            self.bug['scenario_status']['last_attempt'] = self.now

            if self.current_step < len(self.steps):       
                display.panel(f"✅ Objective [green]{step['name']}[/] completed!", 
                f"""[yellow]🏆 Well done![/]\n👇 Now onto the next step:\n{self.show_current_step()}""",
                "dim")  
            else:
                self.bug['scenario_status']['completed'] = True
                self.bug_history_update('fixed')
                return "completed"
        
        save_bugs(self.bugs)
        return "in_progress"


    def get_progress(self):
        return int((self.current_step/len(self.steps))*100)


    def bug_history_update(self, status):
        history_entry = {
            "action": "status updated",
            "from": self.bug['status'],
            "to": status,
            "by": self.bug["assigned_to"],
            "role": "developer",
            "timestamp": self.now
        }
        self.bug['updated_at'] = self.now
        self.bug['status'] = status
        self.bug['history'].append(history_entry)
        save_bugs(self.bugs)
    
