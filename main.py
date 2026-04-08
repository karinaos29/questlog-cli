import os
import argparse
import json
import sys
import shlex


from questlog.quest import Quest
from questlog.inventory import Inventory
from questlog.manager import Manager

QUEST_COMMANDS = ("list", "view", "gap", "complete")
INVENTORY_COMMANDS = ("add", "use", "process")

def plan(manager):
    manager.plan_quests()
   
def manage(manager):
    while True:
        user_input = input("> ").strip()
        
        if not user_input:
                continue

        parts = shlex.split(user_input)
        cmd_type = parts[0].lower()

        if cmd_type == "quest":
            if len(parts) < 2:
                print("Error: Missing sub-command. Try 'list', 'view', 'gap', or 'complete'.")
                continue
            sub_cmd = parts[1].lower()
            match sub_cmd:
                case "list":
                    manager.list_quests()
                case "view":
                    if len(parts) != 3:
                        print("Error: 'quest view' requires a quest name.")
                    else:
                        manager.view_quest(parts[2])
                case "gap":
                    if len(parts) != 3:
                        print("Error: 'quest gap' requires a quest name.")
                    else:
                        manager.gap_analysis(parts[2])
                case "complete":
                    if len(parts) != 3:
                        print("Error: 'quest complete' requires a quest name.")
                    else:
                        manager.complete_quest(parts[2])
                case _:
                    print(f"Error: Unknown quest command '{sub_cmd}'")

        elif cmd_type == "inventory":
            if len(parts) < 2:
                print("Error: Missing sub-command. Try 'add', 'use', or 'process'.")
                continue
            sub_cmd = parts[1].lower()
            match sub_cmd:
                case "add":
                    if len(parts) != 4:
                        print("Error: 'inventory add' requires name and quantity.")
                    else:
                        manager.add_item(parts[2], parts[3])
                case "use":
                    if len(parts) != 4:
                        print("Error: 'inventory use' requires name and quantity.")
                    else:
                        manager.use_item(parts[2], parts[3])
                case "process":
                    if len(parts) != 3:
                        print("Error: 'inventory process' requires a filepath.")
                    else:
                        manager.process_batch(parts[2]) 
                case _:
                    print(f"Error: Unknown inventory command '{sub_cmd}'")

        elif cmd_type == "plan":
            manager.plan_quests()

        elif parts[0] == "exit":
            print("Inventory saved. Goodbye!")
            break
        else:
            print("Error: Unknown command. Valid commands are 'quest', 'inventory', 'plan', 'exit'.")

def main():
    config_path = 'config.json'
    manager = Manager(config_path)

    parser = argparse.ArgumentParser(description="QuestLog CLI")

    subparsers = parser.add_subparsers(dest="command") 

    subparsers.add_parser("plan", help="Runs the plan algorithm")
    subparsers.add_parser("manage", help="Enters interactive mode")

    args = parser.parse_args()

    if args.command == "plan":
        plan(manager)
    elif args.command == "manage":
        manage(manager)

if __name__ == "__main__":
    main()