import json
from .config import BUG_FILE, USER_FILE, SCENARIO_FILE


def load_file(FILE):
   
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        print(f"⚠️   File not found: {FILE}")
        exit(1)


def save_bugs(bugs):
    try:
        with open(BUG_FILE, "w") as f:
            json.dump(bugs, f, indent=4)
    except:
        print(f"⚠️   File not found: {BUG_FILE}")
        exit(1)
