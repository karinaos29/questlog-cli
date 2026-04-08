import json

class Quest:
    def __init__(self, name, items):
        self.name = name
        self.requirements = items

    def __repr__(self):
        output = f"Quest: {self.name}\n Required Items:"
        for item, qty in self.requirements.items():
            output += f"\n- {item}: {qty}"
        return output
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['items'])