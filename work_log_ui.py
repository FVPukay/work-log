import datetime
import re
import work_log_csv_handler
from collections import OrderedDict
from os import system, name
from textwrap import dedent

def clear_screen():
    """
    Clears the screen
    """
    system('cls' if name == 'nt' else 'clear')

def get_date():
    """
    Gets a valid date from the user and returns it
    """
    while True:
        print('Date of the task')
        try:
            date_str = input('Please use DD/MM/YYYY: ')
            day, month, year = map(int, date_str.split('/'))
            date = datetime.date(year, month, day)
            date = date.strftime('%d/%m/%Y')
            clear_screen()
            return date
        except ValueError:
            print("Error: {} doesn't seem to be a valid date".format(date_str))
            enter = input('Press enter to try again')
            clear_screen()
            continue

def get_task_name():
    """
    Gets a task_name from the user and returns it
    """
    task_name = input('Title of the task: ')
    clear_screen()
    return task_name

def get_time_spent():
    """
    Gets a valid time spent from the user and returns it
    """
    while True:
        try:
            time_spent = input('Time spent (rounded minutes): ')
            int(time_spent)
            clear_screen()
            return time_spent
        except ValueError:
            error = "Error: {} doesn't seem to be a valid integer"
            print(error.format(time_spent))
            enter = input('Press enter to try again')
            clear_screen()
            continue

def get_optional_notes():
    """
    Gets optional notes from the user and returns it
    """
    optional_notes = input('Notes (Optional, you can leave this empty): ')
    clear_screen()
    return optional_notes

def get_2_dates():
    """
    Gets 2 valid dates from the user, with the first being <= to the second
    date, and returns the 2 dates
    """
    while True:
        print('Enter the dates')
        try:
            date_str = input('First Date: Please use DD/MM/YYYY: ')
            day, month, year = map(int, date_str.split('/'))
            date = datetime.date(year, month, day)

            date_str = input('Second Date: Please use DD/MM/YYYY: ')
            day, month, year = map(int, date_str.split('/'))
            date_2 = datetime.date(year, month, day)

            if date > date_2:
                error = "Error: {} is greather than {}"
                print(error.format(date, date_2))
                enter = input('Press enter to try again')
                clear_screen()
                continue
            return date, date_2
        except ValueError:
            error = "Error: {} doesn't seem to be a valid date"
            print(error.format(date_str))
            enter = input('Press enter to try again')
            clear_screen()
            continue

def get_exact_string():
    """
    Gets and returns an exact text string
    """
    print('Enter exact text string of task_name or optional_notes')
    exact_string = input('Exact String: ')
    return exact_string

def get_regex():
    """
    Gets and returns a regex
    """
    print('Enter regex search pattern')
    while True:
        try:
            regex = input('Regex: ')
            re.compile(regex)
            return regex
        except re.error:
            error = "Error: {} doesn't seem to be a valid regex"
            print(error.format(regex))
            enter = input('Press enter to try again')
            clear_screen()
            continue

def add_entry():
    """
    Adds entry to csv file
    """
    date = get_date()
    task_name = get_task_name()
    time_spent = get_time_spent()
    optional_notes = get_optional_notes()
    work_log_csv_handler.add_to_csv(date, task_name, time_spent, optional_notes)
    entry = input('The entry has been added. Press enter to return to the menu')

