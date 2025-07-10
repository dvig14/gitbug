from gitbugsim.utils.file_ops import load_file
from gitbugsim.utils.common import available_fields, prompt, scenario_id_validation_prompt
from gitbugsim.bug_simulator.bug_ops import add_bug, assign_bug, available_tags_chck, print_bug, print_open_bugs, specific_bug
from gitbugsim.utils.config import BUG_FILE, SCENARIO_FILE
from gitbugsim.utils.auth import is_valid_user_for_role

def add_bug_cli():
    scenarios = load_file(SCENARIO_FILE)
    scenario_map = {scenario['id'] : scenario for scenario in scenarios}

    available_fields()
    print("\n🐞 Let's Report a New Bug!\n" + "-"*32)

    title = prompt("📝", "Title") 
    description = prompt("🧾", "Description", 2, 0) 
    scenario_id = scenario_id_validation_prompt(scenario_map)
    reported_by = is_valid_user_for_role("Reported by", "reporter", "report", "✍️", 4) 
    tags = available_tags_chck()

    add_bug(title, description, scenario_id, reported_by, tags)


def assign_bug_cli():
    bugs = load_file(BUG_FILE)
    
    if not bugs:
       print("\nNo 🐞 bugs reported. Run python cli.py add\n")
       return
    
    available_fields()
    print("\n🐞 Assign a Bug!\n" + "-"*32)
    bug_map = {bug["id"]: bug for bug in bugs}
    bug_id = prompt("🐞", "Bug ID")

    while True:
        if bug_id.lower() == 'q':
            print("🎯 Assignment cancelled.")
            return

        try:
            bug_id_int = int(bug_id)
        except ValueError:
            print("❌ Invalid input. Please enter a valid numeric Bug ID(1,2,....).")
            bug_id = prompt("🐞", "Bug ID (or 'q' to quit)")
            continue

        bug_to_update = bug_map.get(bug_id_int)

        if not bug_to_update:
            print(f"❌ Bug #{bug_id} not found.")
            bug_id = prompt("🐞", "Bug ID (or 'q' to quit)")
        else:
            assign_bug(bugs, bug_id_int, bug_to_update)
            return


def list_bugs_cli():
    bugs = load_file(BUG_FILE)
    scenarios = load_file(SCENARIO_FILE)
    scenario_map = {scenario['id'] : scenario for scenario in scenarios} if scenarios else None

    if not bugs:
       print("No 🐞 bugs reported. Run python cli.py add")
       return

    print("""What do you want to list?
    1. 🐞 All bugs
    2. 🛠️  Open and Reopened bugs
    3. 📝 Specific bug with id
    """)

    choice = prompt("🔢","Enter choice (1, 2 or 3)").strip()

    if choice == "1":
        print("📃 Listing all bugs:\n")
        for bug in bugs:
          print_bug(bug,scenario_map)
    elif choice == "2":
        print_open_bugs(bugs)
    elif choice == "3":
        specific_bug(bugs,scenario_map)
    else:
        print("❌ Invalid option. Please choose 1, 2 or 3.")
