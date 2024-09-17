import json
from ortools.sat.python import cp_model
import datetime
import sys
import random

def main():
    previous_schedule = None
    worker_names = [f'Worker{i}' for i in range(1, 9)]  # Default worker names
    args = sys.argv[1:]
    for arg in args:
        if arg.endswith('workers.json'):
            with open(arg, 'r') as f:
                worker_names = json.load(f)
        elif arg.endswith('.json'):
            with open(arg, 'r') as f:
                previous_schedule = json.load(f)

    num_workers = len(worker_names)
    weeks = 4
    days_in_week = 7
    total_days = weeks * days_in_week
    shifts = ['7am-5pm', '12pm-10pm']
    days_of_week = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    # Corrected Patterns for days off
    patterns = [
        {'week': 0, 'days_off': [0], 'desc': 'Saturday off'},
        {'week': 1, 'days_off': [1], 'desc': 'Sunday off'},
        {'week': 2, 'days_off': [], 'desc': 'Work both weekend days'},
        {'week': 3, 'days_off': [6, 0, 1], 'desc': 'Friday-Sunday off'},
    ]
    
    model = cp_model.CpModel()
    shifts_var = {}
    for w in range(num_workers):
        for d in range(total_days):
            for s in shifts:
                shifts_var[(w, d, s)] = model.NewBoolVar(f'shift_n{w}_d{d}_s{s}')

    ###### Constraints ########

    # Each worker works exactly 4 shifts per week
    for w in range(num_workers):
        for week in range(weeks):
            total_shifts = sum(shifts_var[(w, week * days_in_week + d, s)]
                               for d in range(days_in_week)
                               for s in shifts)
            model.Add(total_shifts == 4)

    # Days off constraints per pattern
    for w in range(num_workers):
        pattern = patterns[w % len(patterns)]
        for week in range(weeks):
            week_pattern = patterns[(pattern['week'] + week) % len(patterns)]
            days_off = week_pattern['days_off']
            for day_off in days_off:
                day = week * days_in_week + day_off
                for s in shifts:
                    model.Add(shifts_var[(w, day, s)] == 0)

    # No worker should be scheduled a 7am-5pm shift after a 12pm-10pm shift
    for w in range(num_workers):
        for d in range(total_days - 1):
            model.Add(shifts_var[(w, d + 1, '7am-5pm')] + shifts_var[(w, d, '12pm-10pm')] <= 1)

    # Staffing requirements
    extra_shift_days = []
    previous_extra_shift_day = None

    # If previous schedule is provided, extract the last extra staffing day
    if previous_schedule:
        last_week = max(map(int, previous_schedule.keys()))
        last_week_schedule = previous_schedule[str(last_week)]
        for day, info in last_week_schedule.items():
            day_info = info['shifts']
            num_workers_12pm = len(day_info.get('12pm-10pm', []))
            if num_workers_12pm == 2:
                previous_extra_shift_day = int(day)
                break  # Assuming only one extra staffing day per week

    for week in range(weeks):
        # Select a random day for extra staffing
        available_days = list(range(days_in_week))
        if week == 0 and previous_extra_shift_day is not None:
            # Exclude days adjacent to the previous schedule's last extra staffing day
            prev_day = previous_extra_shift_day
            unavailable_days = {prev_day, (prev_day - 1) % days_in_week, (prev_day + 1) % days_in_week}
            available_days = [d for d in available_days if d not in unavailable_days]
        elif week > 0:
            # Exclude days adjacent to the previous week's extra shift day
            prev_day = extra_shift_days[week - 1]
            unavailable_days = {prev_day, (prev_day - 1) % days_in_week, (prev_day + 1) % days_in_week}
            available_days = [d for d in available_days if d not in unavailable_days]
        extra_shift_day = random.choice(available_days)
        extra_shift_days.append(extra_shift_day)
        for d in range(week * days_in_week, (week + 1) * days_in_week):
            day_in_week = d % days_in_week
            # 12pm-10pm shift staffing
            if day_in_week == extra_shift_day:
                # One day a week has two workers on 12pm-10pm shift
                model.Add(sum(shifts_var[(w, d, '12pm-10pm')] for w in range(num_workers)) == 2)
            else:
                model.Add(sum(shifts_var[(w, d, '12pm-10pm')] for w in range(num_workers)) == 1)

    # Staffing requirements for 7am-5pm shift
    for d in range(total_days):
        # 7am-5pm shift staffing: Between 2 and 5 workers
        model.Add(sum(shifts_var[(w, d, '7am-5pm')] for w in range(num_workers)) >= 2)
        model.Add(sum(shifts_var[(w, d, '7am-5pm')] for w in range(num_workers)) <= 5)

    # No worker can work both shifts on the same day
    for w in range(num_workers):
        for d in range(total_days):
            model.Add(sum(shifts_var[(w, d, s)] for s in shifts) <= 1)

    # Solve the model
    solver = cp_model.CpSolver()
    # Optional: To get different solutions on different runs
    solver.parameters.random_seed = random.randint(1, 10000)
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        schedule = {}
        # Initialize validation data structures
        worker_hours = {w: [0]*weeks for w in range(num_workers)}
        worker_days_off = {w: [[] for _ in range(weeks)] for w in range(num_workers)}
        for week in range(weeks):
            schedule[week] = {}
            for day in range(days_in_week):
                d = week * days_in_week + day
                date = (datetime.datetime.now() + datetime.timedelta(days=d)).strftime('%Y-%m-%d')
                schedule[week][day] = {'date': date, 'shifts': {'7am-5pm': [], '12pm-10pm': []}}
                for w in range(num_workers):
                    shift_assigned = False
                    for s in shifts:
                        if solver.Value(shifts_var[(w, d, s)]):
                            schedule[week][day]['shifts'][s].append(worker_names[w])
                            shift_assigned = True
                            worker_hours[w][week] += 10  # Each shift is 10 hours
                    if not shift_assigned:
                        worker_days_off[w][week].append(day % days_in_week)
        # Output the schedule to JSON
        with open('schedule.json', 'w') as f:
            json.dump(schedule, f, indent=4)
        print("Schedule generated and saved to 'schedule.json'.")
        print("\nExtra staffing days for 12pm-10pm shift are on:")
        for week, day in enumerate(extra_shift_days):
            print(f"Week {week + 1}: {days_of_week[day]} (Day {day})")
        
        # Validation Output
        print("\nValidation Report:")
        for w in range(num_workers):
            print(f"\nWorker: {worker_names[w]}")
            pattern = patterns[w % len(patterns)]
            pattern_desc = pattern['desc']
            print(f"  Days Off Pattern: {pattern_desc}")
            for week in range(weeks):
                print(f"  Week {week + 1}:")
                print(f"    Total Hours Worked: {worker_hours[w][week]} hours")
                # Check if total hours are 40
                if worker_hours[w][week] != 40:
                    print("    ERROR: Total hours not equal to 40!")
                else:
                    print("    Total hours are correct.")
                # Verify days off
                expected_days_off = patterns[(pattern['week'] + week) % len(patterns)]['days_off']
                actual_days_off = worker_days_off[w][week]
                # Convert day indices to day names
                expected_days_off_names = [days_of_week[d] for d in expected_days_off]
                actual_days_off_names = [days_of_week[d] for d in actual_days_off]
                print(f"    Expected Days Off: {', '.join(expected_days_off_names) if expected_days_off_names else 'None'}")
                print(f"    Actual Days Off: {', '.join(actual_days_off_names) if actual_days_off_names else 'None'}")
                # Check if expected days off match actual days off
                if set(expected_days_off).issubset(set(actual_days_off)):
                    print("    Days off are correct.")
                else:
                    print("    ERROR: Days off do not match the expected pattern!")
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()
