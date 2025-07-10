import json
from gitbugsim.utils.file_ops import load_file, save_bugs
from gitbugsim.utils.common import currtime, prompt, bug_id_validation_prompt
from gitbugsim.utils.auth import invalid_msg, is_valid_user_for_role
from gitbugsim.utils.config import BUG_FILE


################################################## ADD bug ################################################

def available_tags_chck():
    while True:
        tags_inp = prompt("🏷️", "Tags (comma-separated)", 4, 0)
        tags = list(map(str.lower, tags_inp.split(',')))

        allowed_tags = {"ui", "backend", "performance", "urgent", "production", "critical", "payment", "deployment", "database", "api", "security", "frontend", "build"}
        invalid_tags = [tag for tag in tags if tag.strip() not in allowed_tags]

        if invalid_tags:
            invalid_msg("tags", invalid_tags)
        else:
            return [tag.strip() for tag in tags]


def add_bug(title, description, scenario_id, reported_by, tags):
    bugs = load_file(BUG_FILE)
    bug_id = (bugs[-1]["id"] + 1) if bugs else 1
    now = currtime()

    history_entry = {
        "action": "reported",
        "by": reported_by,
        "role": "reporter",
        "timestamp": now
    }
    
    new_bug = {
        "id": bug_id,
        "title": title,
        "description": description,
        "scenario_id": scenario_id,
        "status": "open",
        "priority": None,
        "assigned_to": None,
        "reported_by": reported_by,
        "created_at": now,
        "updated_at": now,
        "tags": tags,
        "history": [history_entry]
    }

    if scenario_id:
        new_bug["scenario_status"] = {
           "completed": False,
           "current_step": 0,
           "last_attempt": None
        }

    bugs.append(new_bug)
    save_bugs(bugs)
    print(f"✅ Bug #{bug_id} reported. You can check list now (python cli.py list)")
    

################################################## ASSIGN bug ################################################

def assign_bug(bugs, bug_id, bug_to_update):

    bug_assigned_already = bug_to_update["assigned_to"]
    old_status = bug_to_update["status"]
    allowed_status_reassign = {"open", "in-progress", "reopened"}

    assigned_by = is_valid_user_for_role("Assigned by", "manager", "assign", "👤")

    if bug_assigned_already:
        print(f"\n🐞 Bug #{bug_id} is already assigned to {bug_assigned_already}")

        if old_status not in allowed_status_reassign:
            print(f"❌ Cannot assign bug #{bug_id} because it is currently {old_status}.")
            print("➡️  Reopen the bug first if you want to reassign.")

            if input("\nDo you want to reopen bug? (y/n): ").lower() != "y":
                print("🎯 Assignment cancelled.")
                return

            now = currtime()
            bug_to_update["history"].append({
                "action": "status changed",
                "by": assigned_by,
                "role": "manager",
                "from": old_status,
                "to": "reopened",
                "timestamp": now
            })
            bug_to_update["status"] = "reopened"
            bug_to_update["updated_at"] = now
            save_bugs(bugs)
            print(f"✅ Bug #{bug_id} status changed to reopened.")

        if input("\nDo you want to reassign? (y/n): ").lower() != "y":
            print("🎯 Assignment cancelled.")
            return

    assignee = is_valid_user_for_role("Assignee", "developer", "resolve", "💻") 
    priority = prompt("⚠️", "Priority (low,medium,high)", 4)
   
    now = currtime()
    history_entry = {
        "action": "assigned" if bug_assigned_already is None else "reassigned",
        "by": assigned_by,
        "role": "manager",
        **({"from": bug_assigned_already} if bug_assigned_already else {}),
        "to": assignee,
        "timestamp": now
    }
    
    bug_to_update["priority"] = priority
    bug_to_update["assigned_to"] = assignee
    bug_to_update["updated_at"] = now
    bug_to_update["history"].append(history_entry)

    save_bugs(bugs)
    print(f"✅ Bug {bug_id} assigned to {assignee} by {assigned_by}. You can check list now (python cli.py list)")


################################################## LIST bug ################################################

def print_bug(bug,scenario_map):
    scenario_title = scenario_map[bug['scenario_id']]['title'] if bug['scenario_id'] else ''

    print(f"""
🐞  Bug #{bug['id']}
📝  Title           :  {bug['title']}
🧾  Description     :  {bug['description']}
🧪  Scenario id     :  {bug['scenario_id']} {scenario_title}
🛠️   Status          :  {bug['status']}
⚠️   Priority        :  {bug['priority']}
🎯  Assigned to     :  {bug['assigned_to']}
✍️   Reported by     :  {bug['reported_by']}
🗓️   Created at      :  {bug['created_at']}
🔄  Updated at      :  {bug['updated_at']}
🏷️   Tags            :  {bug['tags']}
{f"📍  Scenario Status :  {json.dumps(bug['scenario_status'], indent=4)}" if "scenario_status" in bug else ''}
🕒  History         :  {json.dumps(bug['history'], indent=4)}
""" + "-"*150)


def print_open_bugs(bugs):
    open_bugs = [b for b in bugs if b["status"] in {"open", "reopened"}]

    if not open_bugs:
        print("❌ No open or reopened bugs found.")
        return
    
    print("🔍 Listing bugs with status 'open' or 'reopened':\n")
    print(f"{'id':<5} | {'Title':<40} | {'Status'}")
    print("-" * 65)

    for bug in open_bugs:
        print(f"{bug['id']:<5} | {bug['title'][:40]:<40} | {bug['status']}")
     
    print('\n')


def specific_bug(bugs,scenario_map):
    bug = bug_id_validation_prompt(bugs)    
    print_bug(bug,scenario_map)



