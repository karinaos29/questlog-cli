# QuestLog CLI

QuestLog is a robust, object-oriented command-line application designed to act as an adventure quest and inventory management assistant.

QuestLog helps you track:
- what you have
- what you need
- what you can achieve

---

### 🚀 Features

#### Dual Execution Modes
- Run quick one-off command via `plan`
- Or use an interactive session via `manage` mode

#### Planning Intelligence
- Automatically determine which quests are completable with current inventory
- Instantly see missing items and required quantities for any quest

#### Batch Processing
- Execute commands from text files
- Generate detailed success/error reports

#### Persistent Storage
- Uses JSON files to preserve inventory state across sessions

#### Robust Error Handling
Handles:
- Missing files
- Invalid inputs
- Logical errors (e.g., insufficient stock)

---

## 🛠️ Installation & Setup

### Clone the Repository

```bash
git clone https://github.com/karinaos29/questlog-cli.git
cd questlog
```
---

## Commands

### 🗺️ Quest Management

- quest list - Prints a numbered list of all available quest names.
- quest view "<quest_name>"	- Displays full details, including required items for a specific quest.
- quest gap "<quest_name>" - Performs a "gap analysis" to identify missing items and shortfall quantities.
- quest complete "<quest_name>"	- Verifies requirements and consumes items from inventory to finish a quest.

### 🎒 Inventory Management

- inventory add "<item_name>" <quantity>	- Adds a specified integer quantity to the inventory.
- inventory use "<item_name>" <quantity>	- Reduces item quantity; fails if stock is insufficient.
- inventory process <filepath>	- Executes sequential commands from a text file and generates a report.
