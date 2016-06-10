import datetime
import os
import re
import sys


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def convert_time_spent_to_min(time):
    """Converts time from w/d/h/m to minutes."""
    time_value = float(time[0])
    time_format = time[1]
    if time_format == 'w':
        time_min = time_value * 7 * 24 * 60
    elif time_format == 'd':
        time_min = time_value * 24 * 60
    elif time_format == 'h':
        time_min = time_value * 60
    else:
        time_min = time_value
    return time_min


class Entry:
    def get_name(self, message=None):
        """Gets task name and checks that its length > 0."""
        clear()
        if message:
            print(message)
        self.name = input('Task name: \n').strip()
        if len(self.name) == 0:
            return self.get_name(message='Task name should be at least one character'
                                         ' long!')

    def get_time_spent(self, message=None):
        """Gets time spent in a proper format and returns a value in minutes."""
        clear()
        if message:
            print(message)
        time_input = input('Time spent (in [w]eeks/[d]ays/[h]ours/'
                     '[m]inutes, eg. 1 h): \n').lower().strip()
        match = r'(?P<value>^[0-9]+.?[0-9]*)\s*(?P<format>[wdhm])$'
        time = re.findall(match, time_input)
        if time:
            self.time_spent = convert_time_spent_to_min(time=time[0])
            if self.time_spent <= 0:
                return self.get_time_spent(message="Time spent must be positive!")
        else:
            return self.get_time_spent(message='Invalid time format!')

    def get_notes(self):
        """Gets notes, which can be empty, contain multiple lines."""
        clear()
        print('General notes (press ctrl+d when finished): ')
        self.notes = sys.stdin.read().strip()

    def get_date(self, message=None):
        """Get valid date."""
        clear()
        if message:
            print(message)
        while True:
            date = input("Date (dd.mm.yyyy): ").strip()
            # Check that user provided a valid date.
            try:
                datetime.datetime.strptime(date, '%d.%m.%Y')
            except ValueError:
                return self.get_date(message='Wrong date format!')
            else:
                self.date = date
                break

    def __init__(self):
        self.get_name()
        self.get_time_spent()
        self.get_notes()
        self.date = datetime.datetime.now().date().strftime('%d.%m.%Y')