def search():
    """
    Allows the user to search by exact date, range of dates, time spent,
    exact search, and by regex pattern
    """
    while True:
        print(dedent("""\
            Do you want to search by:
            a) Exact Date
            b) Range of Dates
            c) Time Spent
            d) Exact Search
            e) Regex Pattern
            f) Return to menu\
        """))

        choice = input('>')

        if choice.lower() == 'a':
            clear_screen()
            date = get_date()
            matches = work_log_csv_handler.exact_date_search(date)
            search_navigator(matches, count=0)
            break
        elif choice.lower() == 'b':
            clear_screen()
            date, date_2 = get_2_dates()
            matches = work_log_csv_handler.date_range_search(date, date_2)
            search_navigator(matches, count=0)
            break
        elif choice.lower() == 'c':
            clear_screen()
            time_spent = get_time_spent()
            matches = work_log_csv_handler.time_spent_search(time_spent)
            search_navigator(matches, count=0)
            break
        elif choice.lower() == 'd':
            clear_screen()
            exact_string = get_exact_string()
            matches = work_log_csv_handler.exact_search(exact_string)
            search_navigator(matches, count=0)
            break
        elif choice.lower() == 'e':
            clear_screen()
            regex = get_regex()
            matches = work_log_csv_handler.pattern_search(regex)
            search_navigator(matches, count=0)
            break
        elif choice.lower() == 'f':
            clear_screen()
            break
        else:
            error = input('Enter a valid choice a-f. Enter to continue')
            clear_screen()
            continue

