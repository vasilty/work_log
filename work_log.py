import csv
import datetime
import os
import re

from collections import OrderedDict
from entry import Entry
from entry import convert_time_spent_to_min


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def init_csv_file():
    """Creates a new csv file with a header."""
    with open('work_log.csv', 'w') as csvfile:
        fieldnames = ['Name', 'Time spent (min)', 'Notes', 'Date']
        filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        filewriter.writeheader()


def print_entry(name, time_spent, notes, date):
    """Prints out an entry."""
    print('Task name: {}'.format(name))
    print('Time spent (min): {}'.format(time_spent))
    print('Notes: {}'.format(notes))
    print('Date: {}'.format(date))
    print('_' * 30)


def save_entry(entry):
    """Saves an entry to a csv file."""
    with open('work_log.csv', 'a') as csvfile:
        fieldnames = ['Name', 'Time spent (min)', 'Notes', 'Date']
        filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        filewriter.writerow({
            'Name': entry.name,
            'Time spent (min)': entry.time_spent,
            'Notes': entry.notes,
            'Date': entry.date
        })


def edit_entry(entry):
    """Edit an entry."""
    while True:
        clear()
        choice = input("[N] Edit the task name\n"
                       "[T] Edit the time spent\n"
                       "[O] Edit the notes\n"
                       "[D] Edit the date\n\n"
                       "[E] Return to the entry\n"
                       "Action: "
                       ).lower().strip()
        if choice in list('ntode'):
            break
    if choice == 'n':
        entry.get_name()
    elif choice == 't':
        entry.get_time_spent()
    elif choice == 'o':
        entry.get_notes()
    elif choice == 'd':
        entry.get_date()


def add_entry():
    """Add an entry."""
    entry = Entry()
    while True:
        clear()
        print_entry(
            name=entry.name,
            time_spent=entry.time_spent,
            notes=entry.notes,
            date=entry.date
        )
        choice = input('[S]ave, [D]elete or [E]dit entry? ').lower().strip()
        if choice == 's':
            save_entry(entry=entry)
            input('Entry saved! Press enter to go to the main menu.')
            break
        elif choice == 'e':
            edit_entry(entry=entry)
        elif choice == 'd':
            input('Entry deleted! Press enter to go to the main menu.')
            break


def show_results(results):
    """Shows entries with the ability to page through records."""
    if len(results) == 0:
        clear()
        input('No entries found. Press enter to return to main menu.')
    else:
        index = 0
        while True:
            options = [
                '[N]ext',
                '[P]revious',
                '[M]ain menu'
            ]
            clear()
            result = results[index]
            print_entry(
                name=result['Name'],
                time_spent=result['Time spent (min)'],
                notes=result['Notes'],
                date=result['Date']
            )
            # Remove the option Previous for the first record.
            if index == 0:
                options.remove('[P]revious')
            # Remove the option Next for the last record.
            if index == len(results) - 1:
                options.remove('[N]ext')
            message = ', '.join(options) + ': '
            navigate = input(message).lower().strip()
            if navigate.upper() in message:
                if navigate == 'p':
                    index -= 1
                elif navigate == 'n':
                    index += 1
                elif navigate == 'm':
                    break


def read_csvfile():
    """Read the csv file."""
    with open('work_log.csv', 'r') as csvfile:
        filereader = csv.DictReader(csvfile)
        rows = list(filereader)
        return rows


def sort_dates(dates):
    """Converts date strings into datetime objects and sorts them."""
    dt_dates = [datetime.datetime.strptime(date, '%d.%m.%Y'
                                           ).date() for date in dates]
    sorted_dates = sorted(dt_dates)
    return sorted_dates


def list_of_dates(rows):
    """Prints a list of sorted unique dates."""
    print('Dates with entries:')
    dates = []
    for row in rows:
        if row['Date'] not in dates:
            dates.append(row['Date'])
    sorted_dates = sort_dates(dates)
    for date in sorted_dates:
        print(date.strftime('%d.%m.%Y'))


