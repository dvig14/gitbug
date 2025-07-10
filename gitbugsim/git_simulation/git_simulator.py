import shlex
from gitbugsim.utils.file_ops import load_file
from gitbugsim.utils.config import BUG_FILE, SCENARIO_FILE
from gitbugsim.utils.common import bug_id_validation_prompt
from .git_utils import (
    setup_git_repo_for_bug, run_git_command, git_valid_cmds, 
    check_output, clear_screen, explain_cmd, 
    check_supported_cmds, display_branch_prompt,
    get_modified_files, check_cmd_syntax
)
from .visualizer import list_git_dir, show_git_state, animate_git_transition, show_graph_comparision
from .git_command_hooks import command_hooks 
from gitbugsim.scenarios.scenario_simulator import (
    check_scenario_mode, check_scenario_progress,
    handle_keyboard_interrupt, handle_exit
)
from gitbugsim.utils.display import display
from .graph_manager import graph_tracker
    

def simulate_git_for_bug():
    bugs = load_file(BUG_FILE)
    scenarios = load_file(SCENARIO_FILE) 
    scenario_engine = None

    scenario_map = None
    if scenarios:
       scenario_map = {scenario['id']: scenario for scenario in scenarios}
    
    if not bugs:
       display.print("\nNo 🐞 bugs reported. Run [cyan]python cli.py add[/] to start\n", style="red")
       return
   
    try:
        bug = bug_id_validation_prompt(bugs)
        repo = setup_git_repo_for_bug(bug['id'],bug['title'])

        display.print(f"\n[green]📁 Git repo for Bug#{bug['id']}[/] [yellow]{str(repo.resolve())}[/]")
        list_git_dir(repo / ".git")

        if input("❓ Want to know how `.git` works? (y/n): ").lower() == "y":
           command_hooks["init"]()

        print('\n')
        scenario_engine = check_scenario_mode(scenario_map, bug, repo, bugs)

        display.print("\n💡 Type 'exit' anytime to stop simulation.",style="yellow")
        display.print("💡 Type 'clear' to clear screen.",style='yellow')
        display.print("\n💡 Type 'explain <git_command>' for detailed explanation.",style='cyan')
        display.print("💡 Type 'explain <git_command> [flag]' (eg:explain add -p).\n",style='cyan')    
        
        while True:
            cmd = display_branch_prompt(repo, bug['id'])
            
            if not cmd:
                continue
            if cmd.lower() == "exit":
                handle_exit(scenario_engine)
                break
            if cmd.lower() == "clear":
                clear_screen()
                continue
            if cmd.lower() == 'hint' and scenario_engine:
                scenario_engine.show_hint()
                continue
 
            try:
                parts = shlex.split(cmd)
            except ValueError as e:
                display.print(f"Skipping invalid command: {cmd}\nReason: {e}",style='red')
                continue

            if cmd.startswith('explain'):
                explain_cmd(parts,command_hooks) 
                continue

            git_cmd = parts[0].lower()
            if git_cmd == "git":
                display.print("🏁 **git** prefix already handled automatically just run cmds (status, add, commit etc..)\n",style='green')
                continue
                         
            if git_cmd not in git_valid_cmds(repo):
                display.print(f"❌ `{git_cmd}` is not a valid Git command.\n", style="red")
                continue
            
            is_cmd_supported = check_supported_cmds(parts)
            if not is_cmd_supported:
                continue
            
            pre_state = None
            if git_cmd in {'add'}:
                pre_state = get_modified_files(repo)
             
            is_syntax_correct = check_cmd_syntax(git_cmd,parts)
            if not is_syntax_correct:
                continue
            
            graph_tracker.capture_if_needed(git_cmd, repo)
            returncode, stdout, stderr = run_git_command(repo, parts)
            not_error, feedback = check_output(returncode, stdout, stderr, git_cmd)

            if scenario_engine:
                if not_error:
                    scenario_engine = check_scenario_progress(git_cmd, stdout, stderr, scenario_engine, parts)
                elif git_cmd in {'merge'} and len(parts) > 1:
                    scenario_engine = check_scenario_progress(git_cmd, stdout, stderr, scenario_engine, parts)

            if git_cmd in {'checkout','switch'}:
                continue

            if not_error:
                if git_cmd in {'add','commit'}:
                    animate_git_transition(git_cmd, parts, repo, pre_state)
               
                if git_cmd in {'merge','rebase','reset','revert'}:
                    graph_tracker.show_if_changed(git_cmd,repo)
               
                if git_cmd not in {'log', 'branch'}:
                    show_git_state(repo)

            if not_error and feedback and input(f"\n❓ Want to see *Git Output* ? (y/n):").lower() == 'y':
                display.panel("Git Output", feedback, border_style="dim") 
            
    except KeyboardInterrupt:
        handle_keyboard_interrupt(scenario_engine)


    