def search_navigator(list, count):
    """
    Allows the user to navigate through entries found, edit entries,
    delete entries, and to return to the search menu
    """
    clear_screen()

    navigator__template = dedent("""\
        Date: {},
        Title: {},
        Time Spent: {},
        Notes: {},\n
        Result {} of {}\n
    """)

    e_d_r_template = '[E]dit, [D]elete, [R]eturn to search menu'
    n_e_d_r_template = '[N]ext, [E]dit, [D]elete, [R]eturn to search menu'
    p_e_d_r_template = '[P]revious, [E]dit, [D]elete, [R]eturn to search menu'
    n_p_e_d_r_template = dedent("""\
        [N]ext, [P]revious, [E]dit, [D]elete, [R]eturn to search menu\
    """)

    # List is length 0 - there are no matches found or left
    if len(list) == 0:
        no_matches = 'No matches found\nPress enter to continue'
        enter = input(no_matches)
        clear_screen()
        search()
    # List is length 1 - there is 1 match found or left
    elif len(list) == 1:
        is_valid = False
        while is_valid == False:
            print(navigator__template.format(
                list[count]["date"], list[count]["task_name"],
                list[count]["time_spent"], list[count]["optional_notes"],
                count+1, len(list)
                ), e_d_r_template, sep='')

            choice = input('>')

            if choice.lower() == 'e':
                is_valid = True
                clear_screen()
                date = get_date()
                task_name = get_task_name()
                time_spent = get_time_spent()
                optional_notes = get_optional_notes()
                modification = OrderedDict(
                {'date': date, 'task_name': task_name, 'time_spent': time_spent,
                 'optional_notes': optional_notes}
                 )
                original_entry = dict(list[count])
                work_log_csv_handler.edit_entry(original_entry, modification)

                for item in modification:
                    list[count]['{}'.format(item)] = modification['{}'.format(
                        item)]

                search_navigator(list, count)
                clear_screen()
            elif choice.lower() == 'd':
                is_valid = True
                work_log_csv_handler.delete_entry(dict(list[count]))
                del list[count]
                search_navigator(list, count)
                clear_screen()
            elif choice.lower() == 'r':
                is_valid = True
                clear_screen()
                search()
            else:
                error = dedent("""\
                Please enter 'e', 'd' or 'r'
                Press enter to return to main menu""")
                enter = input(error)
                clear_screen()
    # The list has 2 or more entries and this is the first list item
    elif count == 0:
        is_valid = False
        while is_valid == False:
            print(navigator__template.format(
                list[count]["date"], list[count]["task_name"],
                list[count]["time_spent"], list[count]["optional_notes"],
                count+1, len(list)
                ), n_e_d_r_template, sep='')

            choice = input('>')

            if choice.lower() == 'n':
                is_valid = True
                count += 1
                search_navigator(list, count)
            elif choice.lower() == 'e':
                is_valid = True
                clear_screen()
                date = get_date()
                task_name = get_task_name()
                time_spent = get_time_spent()
                optional_notes = get_optional_notes()
                modification = OrderedDict(
                {'date': date, 'task_name': task_name, 'time_spent': time_spent,
                 'optional_notes': optional_notes}
                 )
                original_entry = dict(list[count])
                work_log_csv_handler.edit_entry(original_entry, modification)

                for item in modification:
                    list[count]['{}'.format(item)] = modification['{}'.format(
                        item)]

                search_navigator(list, count)
                clear_screen()
            elif choice.lower() == 'd':
                is_valid = True
                work_log_csv_handler.delete_entry(dict(list[count]))
                del list[count]
                search_navigator(list, count)
                clear_screen()
            elif choice.lower() == 'r':
                is_valid = True
                clear_screen()
                search()
            else:
                error = dedent("""\
                Please enter 'n', 'e', 'd' or 'r'
                Press enter to return to main menu""")
                enter = input(error)
                clear_screen()
    # This is the last item in the list
    elif count+1 == len(list):
        is_valid = False
        while is_valid == False:

            print(navigator__template.format(
                list[count]["date"], list[count]["task_name"],
                list[count]["time_spent"], list[count]["optional_notes"],
                count+1, len(list)
                ), p_e_d_r_template, sep='')

            choice = input('>')

            if choice.lower() == 'p':
                is_valid = True
                count -= 1
                search_navigator(list, count)
            elif choice.lower() == 'e':
                is_valid = True
                clear_screen()
                date = get_date()
                task_name = get_task_name()
                time_spent = get_time_spent()
                optional_notes = get_optional_notes()
                modification = OrderedDict(
                {'date': date, 'task_name': task_name, 'time_spent': time_spent,
                 'optional_notes': optional_notes}
                 )
                original_entry = dict(list[count])
                work_log_csv_handler.edit_entry(original_entry, modification)

                for item in modification:
                    list[count]['{}'.format(item)] = modification['{}'.format(
                        item)]

                search_navigator(list, count)
                clear_screen()
            elif choice.lower() == 'd':
                is_valid = True
                work_log_csv_handler.delete_entry(dict(list[count]))
                del list[count]
                search_navigator(list, count-1)
                clear_screen()
            elif choice.lower() == 'r':
                is_valid = True
                clear_screen()
                search()
            else:
                error = dedent("""\
                Please enter 'p', 'e', 'd' or 'r'
                Press enter to return to main menu""")
                enter = input(error)
                clear_screen()
    # List items between the first and last list items
    else:
        is_valid = False
        while is_valid == False:
            print(navigator__template.format(
                list[count]["date"], list[count]["task_name"],
                list[count]["time_spent"], list[count]["optional_notes"],
                count+1, len(list)
                ), n_p_e_d_r_template, sep='')

            choice = input('>')

            if choice.lower() == 'n':
                is_valid = True
                count += 1
                search_navigator(list, count)
            elif choice.lower() == 'p':
                is_valid = True
                count -= 1
                search_navigator(list, count)
            elif choice.lower() == 'e':
                is_valid = True
                clear_screen()
                date = get_date()
                task_name = get_task_name()
                time_spent = get_time_spent()
                optional_notes = get_optional_notes()
                modification = OrderedDict(
                {'date': date, 'task_name': task_name, 'time_spent': time_spent,
                 'optional_notes': optional_notes}
                 )
                original_entry = dict(list[count])
                work_log_csv_handler.edit_entry(original_entry, modification)

                for item in modification:
                    list[count]['{}'.format(item)] = modification['{}'.format(
                        item)]

                search_navigator(list, count)
                clear_screen()
            elif choice.lower() == 'd':
                is_valid = True
                work_log_csv_handler.delete_entry(dict(list[count]))
                del list[count]
                search_navigator(list, count)
                clear_screen()
            elif choice.lower() == 'r':
                is_valid = True
                clear_screen()
                search()
            else:
                error = dedent("""\
                Please enter 'n', 'p', 'e', 'd' or 'r'
                Press enter to return to main menu""")
                enter = input(error)
                clear_screen()