def search_by_date(data, message=None):
    """Searches entries by the exact date or date range."""
    clear()
    search_results = []
    if message:
        print(message)
    list_of_dates(rows=data)
    date_input = input('Date (dd.mm.yyyy) or date range '
                       '(dd.mm.yyyy - dd.mm.yyyy):\n')
    dates = re.findall(r'[0-9]{2}.[0-9]{2}.[0-9]{4}', date_input)
    # Checks that 1 date (exact date) or 2 dates (date range) were provided.
    if len(dates) == 1 or len(dates) == 2:
        # Checks that input data is actually date(s).
        for date in dates:
            try:
                datetime.datetime.strptime(date, '%d.%m.%Y').date()
            except ValueError:
                return search_by_date(
                    data=data,
                    message='Wrong date format! {} is not a '
                            'valid date!'.format(date)
                )

        sorted_dates = sort_dates(dates)
        for row in data:
            dt_date = datetime.datetime.strptime(row['Date'], '%d.%m.%Y'
                                                 ).date()
            if (dt_date >= sorted_dates[0] and (
                    dt_date <= sorted_dates[-1])):
                search_results.append(row)
    # If no date or 3 and more dates were provided start over with the error
    # message.
    else:
        return search_by_date(
            data=data,
            message='Wrong format! One date should be '
                    'provided for search by a specific date, two dates - for'
                    ' search by a date range.')
    return search_results


def search_by_string_re(data):
    """Searches entries by string or regular expression provided."""
    search_results = []
    clear()
    string = input('Exact string or regular expression: ')
    match = r'' + string
    for row in data:
        if re.search(match, row['Name']) or re.search(match, row['Notes']):
            search_results.append(row)
    return search_results


def search_by_time_spent(data, message=None):
    """Searches entries by the time spent or time spent range."""
    search_results = []
    clear()
    if message:
        print(message)
    time_input = input('Time spent (in [w]eeks/[d]ays/[h]ours/'
                       '[m]inutes, eg. 1 h) or time range (eg. 1 h - 2 h):\n'
                       ).lower().strip()
    match = r'(?P<value>[0-9]+.?[0-9]*)\s*(?P<format>[wdhm])'
    times = re.findall(match, time_input)
    # If time in particular format was provided.
    if times:
        times_min = map(convert_time_spent_to_min, times)
        # Checks that 1 time (exact time) or 2 times (time range) were provided.
        if len(times) == 1 or len(times) == 2:
            sorted_times_min = sorted(times_min)
            for row in data:
                if float(row['Time spent (min)']) >= sorted_times_min[0] and (
                            float(row['Time spent (min)']
                                  ) <= sorted_times_min[-1]):
                    search_results.append(row)
        # If no time or 3 and more times were provided start over with the error
        # message.
        else:
            return search_by_time_spent(
                data=data,
                message='Invalid format! One time should be provided for'
                        ' search by a specific time spent, two times -'
                        ' for search by a time spent range.'
            )
        return search_results
    # If time in particular format wasn't provided, start over with the
    # appropriate error message.
    else:
        return search_by_time_spent(data=data, message='Invalid time format!')


def lookup_entry():
    """Look up an entry."""
    while True:
        clear()
        choice = input('[D] Search by date\n'
                       '[S] Search by exact string\n'
                       '[R] Search by regular expression\n'
                       '[T] Search by time spent\n\n'
                       '[M] Return to the main menu\n'
                       'Action: '
                       ).lower().strip()
        if choice in list('dsrtm'):
            break
    if choice != 'm':
        rows = read_csvfile()
        if choice == 'd':
            search_results = search_by_date(data=rows)
        elif choice == 's' or choice == 'r':
            search_results = search_by_string_re(data=rows)
        elif choice == 't':
            search_results = search_by_time_spent(data=rows)
        show_results(results=search_results)


def menu_loop():
    """Show the menu."""
    while True:
        clear()
        for key, value in menu.items():
            print('[{}] {}'.format(key, value.__doc__))
        print('[Q] Quit the program.')
        choice = input("Action: ").upper().strip()
        if choice in menu:
            menu[choice]()
        if choice == 'Q':
            break


menu = OrderedDict([
    ('A', add_entry),
    ('L', lookup_entry),
])

if __name__ == '__main__':
    #    init_csv_file()
    menu_loop()
