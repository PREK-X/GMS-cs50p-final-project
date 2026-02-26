# GYM MANAGEMENT SYSTEM

#### Video Demo: https://youtu.be/fpPn1SNyzU0

#### Description:

## Overview

This is a command-line gym management app I built in Python. It lets gym staff do the everyday admin stuff — adding new members, tracking their memberships, handling payments, editing records, and deleting them when needed. Everything gets saved to a CSV file, which keeps things simple without needing a database.

---

## Why I Built It This Way

Honestly, this project is pretty much a direct result of everything I picked up throughout CS50P. Functions, file I/O, CSV handling, working with libraries — it all clicked together here. I wanted to build something that actually felt useful, not just a script that does something random to tick a box.

A gym management system made sense because it touches on a lot of what we covered — reading and writing files, validating user input, doing date calculations, and keeping the code organized with well-defined functions. I intentionally skipped a database or GUI because we didn't cover those in the course, and I wanted to show I could build something practical using just what I'd learned. CSV storage is simple, transparent, and honestly more than enough for a project at this scale.

---

## Project Files

### `project.py`

This is where all the main logic lives. Here's a breakdown of what each function does:

**`main()`** — Starts the program, shows a banner using pyfiglet wrapped inside a rich Panel, and runs the main loop. User picks an option and gets routed to the right function using a match-case statement.

**`main_menu()`** — A separate function that just returns the formatted menu string. Keeping it separate makes main() cleaner and easier to read.

**`new_member()`** — Walks through registering a new member. It validates their age and membership choice, figures out the fee based on the plan and duration, calculates when the membership expires using timedelta, gives them a random ID using secrets, and saves everything to the CSV.

**`show_all_members()`** — Pulls all the records from the CSV and prints them out as a clean table using tabulate.

**`search_member()`** — Lets you look up a specific member by their ID and displays their info in a table.

**`memberships()`** — Shows the available plans, what's included, and what they cost across monthly, 6-month, and yearly durations.

**`payment_status()`** — Shows the payment info and renewal date for a given member.

**`delete_member()`** — Removes a member from the CSV by their ID. Reads all rows into memory, filters out the target, and rewrites the file.

**`edit_member()`** — Lets you update either a member's personal info (name and age) or their membership details. If the membership changes, it recalculates the fee and renewal date automatically, then rewrites the CSV.

---

### `test_project.py`

Has three basic tests:

- `test_new_member()`
- `test_delete_member()`
- `test_edit_member()`

These check that the core functions return the right success messages. Since the functions use `input()`, the tests aren't fully isolated — they're more like behavior checks than pure unit tests.

---

## Libraries Used

**Built-in:**

- `csv` — saving and reading member data
- `datetime` — calculating renewal dates with timedelta
- `secrets` — generating random member IDs
- `os` — checking if the CSV file already exists
- `sys` — exiting the program cleanly

**Third-party:**

- `tabulate` — formats member data into readable tables
- `pyfiglet` — generates the ASCII banner at startup
- `rich` — styled terminal output, used for the Panel and box styling

Install everything with:

```bash
pip install tabulate pyfiglet rich pytest
```

---

## How to Run It

```bash
python project.py
```

You'll see the welcome banner and menu. Navigate by typing the corresponding number.

---

## Running the Tests

```bash
pytest test_project.py -v
```

The tests use `unittest.mock` to simulate user input so pytest can run them without hanging or needing manual input. Each function's `input()` calls are patched using `patch("builtins.input", side_effect=[...])` where the list contains the values in the exact order the function asks for them. This makes the tests fully isolated and reproducible without any user interaction.

For example:

```python
from unittest.mock import patch
from project import new_member, delete_member, edit_member

def test_new_member():
    with patch("builtins.input", side_effect=["John", "25", "monthly", "basic"]):
        assert new_member() == "Member Created Successfully!"

def test_delete_member():
    with patch("builtins.input", side_effect=["some_id"]):
        assert delete_member() == "Member deleted successfully!"

def test_edit_member():
    with patch("builtins.input", side_effect=["1", "some_id", "John", "25"]):
        assert edit_member() == "Changes Made Successfully!"
```

---

## A Few Design Decisions

**CSV over a database** — I went with CSV because it requires zero setup and you can open the file and see exactly what's in it. For a small project like this it makes total sense. If this were a bigger system I'd switch to SQLite.

**Functions over classes** — I kept the structure procedural and straightforward, with each function handling one clear responsibility. A future version could use a Member class and a proper data layer, but for now this approach is easy to follow and matches what was taught in the course.

**Separating main_menu() from main()** — Rather than putting the menu string directly inside main(), I moved it into its own function. It's a small thing but it keeps main() focused on logic and routing rather than presentation.

**Full file rewrite for edits/deletes** — Whenever you edit or delete a record, the whole CSV gets rewritten. It's not the most efficient approach at scale, but it keeps the file consistent and avoids partial updates or corrupt rows.

---

## Known Limitations

- IDs are random and could technically collide (unlikely but possible)
- No login or authentication
- No automatic detection of expired memberships

---

## What I'd Add With More Time

- Swap CSV for a SQLite database
- Add proper unique ID validation
- Build an expiration checker that flags overdue memberships
- Maybe a simple web interface or Tkinter GUI
- Revenue tracking and analytics

---

## Wrapping Up

This project gave me a chance to pull together everything from CS50P into something that feels like a real tool. It covers file handling, business logic, terminal UI, and testing all in one place. It's not perfect, but it works well and there's a clear path to improving it further.
