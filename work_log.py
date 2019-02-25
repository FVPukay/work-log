import work_log_ui
from textwrap import dedent

if __name__ == '__main__':
    while True:
        work_log_ui.clear_screen()
        print(dedent("""\
            WORK LOG
            What would you like to do?
            a) Add new entry
            b) Search in existing entries
            c) Quit program\
        """))

        choice = input('>')

        if choice.lower() == 'a':
            work_log_ui.clear_screen()
            work_log_ui.add_entry()
            work_log_ui.clear_screen()
            continue
        elif choice.lower() == 'b':
            work_log_ui.clear_screen()
            work_log_ui.search()
            continue
        elif choice.lower() == 'c':
            work_log_ui.clear_screen()
            print(dedent("""\
                Thanks for using the Work Log program!
                Come again soon.\
            """))
            break
        else:
            error = "Please enter 'a', 'b', or 'c'\nPress enter to try again"
            enter = input(error)
            continue
