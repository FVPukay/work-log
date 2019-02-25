import csv
import datetime
import os.path
import re

csv_name = 'database.csv'
fieldnames = ['date', 'task_name', 'time_spent', 'optional_notes']
csv_exists = os.path.isfile(csv_name)

# Creates the csv and writes headers to the file if the csv does not exist yet
with open(csv_name, 'a') as csvfile:
    logwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if not csv_exists:
        logwriter.writeheader()

def readcsv_edit_delete():
    """
    Reads the csv, returns rows, and an empty amended entries list so that
    entries in the csv can be edited or deleted

    This is used with the delete_entry and edit_entry functions
    """
    with open(csv_name, 'r') as source_file:
        amended_entries = []
        logreader = csv.DictReader(source_file, delimiter=",")
        rows = list(logreader)
        return rows, amended_entries

def overwrite_csv(amended_entries):
    """
    Overwrites the data in the csv with the new data

    This is used with the delete_entry and edit_entry functions
    """
    with open(csv_name, 'w') as csvfile:
        logwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        logwriter.writeheader()
        logwriter.writerows(amended_entries)

def readcsv_search():
    """
    Reads the csv, returns rows, and an empty matches list

    This is used with the exact_date_search, date_range_search,
    time_spent_search, exact_search, and pattern_search functions
    """
    with open(csv_name, 'r') as csvfile:
        matches = []
        logreader = csv.DictReader(csvfile, delimiter=",")
        rows = list(logreader)
        return rows, matches

def add_to_csv(date, task_name, time_spent, optional_notes):
    """
    Adds the entry to the csv
    """
    with open(csv_name, 'a') as csvfile:
        logwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        logwriter.writerow({
            "date": date,
            "task_name": task_name,
            "time_spent": time_spent,
            "optional_notes": optional_notes
        })

def exact_date_search(date):
    """
    Finds all entries in the csv that have the specified date
    """
    rows, matches = readcsv_search()
    for row in rows:
        if row["date"] == date:
            matches.append(row)
    return matches

def date_range_search(date, date_2):
    """
    Finds all entries in the csv that are within the specififed date range
    """
    rows, matches = readcsv_search()
    for row in rows:
        day, month, year = map(int, row["date"].split('/'))
        datetime_date = datetime.date(year, month, day)
        if datetime_date >= date and datetime_date <= date_2:
            matches.append(row)
    return matches

def time_spent_search(time_spent):
    """
    Finds all entries in the csv with the specified time spent
    """
    rows, matches = readcsv_search()
    for row in rows:
        if row["time_spent"] == time_spent:
            matches.append(row)
    return matches

def exact_search(str):
    """
    Finds all entries in the csv containing the exact string in the task name
    or notes
    """
    rows, matches = readcsv_search()
    for row in rows:
        if str.lower() in row["task_name"].lower():
            matches.append(row)
        elif str.lower() in row["optional_notes"].lower():
            matches.append(row)
    return matches

def pattern_search(regex):
    """
    Finds all entries in the csv matching the regex pattern in the task name or
    notes
    """
    rows, matches = readcsv_search()

    pattern = re.compile('''{}'''.format(regex), re.X|re.M|re.I)

    for row in rows:
        tn_search = re.search(pattern, row["task_name"])
        on_search = re.search(pattern, row["optional_notes"])
        if tn_search:
            matches.append(row)
        elif on_search:
            matches.append(row)
    return matches

def delete_entry(entry):
    """
    Replaces the existing csv with a new version that omits the entry
    being deleted
    """
    rows, amended_entries = readcsv_edit_delete()
    for row in rows:
        if row != entry:
            amended_entries.append(row)

    overwrite_csv(amended_entries)

def edit_entry(original_entry, modification):
    """
    Replaces the existing csv with a new version that modifies the entry
    that is being edited
    """
    rows, amended_entries = readcsv_edit_delete()
    for row in rows:
        if row != original_entry:
            amended_entries.append(row)
        else:
            amended_entries.append(modification)

    overwrite_csv(amended_entries)
