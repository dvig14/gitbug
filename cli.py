import argparse
from gitbugsim.bug_simulator.bug_cli import add_bug_cli, assign_bug_cli, list_bugs_cli
from gitbugsim.git_simulation.git_simulator import simulate_git_for_bug
from gitbugsim.utils.display import display
import sys

if not display.rich_available:
    print("\n⚠️  Optional: For enhanced visuals, run:")
    print("    pip install rich\n")
    
    choice = input("❓ Want to install and restart? (y/n): ").strip().lower()
    if choice == 'y':
        print("ℹ️  Please run:\n    pip install rich\nThen restart the tool.\n")
        sys.exit(1)

parser = argparse.ArgumentParser(description="Bug Tracker CLI")
subparsers = parser.add_subparsers(dest="command")

# Add bug
add_parser = subparsers.add_parser("add", help="Report a new bug")
add_parser.set_defaults(func=add_bug_cli)

# List bug
list_parser = subparsers.add_parser("list", help="List all reported bugs")
list_parser.set_defaults(func=list_bugs_cli)

# Assign bug
assign_parser = subparsers.add_parser("assign", help="Assign a bug")
assign_parser.set_defaults(func=assign_bug_cli)

#Git simulation 
simulate_parser = subparsers.add_parser("simulate", help="Start Git simulation for a bug")
simulate_parser.set_defaults(func=simulate_git_for_bug)

args = parser.parse_args()

if args.command is None:
    parser.print_help()
else:
    args.func()

