from calendar import monthrange
from datetime import date, timedelta


class GroupCellData():

    def __init__(self, group, task_manager, sum_task_delimiter, date_start, date_end):
        self.minutes = 0.0
        self.summary = ""
        self.group = group
        self.task_manager = task_manager
        self.sum_task_delimiter = sum_task_delimiter
        self.date_start = date_start
        self.date_end = date_end
        self.populate()

    def populate(self):
        tasks = self.task_manager.get_tasks_for_group(self.group, self.date_start, self.date_end)
        for task in tasks:
            self.add_task(task)
        self.remove_trailing_summary_delimiter()

    def add_task(self, task):
        self.minutes = self.minutes + task.get_duration()
        self.summary = self.summary + task.summary + self.sum_task_delimiter

    def remove_trailing_summary_delimiter(self):
        if len(self.summary) > 0:
            self.summary = self.summary[:-2]

    def get_duration(self, interval):
        if interval == 'hours':
            return round(self.minutes / 60, 2)
        elif interval == 'minutes':
            return self.minutes
        else:
            return self.minutes

    def to_plain_list(self):
        return [str(self.date_start), str(self.group), str(self.summary)]


class RowData():

    def __init__(self, groups, task_manager, sum_task_delimiter, date_start, date_end):
        self.minutes = 0.0
        self.groups = groups
        self.task_manager = task_manager
        self.sum_task_delimiter = sum_task_delimiter
        self.date_start = date_start
        self.date_end = date_end
        self.data = []
        self.populate()

    def populate(self):
        for group in self.groups:
            cell = GroupCellData(group, self.task_manager, self.sum_task_delimiter, self.date, self.date)
            self.data.append(cell)

    def get_duration(self, interval):
        duration = 0.0
        for cell in self.data:
            duration = duration + cell.get_duration(interval)
        return duration

    def to_plain_list(self):
        to_return = []
        for cell in self.data:
            to_return = to_return + [str(cell.get_duration("hours")), cell.summary]
        return to_return


class DailyRowData(RowData):

    def __init__(self, groups, task_manager, sum_task_delimiter, date_):
        self.day = date_.day
        RowData.__init__(self, groups, task_manager, sum_task_delimiter, date_, date_)


class WeeklyRowData(RowData):

    def __init__(self, groups, task_manager, sum_task_delimiter, week, year):
        self.week = week
        self.year = year
        date_start, date_end = self.week_beg_end(self.week, self.year)
        RowData.__init__(self, groups, task_manager, sum_task_delimiter, date_start, date_end)

    def week_beg_end(self, week, year):
        # HERE BE DRAGONS
        d = date(year, 1, 1)
        delta_days = d.isoweekday() - 1
        delta_weeks = week
        if year == d.isocalendar()[0]:
            delta_weeks -= 1
        # delta for the beginning of the week
        delta = timedelta(days=-delta_days, weeks=delta_weeks)
        week_beg = d + delta
        # delta2 for the end of the week
        delta2 = timedelta(days=6-delta_days, weeks=delta_weeks)
        week_end = d + delta2
        return week_beg, week_end


class MonthlyRowData(RowData):

    def __init__(self, groups, task_manager, sum_task_delimiter, month, year):
        self.month = month
        self.year = year
        date_start = date(self.year, self.month, 1)
        date_end = date(self.year, self.month, monthrange(self.year, self.month)[1] + 1)
        RowData.__init__(self, groups, task_manager, sum_task_delimiter, date_start, date_end)


class Report():

    def __init__(self, groups, task_manager, sum_task_delimiter, date_start, date_end):
        self.rows = []
        self.groups = groups
        self.task_manager = task_manager
        self.sum_task_delimiter = sum_task_delimiter
        self.date_start = date_start
        self.date_end = date_end

    def populate(self):
        raise NotImplementedError

    def get_total_hours(self):
        to_return = 0.0
        for row in self.rows:
            to_return = to_return + row.get_duration('hours')
        return to_return


class DailyReport(Report):
    def __init__(self, groups, task_manager, sum_task_delimiter, date_start, date_end):
        Report.__init__(self, groups, task_manager, sum_task_delimiter, date_start, date_end)
        self.populate()

    def populate(self):
        delta = self.date_end - self.date_start
        for i in range(delta.days + 1):
            day_date = self.date_start + timedelta(days=i)
            self.rows.append(DailyRowData(self.groups, self.task_manager, self.sum_task_delimiter, day_date))


class WeeklyReport(Report):
    def __init__(self, groups, task_manager, sum_task_delimiter, date_start, date_end):
        Report.__init__(self, groups, task_manager, sum_task_delimiter, date_start, date_end)
        self.populate()

    def populate(self):  # fixme - error when crossing years in weekly reports
        for week in self.week_numbers():
            self.rows.append(WeeklyRowData(self.groups, self.task_manager,
                                           self.sum_task_delimiter, week, self.date_start.year))

    def week_numbers(self):
        to_return = []
        delta = self.date_end - self.date_start
        for i in range(delta.days + 1):
            day_date = self.date_start + timedelta(days=i)
            week = day_date.isocalendar()[1]
            if not (week in to_return):
                to_return.append(week)
        return to_return

    def get_rows_week_numbers(self):
        to_return = []
        for row in self.rows:
            to_return.append(row.week)
        return to_return


class MonthlyReport(Report):
    def __init__(self, groups, task_manager, date_start, date_end):
        Report.__init__(self, groups, task_manager, date_start, date_end)
        self.populate()

    def populate(self):  # fixme - error when crossing years in weekly reports
        for month in self.get_month_numbers():
                self.rows.append(MonthlyRowData(self.groups, self.task_manager,
                                                self.sum_task_delimiter, month, self.date_start.year))

    def get_month_numbers(self):
        to_return = []
        delta = self.date_end - self.date_start
        for i in range(delta.days + 1):
            day_date = self.date_start + timedelta(days=i)
            month = day_date.month
            if not (month in to_return):
                to_return.append(month)
        return to_return