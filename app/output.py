import csv
import os


class GeneralOutput:

    def __init__(self):
        pass

    def process_monthly_reports(self, report_instance):
        raise NotImplementedError("process_monthly_reports")

    def process_weekly_reports(self, report_instance):
        raise NotImplementedError("process_weekly_reports")

    def process_daily_reports(self, report_instance):
        raise NotImplementedError("process_daily_reports")

    def process_invalid_events(self, task_manager):
        raise NotImplementedError("process_invalid_events")


class CsvOutput(GeneralOutput):

    def __init__(self, csv_delimiter, filename_pattern, csv_directory, month, year):
        GeneralOutput.__init__(self)
        self.delimiter = csv_delimiter
        self.filename_pattern = filename_pattern
        self.csv_directory = csv_directory
        self.month = month
        self.year = year

    def process_monthly_reports(self, report_instance):
        csv_file_path = self.generate_filepath('monthly', '.csv')
        data = []
        heading = ['GROUP', 'HOURS']

        for row in report_instance.rows:
            data_row = []
            data_row.append(str(row.group))
            data_row.append(str(row.get_duration('hours')))
            data.append(data_row)

        data.append(['TOTAL', str(report_instance.get_total_hours())])

        self.csv_writer(heading, data, csv_file_path, self.delimiter)

    def process_weekly_reports(self, report_instance):
        csv_file_path = self.generate_filepath('weekly', '.csv')
        data = []
        heading = ['TOTAL', '###', 'WEEK', '###']
        for group in report_instance.groups:
            heading.append('###')
            heading.append(group.upper())

        for row in report_instance.rows:
            data_row = []
            data_row.append(str(row.get_duration('hours')))
            data_row.append('   ')
            data_row.append(str(row.week))
            data_row.append('   ')
            data_row.append(row.to_plain_list())
            data.append(data_row)

        self.csv_writer(heading, data, csv_file_path, self.delimiter)

    def process_daily_reports(self, report_instance):
        csv_file_path = self.generate_filepath('daily', '.csv')
        data = []

        heading = ['TOTAL', '###', 'DAY', '###']
        for group in report_instance.groups:
            heading.append('###')
            heading.append(group.upper())

        for row in report_instance.rows:
            data_row = []
            data_row.append(str(row.get_duration('hours')))
            data_row.append('   ')
            data_row.append(str(row.day))
            data_row.append('   ')
            data_row.append(row.to_plain_list())
            data.append(data_row)

        self.csv_writer(heading, data, csv_file_path, self.delimiter)

    def process_invalid_events(self, invalid_tasks):
        csv_file_path = self.generate_filepath('invalid', '.csv')
        data = []
        heading = ['date', 'group', 'summary']

        for task in invalid_tasks:
            data.append(task.to_plain_list())

        self.csv_writer(heading, data, csv_file_path, self.delimiter)

    def csv_writer(self, heading, data, path, delimiter):
        with open(path, "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter)
            heading = [s.encode('utf-8') for s in heading]
            writer.writerow(heading)
            for line in data:
                line = [s.encode('utf-8') for s in line]
                writer.writerow(line)

    def generate_filepath(self, case, filetype):
        directory = self.csv_directory
        filename = self.filename_pattern
        filename = filename.replace('%M', str(self.month))
        filename = filename.replace('%Y', str(self.year))
        filename = filename.replace('%T', case)
        filepath = directory + os.sep + filename + filetype
        return filepath
