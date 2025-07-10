from .scenario_engine import ScenarioEngine
from gitbugsim.utils.display import display

def check_scenario_mode(scenario_map, bug, repo, bugs):
   
    scenario_engine = None
    scenario_id = bug.get('scenario_id')

    if scenario_map and scenario_id and not bug['scenario_status']['completed']: 
        scenario_name = scenario_map[bug['scenario_id']]['type']
        scenario_title = scenario_map[bug['scenario_id']]['title']
        icon = scenario_map[bug['scenario_id']]['icon']
        steps = scenario_map[bug['scenario_id']]['objective']

        scenario_engine = ScenarioEngine(bug, repo, steps, bugs)
        scenario_engine.start(scenario_name, icon, scenario_title)

    else:
        display.panel(f"🐛 Free Exploration: [red]Bug#{bug['id']}[/] - [magenta]{bug['title']}[/]", 
        "💡 Try This First : git status OR git add <file_name>", "dim")    

    return scenario_engine  


def check_scenario_progress(cmd, stdout, stderr, scenario_engine, parts):
    
    progress = scenario_engine.check_progress(cmd, stdout + stderr, parts)

    if progress == "completed":
        display.panel("[green]🎉 SCENARIO COMPLETE AND BUG FIXED![/]", 
        f"""
>[green] You've successfully completed all objectives!\n[/]"
> Now try [magenta]🔓 FREE EXPLORATION MODE[/] with these challenges:
    - Try alternative solutions
    - Experiment with different commands
> Or You can [yellow]exit[/] and then check bug list [yellow]python cli.py list[/]
""","dim")
        return None

    return scenario_engine


def handle_exit(scenario_engine):
    if scenario_engine:
        progress = scenario_engine.get_progress()
        display.panel("[yellow]⚠️  SCENARIO PAUSED[/]", 
                     f"You completed [green]{progress} %[/] of the scenario\n"
                     "Your progress will be saved", 
                     "dim")
    display.print("👋 Exiting Git simulation.", style='red') 


def handle_keyboard_interrupt(scenario_engine):
    if scenario_engine:
        progress = scenario_engine.get_progress()
        display.print(f"\n[yellow]⏸️  Scenario progress saved: [green]{progress} %[/] complete[/]")

    display.print("\n[red]KeyboardInterrupt caught.[/]\n👋 Exiting Git simulation.\n")
