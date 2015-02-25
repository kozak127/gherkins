import icalendar
import urllib


class Task():

    def __init__(self, project, summary, date, duration):
        self.project = project
        self.summary = summary
        self.date = date
        self.duration = duration

    def to_plain_list(self):
        return [str(self.date), str(self.project), str(self.summary)]

    def get_duration(self):
        return self.duration.seconds // 60


class TaskManager():

    def __init__(self, url, cal_delimiter):
        self.reader = CalFileReader(url, cal_delimiter)
        self.tasks = self.reader.read_tasks()

    def get_tasks_for_group(self, group, date_start, date_end):
        to_return = []
        projects = []

        # for group in groups:
        projects += group.split(', ')
        for task in self.tasks:
            if date_start <= task.date <= date_end and task.project in projects:
                to_return.append(task)
        return to_return

    def get_invalid_tasks(self, groups, date_start, date_end):
        to_return = []
        projects = []

        for group in groups:
            projects += group.split(', ')

        for task in self.tasks:
            if date_start <= task.date <= date_end and not (task.project in projects):
                to_return.append(task)

        if len(to_return) == 0:
            return None
        else:
            return to_return


class CalFileReader:

    def __init__(self, url, cal_delimiter):
        self.url = url
        self.cal_delimiter = cal_delimiter
        self.ical_file = urllib.urlopen(self.url)

    def read_tasks(self):
        tasks = []
        calendar_file = self.ical_file
        parsed_calendar = icalendar.Calendar.from_ical(calendar_file.read())

        for component in parsed_calendar.walk('vevent'):
            dtstart = component['dtstart'].dt
            dtend = component['dtend'].dt
            raw_summary = component['SUMMARY'].split(self.cal_delimiter, 1)
            project = raw_summary[0].lower()
            if len(raw_summary) > 1:
                summary = raw_summary[1]
            else:
                summary = ""

            duration = (dtend - dtstart)

            # icalendar lib returns datetime.date and datetime.datetime objects at random choice. Standardisation
            date = 0
            try:
                date = dtstart.date()
            except AttributeError:
                date = dtstart

            tasks.append(Task(project, summary, date, duration))

        calendar_file.close()
        return tasks
