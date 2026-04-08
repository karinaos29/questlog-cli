import sys
import json
from .quest import Quest
from .inventory import Inventory

class Manager:
    def __init__(self, config_path):
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_path}' not found.")
            sys.exit(1)

        self.quests = self.load_quests()
        self.inventory = self.load_inventory()

    def load_quests(self):
        path = self.config.get("quest_file")
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                return [Quest.from_dict(q) for q in data]
        except FileNotFoundError:
            print(f"Error: Quest file '{path}' not found.")
            return []

    def load_inventory(self):
        path = self.config.get("inventory_file")
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                return Inventory.from_dict(data)
        except FileNotFoundError:
            print(f"Error: Inventory file '{path}' not found.")
            return Inventory({})

    def list_quests(self):
        print("Available Quests:")
        for i, quest in enumerate(self.quests, 1):
            print(f"{i}. {quest.name}")

    def view_quest(self, quest_name):
        quest = self.find_quest(quest_name)
        if quest:
            print(quest)
        else:
            print(f"Error: Quest '{quest_name}' not found.")

    def gap_analysis(self, quest_name):
        quest = self.find_quest(quest_name)
        if not quest:
            print(f"Error: Quest '{quest_name}' not found.")
            return

        print(f"Missing items for '{quest.name}':")
        missing_found = False
        for item, needed in quest.requirements.items():
            current = self.inventory.inventory.get(item, 0)
            if current < needed:
                print(f"{item}: {needed - current} more needed")
                missing_found = True
        
        if not missing_found:
            print("No items missing!")

    def complete_quest(self, quest_name):
        quest = self.find_quest(quest_name)
        if not quest:
            print(f"Error: Quest '{quest_name}' not found.")
            return

        if self.inventory.has_enough(quest.requirements):
            for item, qty in quest.requirements.items():
                self.inventory.use_item(item, qty)
            
            self.inventory.save_to_file(self.config["inventory_file"])
            print(f"Successfully completed '{quest.name}'. Inventory updated.")
        else:
            print(f"Error: Insufficient items to complete '{quest.name}'.")

    def plan_quests(self):
        print("Completable Quests:")
        completable = [q.name for q in self.quests if self.inventory.has_enough(q.requirements)]
        
        if not completable:
            print("None")
        for name in completable:
            print(f"{name}")

    def add_item(self, item, qty):
        self.inventory.add_item(item, int(qty))
        self.inventory.save_to_file(self.config["inventory_file"])
        print(f"Added {qty} {item}.")

    def use_item(self, item, qty):
        try:
            self.inventory.use_item(item, int(qty))
            self.inventory.save_to_file(self.config["inventory_file"])
            print(f"Used {qty} {item}.")
        except ValueError as e:
            print(f"Error: {e}")


    def find_quest(self, name):
        for q in self.quests:
            if q.name.lower() == name.lower():
                return q
        return None
    
    def process_batch(self, batch_path="batch_commands.txt"):
        report_path = self.config.get("report_file", "reports/report.txt")
        
        try:
            with open(batch_path, 'r') as b_file, open(report_path, 'w') as r_file:
                for line in b_file:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split()
                    if not parts: continue
                    
                    action = parts[0].upper()
                    
                    try:
                        if action == "ADD" and len(parts) == 3:
                            self.add_item(parts[1], parts[2])
                            r_file.write(f"SUCCESS: ADD {parts[1]} {parts[2]}\n")
                            
                        elif action == "USE" and len(parts) == 3:
                            self.inventory.use_item(parts[1], int(parts[2]))
                            self.inventory.save_to_file(self.config["inventory_file"])
                            r_file.write(f"SUCCESS: USE {parts[1]} {parts[2]}\n")
                            
                        else:
                            r_file.write(f"ERROR: Unknown command '{action}'.\n")
                            
                    except ValueError as e:
                        r_file.write(f"ERROR: {str(e)}\n")

            print(f"Batch processing complete. See '{report_path}' for details.")

        except FileNotFoundError:
            print(f"Error: The batch file '{batch_path}' was not found.")