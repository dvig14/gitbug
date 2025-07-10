from datetime import datetime 
from .display import display 
import re

def currtime():
    return f"{datetime.today().strftime('%Y-%m-%dT%H:%M:%S')}"


def prompt(emoji, field, emoji_width=2, space=1, field_width=35):
    label = f"{field:<{field_width}}"
    emoji_padded = f"{emoji:<{emoji_width}}" 
    inp = input(f"{emoji_padded} {label}: {' ' * space}").strip()

    if inp:
        if field in {'Title','Description'}:
            if re.fullmatch(r'^(?=.*\b[a-zA-Z]+\b)(?:\S+\s+){1,}\S+$', inp):
               return inp
            else:
                display.print(f"Invalid input for [yellow]{field}[/]. Please enter a string with at least [magenta]two words[/]")
                return prompt(emoji, field, emoji_width, space, field_width)

        elif field in {'Priority (low,medium,high)'}:
            if re.fullmatch(r'(?i)^(low|medium|high)$', inp):
                return inp
            else:
                display.print(f"[red]Invalid input[/] for {field}.")
                return prompt(emoji, field, emoji_width, space, field_width)
        
        return inp
    else:
        display.print(f"[red]Bug must have[/] {field}")
        return prompt(emoji, field, emoji_width, space, field_width)


def bug_id_validation_prompt(bugs, open_only=False):
    bug_map = {bug['id']: bug for bug in bugs}

    while True:
        bug_id = prompt("🐞", "Bug ID")

        try:
            bug_id_int = int(bug_id)
        except ValueError:
            print("❌ Invalid input. Please enter a valid numeric Bug ID(1,2,....).")
            continue

        bug = bug_map.get(bug_id_int)

        if not bug:
            display.print(f"❌ Bug [red]#{bug_id_int}[/] not found.")
            from gitbugsim.bug_simulator.bug_ops import print_open_bugs 
            print_open_bugs(bugs)
            continue
        
        if open_only and bug["status"] not in {"open", "reopened"}:
           print(f"\n🚫 Bug #{bug_id_int} is '{bug['status']}' — only 'open' or 'reopened' allowed.")
           print("🔍 Showing available bugs you *can* work on:\n")
           # local import to break circular chain
           from gitbugsim.bug_simulator.bug_ops import print_open_bugs 
           print_open_bugs(bugs) 
           continue

        return bug 


def scenario_id_validation_prompt(scenario):
    while True:
        id_val = prompt("🧪", "Scenario (Id / None)")
       
        if re.fullmatch(r'^(None|[1-9][0-9]*)$', id_val):
            if id_val == "None":
               return None 
            
            is_present = scenario.get(int(id_val))
            if is_present:
                return int(id_val)  
            else:
                display.print(f"""❌ Scenario [red]#{id_val}[/] not found.
Create a Scenario first and then add bug [grren]python cli.py add.[/]
Until it's considered None""")
                return None
        else:
            display.print(f"Enter either [blue]None[/] or [yellow]number[/]")
            continue


def available_fields():
    print("\n🔧 Available Configuration\n" + "="*50)
    print("\n🧠 Roles: reporter, manager, developer, reviewer")
    print("""\n👥 Users:
  manager: lead-dev, project-mgr, triage-bot
  developer: dev1, dev2, dev3, dev5
  reporter: reporter1, reporter2, reporter4
  reviewer: reviewer1, reviewer2 """)
    print("\n🛠️  Status: open, in-progress, fixed, closed, reopened")
    print("\n🏷️  Tags: ui, backend, performance, urgent, production, critical, payment, deployment, database, api, security, frontend, build")
    print("="*50)



false_errors = [
    ("commit", "nothing to commit"),
    ("commit", "working tree clean"),
    ("commit", "untracked files"),
    ("commit", "changes not staged for commit"),
    ("rebase", "no tracking information for the current branch."),
    ('rebase', 'please specify which branch you want to rebase against')
]


warning_phrases = [
    ("add", "nothing specified, nothing added"),
    ("add", "maybe you wanted to say"),
    ("checkout", "updated 0 paths from the index"),
    ("checkout", "already on")
]