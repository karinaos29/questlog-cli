import json

class Inventory:
    def __init__(self, items_dict):
        self.inventory = items_dict

    def __repr__(self):
        output = "Inventory:"
        for item, qty in self.inventory.items():
            output += f"\n- {item}: {qty}"
        return output
    def add_item(self, name, qty):
        if name in self.inventory:
            self.inventory[name] += qty
        else:
            self.inventory[name] = qty
    
    def use_item(self, name, qty):
        current_stock = self.inventory.get(name, 0)
        
        if current_stock < qty:
            raise ValueError(f"Cannot USE {qty} {name}, only {current_stock} available.")
            
        self.inventory[name] -= qty
    
    def has_enough(self, requirements):
        for item, needed_qty in requirements.items():
            if self.inventory.get(item, 0) < needed_qty:
                return False
        return True

    def save_to_file(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.inventory, f, indent=4)
    @classmethod
    def from_dict(cls, data):
        return cls(data)
