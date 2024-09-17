Worker Scheduling Program

This repository contains a Python script that generates a monthly worker schedule based on specific constraints. The program ensures fair distribution of shifts among workers while adhering to operational requirements.
Table of Contents

    Features
    Prerequisites
    Installation
    Usage
        Running the Script
        Editing workers.json
        Using a Previous Schedule
        Adjusting Scheduling Constraints
    Constraints and Rules
    Troubleshooting
    FAQ
    License

Features

    Generates a worker schedule based on predefined constraints.
    Ensures each worker gets 40 hours per week (4 shifts).
    Randomizes extra staffing days while avoiding back-to-back days.
    Allows for custom worker names through workers.json.
    Accepts a previous schedule to maintain continuity.

Prerequisites

    Python 3.7 or higher: The script is written in Python and requires Python 3.
    OR-Tools Library: Google's OR-Tools library is used for constraint programming.

Installation
For Non-Python Users

If you're not familiar with Python or don't have it installed, follow these steps:

    Install Python 3:
        Windows: Download and install from the official website.
        macOS: Download and install from the official website.
        Linux: Use your distribution's package manager (e.g., sudo apt-get install python3).

    Note: During installation on Windows, make sure to check the box that says "Add Python to PATH".

    Install OR-Tools:

    Open the Command Prompt (Windows) or Terminal (macOS/Linux) and run:

    bash

    pip install ortools

    If pip is not recognized, you may need to use python -m pip install ortools.

For Users with Python Knowledge

Ensure you have Python 3 installed, then install OR-Tools:

bash

pip install ortools

Usage
Running the Script

    Download the Script:
        Clone the repository or download the scheduler.py script.

    Open Command Prompt or Terminal:

    Navigate to the directory where scheduler.py is located.

    Run the Script:

        Basic Usage:

        bash

python scheduler.py

With Custom Worker Names:

bash

python scheduler.py workers.json

With Previous Schedule and Custom Worker Names:

bash

        python scheduler.py previous_schedule.json workers.json

    Note: Replace workers.json and previous_schedule.json with the actual filenames if different.

    Output:
        The schedule will be saved as schedule.json in the same directory.
        The script will print the extra staffing days for the 12pm-10pm shift to the console.

Editing workers.json

The workers.json file contains a list of worker names. To customize:

    Create or Edit workers.json:

    json

    ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Hannah"]

    Ensure:
        There are exactly 8 worker names (or adjust the script accordingly if you have a different number of workers).
        The names are enclosed in double quotes and separated by commas.
        The file is saved with UTF-8 encoding.

Using a Previous Schedule

To maintain continuity and avoid back-to-back extra staffing days:

    Provide the Previous Schedule:
        Ensure the previous schedule is saved as a JSON file (e.g., previous_schedule.json).

    Run the Script with the Previous Schedule:

    bash

    python scheduler.py previous_schedule.json workers.json

Adjusting Scheduling Constraints

If you need to adjust the staffing minimums, maximums, or other constraints:

    Open scheduler.py in a Text Editor.

    Locate the Constraints Section:

    python

# Staffing requirements for 7am-5pm shift
for d in range(total_days):
    # Adjust the minimum and maximum number of workers as needed
    model.Add(sum(shifts_var[(w, d, '7am-5pm')] for w in range(num_workers)) >= MIN_WORKERS)
    model.Add(sum(shifts_var[(w, d, '7am-5pm')] for w in range(num_workers)) <= MAX_WORKERS)

Change MIN_WORKERS and MAX_WORKERS:

    Replace MIN_WORKERS and MAX_WORKERS with the desired numbers.

Example:

python

    model.Add(sum(shifts_var[(w, d, '7am-5pm')] for w in range(num_workers)) >= 3)
    model.Add(sum(shifts_var[(w, d, '7am-5pm')] for w in range(num_workers)) <= 4)

    Save the File and rerun the script.

Constraints and Rules

The scheduling program adheres to the following constraints:

    Worker Shifts per Week:
        Each worker works exactly 4 shifts per week (totaling 40 hours).

    Shifts:
        7am-5pm Shift: Workers are scheduled between 2 and 5 per day.
        12pm-10pm Shift:
            6 days per week: Exactly 1 worker.
            1 day per week: Exactly 2 workers (extra staffing day).

    Extra Staffing Day for 12pm-10pm Shift:
        The extra staffing day is randomly selected each week.
        It cannot be the same or adjacent to the previous week's extra staffing day.
        When a previous schedule is provided, the first week's extra staffing day is not adjacent to the last extra staffing day from the previous schedule.

    Days Off Patterns:

    Each worker follows a four-week cycle:
        Week 1: Saturday off.
        Week 2: Sunday off.
        Week 3: Work both weekend days.
        Week 4: Friday through Sunday off (three-day weekend).

    No Consecutive Late to Early Shifts:
        A worker scheduled for a 12pm-10pm shift cannot be scheduled for a 7am-5pm shift the following day.

    No Double Shifts:
        No worker is scheduled for both shifts on the same day.

    Fair Distribution:
        The script aims to distribute shifts fairly among all workers while meeting the constraints.

Troubleshooting

    No Feasible Solution Found:

        If the script outputs "No feasible solution found," consider:
            Adjusting the minimum and maximum staffing levels for the 7am-5pm shift.
            Reviewing the days off patterns for potential conflicts.
            Ensuring that the number of workers and shifts align with the constraints.

    Invalid Worker Names:
        Ensure that workers.json contains valid JSON.
        All names should be strings enclosed in double quotes.

    Python or OR-Tools Not Installed:
        Verify Python installation by running python --version.
        Reinstall OR-Tools using pip install ortools.

FAQ
1. Can I use more or fewer than 8 workers?

Yes, but you will need to adjust the script accordingly:

    Change the number of workers in the workers.json file.
    Ensure that the constraints (e.g., shifts per worker) are adjusted to maintain feasibility.

2. How do I change the number of weeks scheduled?

Modify the weeks variable in the script:

python

weeks = NUMBER_OF_WEEKS

3. Can I change the shift times?

Yes, but you'll need to update the shifts list and adjust any constraints that reference specific shift names.
4. What if I don't have a previous schedule?

You can run the script without a previous schedule. The extra staffing days will be randomized without considering past schedules.
License

This project is licensed under the MIT License. Feel free to use and modify the code as needed.

Note: This scheduling tool is designed to help create fair and efficient work schedules. Always review the generated schedules to ensure they meet your organization's specific needs and comply with labor regulations.