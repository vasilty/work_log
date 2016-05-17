import datetime
import os
import re
import sys


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


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
        time = input('Time spent (in [w]eeks/[d]ays/[h]ours/'
                     '[m]inutes, eg. 1 h): \n').lower().strip()
        match = r'(?P<value>^[0-9]+.?[0-9]*)\s*(?P<format>[wdhm])$'
        if re.search(match, time):
            time_value = float(re.search(match, time).group('value'))
            time_format = re.search(match, time).group('format')
            if time_format == 'w':
                self.time_spent = time_value * 7 * 24 * 60
            elif time_format == 'd':
                self.time_spent = time_value * 24 * 60
            elif time_format == 'h':
                self.time_spent = time_value * 60
            else:
                self.time_spent = time_value
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
