# Worker Scheduling Program

This repository contains a Python script that generates a monthly worker schedule based on specific constraints. The program ensures fair distribution of shifts among workers while adhering to operational requirements.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Advanced Usage](#advanced-usage)
  - [Running the Script](#running-the-script)
  - [Editing `workers.json`](#editing-workersjson)
  - [Using a Previous Schedule](#using-a-previous-schedule)
  - [Adjusting Scheduling Constraints](#adjusting-scheduling-constraints)
- [Constraints and Rules](#constraints-and-rules)
- [Advanced Troubleshooting](#advanced-troubleshooting)
- [FAQ](#faq)
- [How to Get This All Working Without Much Prexisting Knowledge](#how-to-get-this-all-working-without-much-prexisting-knowledge)
- [License](#license)

---

## Features

- Generates a worker schedule based on predefined constraints.
- Ensures each worker gets 40 hours per week (4 shifts).
- Randomizes extra staffing days while avoiding back-to-back days.
- Allows for custom worker names through `workers.json`.
- Accepts a previous schedule to maintain continuity.

## Prerequisites

- **Python 3.7 or higher**: The script is written in Python and requires Python 3.
- **OR-Tools Library**: Google's OR-Tools library is used for constraint programming.

## Installation

### For Non-Python Users

If you're not familiar with Python or don't have it installed, please scroll righ down to:

* [How to Get This All Working Without Much Prexisting Knowledge](#how-to-get-this-all-working-without-much-prexisting-knowledge)

### For Users with Python Knowledge

Ensure you have Python 3 installed, then install OR-Tools:
```
pip install ortools
```
---

## Advanced Usage

### Running the Script

1. **Download the Script**:

   - Clone the repository or download the `scheduler.py` script.

2. **Open Command Prompt or Terminal**:

   Navigate to the directory where `scheduler.py` is located.

3. **Run the Script**:

   - **Basic Usage**:
        ```
        python scheduler.py
        ```
   - **With Custom Worker Names**:
         ```
         python scheduler.py workers.json
         ```
   - **With Previous Schedule and Custom Worker Names**:
        ```
        python scheduler.py previous_schedule.json workers.json
        ```
   **Note**: Replace `workers.json` and `previous_schedule.json` with your filenames if different.

4. **Output**:

   - The schedule will be saved as `schedule.json` in the same directory.
   - The script will print the extra staffing days for the 12pm-10pm shift to the console.

### Editing `workers.json`

The `workers.json` file contains a list of worker names. To customize:

1. **Create or Edit `workers.json`**:

    ```json
    ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Hannah"]
    ```

2. **Ensure**:

   - There are exactly 8 worker names (or adjust the script if you have a different number of workers).
   - Names are enclosed in double quotes and separated by commas.
   - The file is saved with UTF-8 encoding.

### Using a Previous Schedule

To maintain continuity and avoid back-to-back extra staffing days:

1. **Provide the Previous Schedule**:

   - Ensure the previous schedule is saved as a JSON file (e.g., `previous_schedule.json`).

2. **Run the Script with the Previous Schedule**:

    ```python
    python scheduler.py previous_schedule.json workers.json
    ```

### Adjusting Scheduling Constraints

If you need to adjust the staffing minimums, maximums, or other constraints:

1. **Open `scheduler.py` in a Text Editor**.

2. **Locate the Constraints Section**:

    # Staffing requirements for 7am-5pm shift
    ```python
    for d in range(total_days):
    # Adjust the minimum and maximum number of workers as needed
      model.Add(sum(shifts_var[(w, d, '7am-5pm')] for w in range(num_workers)) >= MIN_WORKERS)
      model.Add(sum(shifts_var[(w, d, '7am-5pm')] for w in range(num_workers)) <= MAX_WORKERS)```
    ```
3. **Change `MIN_WORKERS` and `MAX_WORKERS`**:

   - Replace `MIN_WORKERS` and `MAX_WORKERS` with the desired numbers.

   **Example**:
    ```python
    model.Add(sum(shifts_var[(w, d, '7am-5pm')] for w in range(num_workers)) >= 3)
    model.Add(sum(shifts_var[(w, d, '7am-5pm')] for w in range(num_workers)) <= 4)
    ```

4. **Save the File** and rerun the script.

---

## Constraints and Rules

The scheduling program adheres to the following constraints:

1. **Worker Shifts per Week**:

   - Each worker works exactly **4 shifts per week** (totaling 40 hours).

2. **Shifts**:

   - **7am-5pm Shift**: Workers are scheduled between **2 and 5** per day.
   - **12pm-10pm Shift**:
     - **6 days per week**: Exactly **1 worker**.
     - **1 day per week**: Exactly **2 workers** (extra staffing day).

3. **Extra Staffing Day for 12pm-10pm Shift**:

   - The extra staffing day is **randomly selected** each week.
   - It **cannot be the same or adjacent** to the previous week's extra staffing day.
   - When a previous schedule is provided, the first week's extra staffing day is **not adjacent** to the last extra staffing day from the previous schedule.

4. **Days Off Patterns**:

   Each worker follows a four-week cycle:

   - **Week 1**: Saturday off.
   - **Week 2**: Sunday off.
   - **Week 3**: Work both weekend days.
   - **Week 4**: Friday through Sunday off (three-day weekend).

5. **No Consecutive Late to Early Shifts**:

   - A worker scheduled for a **12pm-10pm** shift cannot be scheduled for a **7am-5pm** shift the following day.

6. **No Double Shifts**:

   - No worker is scheduled for **both shifts on the same day**.

7. **Fair Distribution**:

   - The script aims to distribute shifts fairly among all workers while meeting the constraints.

---

## Advanced Troubleshooting

- **No Feasible Solution Found**:

  - If the script outputs "No feasible solution found," consider:

    - Adjusting the minimum and maximum staffing levels for the 7am-5pm shift.
    - Reviewing the days off patterns for potential conflicts.
    - Ensuring that the number of workers and shifts align with the constraints.

- **Invalid Worker Names**:

  - Ensure that `workers.json` contains valid JSON.
  - All names should be strings enclosed in double quotes.

- **Python or OR-Tools Not Installed**:

  - Verify Python installation by running `python --version`.
  - Reinstall OR-Tools using `pip install ortools`.

- Additionally, check if your issue is addressed down under [Basic Troubleshooting](#basic-troubleshooting)
---

## FAQ

### 1. **Can I use more or fewer than 8 workers?**

Yes, but you will need to adjust the script accordingly:

- Change the number of workers in the `workers.json` file.
- Adjust constraints (e.g., shifts per worker) to maintain feasibility.

### 2. **How do I change the number of weeks scheduled?**

Modify the `weeks` variable in the script:
    ```python
    weeks = NUMBER_OF_WEEKS
    ```

### 3. **Can I change the shift times?**

Yes, but you'll need to update the `shifts` list and adjust any constraints that reference specific shift names.

### 4. **What if I don't have a previous schedule?**

You can run the script without a previous schedule. The extra staffing days will be randomized without considering past schedules.


---
...
> "Okay, but what if I don't even use python? This is all confusing, help."

Here we go:
## How to Get This All Working Without Much Prexisting Knowledge

### 1- Install Python 3

**Step 1:** Open your web browser (e.g., Chrome, Firefox, Edge).

**Step 2:** Go to the official Python website: https://www.python.org/downloads/

**Step 3:** Download the latest version of Python 3 for your operating system:

- **Windows Users:**
  - Click on "Download Python 3.x.x" button.
- **macOS Users:**
  - Scroll down to "Latest Python 3 Release" and click on "Download Python 3.x.x".
- **Linux Users:**
  - Use your software manager or package manager to install Python 3.

**Step 4:** Run the installer:

- **Windows Users:**
  - Double-click the downloaded file (e.g., `python-3.x.x.exe`).
  - In the installer, **check the box that says "Add Python 3.x to PATH"** at the bottom.
  - Click "Install Now" and follow the prompts.
- **macOS Users:**
  - Open the downloaded package file (`.pkg`) and follow the installation instructions.
- **Linux Users:**
  - Python 3 may already be installed. If not, open the Terminal and install it using your package manager.

---

### 2- Install the Worker Scheduling Program

**Step 1:** Download the program files:

- Click on the link provided to download the `scheduler.py` script and any other necessary files.
- Alternatively, if the files are provided as a ZIP archive, download and extract them to a folder on your computer (e.g., `C:\WorkerScheduler` or `Documents/WorkerScheduler`).

**Step 2:** Install the required library (OR-Tools):

- **Windows Users:**

  - Open the **Command Prompt**:
    - Press the **Windows key** on your keyboard.
    - Type **"Command Prompt"**.
    - Click on the **Command Prompt** application to open it.

  - In the Command Prompt window, type:

    ```
    pip install ortools
    ```

  - Press **Enter** and wait for the installation to complete.

- **macOS Users:**

  - Open the **Terminal** application:
    - Go to **Applications** > **Utilities** > **Terminal**.

  - In the Terminal window, type:

    ```
    pip3 install ortools
    ```

  - Press **Enter** and wait for the installation to complete.

- **Note:** If you receive a message saying that `pip` is not recognized, you may need to install `pip` or use the full path to Python.

---

### 3- Run the Program

**Step 1:** Open the Command Prompt or Terminal:

- **Windows Users:**
  - Press the **Windows key**.
  - Type **"Command Prompt"**.
  - Click on the **Command Prompt** application.

- **macOS Users:**
  - Open **Terminal** from **Applications** > **Utilities**.

**Step 2:** Navigate to the directory where you saved the program files:

- In the Command Prompt or Terminal, type:

  - **Windows Users:**

    ```
    cd path\to\your\folder
    ```

    Replace `path\to\your\folder` with the actual path (e.g., `C:\WorkerScheduler`).

  - **macOS Users:**

    ```
    cd /path/to/your/folder
    ```

    Replace `/path/to/your/folder` with the actual path (e.g., `Documents/WorkerScheduler`).

**Step 3:** Run the script:

- **Windows Users:**

   ```python scheduler.py```

- **macOS Users:**

   ```python3 scheduler.py```


- Press **Enter** and wait for the program to run.

**Step 4:** Wait for the program to complete:

- The program will generate a schedule and save it as `schedule.json` and `schedule.csv` in the same folder.
- The Command Prompt or Terminal will display messages indicating the progress.

---

### 4- View the Schedule

**Step 1:** Locate the `schedule.csv` file in the program folder.

**Step 2:** Open the `schedule.csv` file:

- Double-click the file to open it in your default spreadsheet application (e.g., Microsoft Excel, Google Sheets, or LibreOffice Calc).

**Step 3:** Review the schedule:

- The schedule will display dates, shift times, and the workers assigned to each shift.

---

### Optional: Customize Worker Names

If you want to use custom worker names:

**Step 1:** Create a `workers.json` file:

- Open a text editor (e.g., Notepad on Windows or TextEdit on macOS).
- Enter the worker names in the following format: ```["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Hannah"]```

Ensure that the names are enclosed in double quotes and separated by commas.

- Save the file as `workers.json` in the program folder.

**Step 2:** Run the script with the custom worker names:

- In the Command Prompt or Terminal, run:

- **Windows Users:**

  ```
  python scheduler.py workers.json
  ```

- **macOS Users:**

  ```
  python3 scheduler.py workers.json
  ```

---

### Optional: Use a Previous Schedule

To maintain continuity and avoid back-to-back extra staffing days:

**Step 1:** Ensure you have the previous `schedule.json` file.

**Step 2:** Run the script with the previous schedule:

- In the Command Prompt or Terminal, run:

- **Windows Users:**

  ```
  python scheduler.py schedule.json workers.json
  ```

- **macOS Users:**

  ```
  python3 scheduler.py schedule.json workers.json
  ```

- Replace `schedule.json` and `workers.json` with your actual filenames if different.

---

### Basic Troubleshooting

- **"pip is not recognized" Error:**

  - Ensure that Python was added to your system PATH during installation.
  - Close and reopen the Command Prompt or Terminal.
  - Alternatively, run the installation using:

    ```
    python -m pip install ortools
    ```

- **"No module named ortools" Error:**

  - Ensure that you have installed the OR-Tools library.
  - Run `pip install ortools` (Windows) or `pip3 install ortools` (macOS).

- **Permission Errors:**
  - Run the Command Prompt or Terminal as an administrator.
  - Right-click on the Command Prompt icon and select "Run as administrator".
 
- **Schedule Not Generated:**

  - Ensure that you are in the correct directory where `scheduler.py` is located.
  - Verify that all required files are present.



---

## License

This project is licensed under the MIT License. Feel free to use and modify the code as needed.

---

**Note**: This scheduling tool is designed to help create fair and efficient work schedules. Always review the generated schedules to ensure they meet your organization's specific needs and comply with labor regulations etc, idk, lol.

---
