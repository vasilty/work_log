import csv
import datetime
import os
import re

from collections import OrderedDict
from entry import Entry


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def init_csv_file():
    with open('work_log.csv', 'w') as csvfile:
        fieldnames = ['Name', 'Time spent (min)', 'Notes', 'Date']
        filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        filewriter.writeheader()


def print_entry(name, time_spent, notes, date):
    print('Task name: {}'.format(name))
    print('Time spent (min): {}'.format(time_spent))
    print('Notes: {}'.format(notes))
    print('Date: {}'.format(date))


def save_entry(entry):
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
        choice = input("Edit the task [N]ame, [T]ime spent, n[O]tes, [D]ate\n"
                       "or delete the entry and go to the main [M]enu: "
                       ).lower().strip()
        if choice in 'ntodm':
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
            print('_' * 20)
            if index == 0:
                options.remove('[P]revious')
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
    with open('work_log.csv', 'r') as csvfile:
        filereader = csv.DictReader(csvfile)
        rows = list(filereader)
        return rows


def sort_dates(dates):
    dt_dates = [datetime.datetime.strptime(date, '%d.%m.%Y'
                                           ).date() for date in dates]
    sorted_dates = sorted(dt_dates)
    return sorted_dates


def list_of_dates(rows):
    """Prints a list of sorted dates."""
    print('Dates with entries:')
    dates = []
    for row in rows:
        if row['Date'] not in dates:
            dates.append(row['Date'])
    sorted_dates = sort_dates(dates)
    for date in sorted_dates:
        print(date.strftime('%d.%m.%Y'))


def search_by_date(message=None):
    clear()
    rows = read_csvfile()
    search_results = []
    if message:
        print(message)
    list_of_dates(rows=rows)
    date_input = input('Date (dd.mm.yyyy) or date range '
                       '(dd.mm.yyyy - dd.mm.yyyy): ')
    date_range = re.findall(r'[0-9]{2}.[0-9]{2}.[0-9]{4}', date_input)
    if date_range:
        # Check that input data is actually date(s).
        for date in date_range:
            try:
                datetime.datetime.strptime(date, '%d.%m.%Y').date()
            except ValueError:
                return search_by_date(message='Wrong date format!')
        # Search by date.
        if len(date_range) == 1:
            for row in rows:
                if row['Date'] == date_range[0]:
                    search_results.append(row)
        # Search by date range.
        elif len(date_range) == 2:
            sorted_date_range = sort_dates(date_range)
            tdelta = sorted_date_range[-1] - sorted_date_range[0]
            for row in rows:
                dt_date = datetime.datetime.strptime(row['Date'], '%d.%m.%Y'
                                                     ).date()
                if (sorted_date_range[-1] - dt_date).days >= 0 and (
                        (sorted_date_range[-1] - dt_date).days) <= tdelta.days:
                    search_results.append(row)
        else:
            return search_by_date(message='Wrong date format!')
        return search_results
    else:
        return search_by_date(message='Wrong date format!')


def search_by_string_re():
    search_results = []
    clear()
    rows = read_csvfile()
    string = input('Exact string or regular expression: ')
    match = r'' + string
    for row in rows:
        if re.search(match, row['Name']) or re.search(match, row['Notes']):
            search_results.append(row)
    return search_results


def convert_time_spent_to_min(times):
    """Converts time from w/d/h/m to minutes."""
    times_min = []
    for time in times:
        time_value = float(time[0])
        time_format = time[1]
        if time_format == 'w':
            time_spent = time_value * 7 * 24 * 60
        elif time_format == 'd':
            time_spent = time_value * 24 * 60
        elif time_format == 'h':
            time_spent = time_value * 60
        else:
            time_spent = time_value
        times_min.append(time_spent)
    return times_min


def search_by_time_spent(message=None):
    search_results = []
    clear()
    rows = read_csvfile()
    if message:
        print(message)
    time = input('Time spent (in [w]eeks/[d]ays/[h]ours/'
                 '[m]inutes, eg. 1 h) or time range (eg. 1 h - 2 h): \n'
                 ).lower().strip()
    match = r'(?P<value>[0-9]+.?[0-9]*)\s*(?P<format>[wdhm])'
    times = re.findall(match, time)
    if times:
        times_min = convert_time_spent_to_min(times=times)
        # Search by time spent.
        if len(times) == 1:
            for row in rows:
                if float(row['Time spent (min)']) == times_min[0]:
                    search_results.append(row)
        # Search by time spent range.
        elif len(times) == 2:
            sorted_times_min = sorted(times_min)
            for row in rows:
                if float(row['Time spent (min)']) >= sorted_times_min[0] and (
                float(row['Time spent (min)']) <= sorted_times_min[-1]):
                    search_results.append(row)
        else:
            return search_by_time_spent(message='Invalid time format!')
        return search_results
    else:
        return search_by_time_spent(message='Invalid time format!')


def lookup_entry():
    """Look up an entry."""
    while True:
        clear()
        choice = input('Search by [D]ate, exact [S]tring, [R]egular '
                       'expression,\n[T]ime spent or go to the main [M]enu: '
                       ).lower().strip()
        if choice in 'dsrtm':
            break
    if choice == 'd':
        search_results = search_by_date()
        show_results(results=search_results)
    elif choice == 's' or choice == 'r':
        search_results = search_by_string_re()
        show_results(results=search_results)
    elif choice == 't':
        search_results = search_by_time_spent()
        show_results(results=search_results)



def menu_loop():
    """Show the menu."""
    while True:
        clear()
        for key, value in menu.items():
            print('[{}] {}'.format(key, value.__doc__))
        print('[Q] Quit the program')
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
