from datetime import datetime, timedelta
from .monthdelta import MonthDelta

__author__ = 'Tom'


class DateOffset:
    def __init__(self):
        pass

    @staticmethod
    def get_offset(time_offset_string, start_date_time=None, include_time=False):

        if start_date_time is None:
            start_date_time = datetime.now()
        elif not isinstance(start_date_time, datetime):
            start_date_time = datetime.combine(start_date_time, datetime.min.time())

        if len(time_offset_string) == 0:
            return start_date_time.date()

        current_string = ""
        for c in time_offset_string:
            if c == '#':  # start of week
                start_date_time += timedelta(days=-start_date_time.weekday())
                current_string = ""

            elif c == '*':  # end of week
                start_date_time += timedelta(days=6-start_date_time.weekday())
                current_string = ""

            elif c == '%':  # first day of te month
                start_date_time = start_date_time.replace(day=1)
                current_string = ""
            elif c == "d":  # offset by days
                start_date_time += timedelta(days=int(current_string))
                current_string = ""
            elif c == "w":  # offset by weeks
                start_date_time += timedelta(weeks=int(current_string))
                current_string = ""
            elif c == "m":  # offset by months
                start_date_time += MonthDelta(int(current_string))
                current_string = ""
            elif c == "y":  # offset by years
                start_date_time += MonthDelta(int(current_string) * 12)
                current_string = ""
            elif c == 's':  # offset by seconds
                start_date_time += timedelta(seconds=int(current_string))
                current_string = ""
            elif c == 'i':  # offset by minutes
                start_date_time += timedelta(minutes=int(current_string))
                current_string = ""
            elif c == 'h':  # offset by hours
                start_date_time += timedelta(hours=int(current_string))
                current_string = ""

            elif c == '~':  # not weekend
                weekday = start_date_time.weekday()
                if weekday >= 5:
                    if weekday == 5:
                        start_date_time += timedelta(days=2)
                    elif weekday == 6:
                        start_date_time += timedelta(days=1)

            elif c == "t":
                data = current_string.split(':')
                hours = int(data[0])
                minutes = 0
                seconds = 0

                length = len(data)
                if length > 1:
                    minutes = int(data[1])
                if length > 2:
                    seconds = int(data[2])
                start_date_time = start_date_time.replace(hour=hours, minute=minutes, second=seconds, microsecond=0)
                include_time = True

            elif c == " ":
                continue
            else:
                current_string += c
        if include_time:
            return start_date_time
        else:
            return start_date_time.date()
