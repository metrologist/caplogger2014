# intertime.py is a datetime utility for sql_cap.py
from dateutil import parser
import datetime
from zoneinfo import ZoneInfo

class INTERTIME():
    def __init__(self, region):
        """

        Utility methods for working with time strings, datetime objects and decimal year. Set for NZ time zone
        with awareness of daylight saving. More methods could be added but stringing together a few will likely
        achieve the conversion you need.
        :param region: string, normally "Pacific/Auckland"
        """
        self.loc_zone = region

    def date_to_sec(self, string):
        """

        converts a string like 22 June, 2024, 1:30 PM into seconds since epoch
        :param string:
        :return: seconds since epoch
        """
        parsed_date = parser.parse(string)
        local_dt = parsed_date.replace(tzinfo=ZoneInfo(self.loc_zone))  # add time zone
        secs = int(local_dt.timestamp())
        return secs


    def sec_to_date(self, epoch_seconds):
        """

        :param seconds: since epoch time
        :return: a structured local datetime
        """
        # Convert to UTC datetime
        utc_dt = datetime.datetime.fromtimestamp(epoch_seconds, tz=ZoneInfo("UTC"))
        local_dt = utc_dt.astimezone(ZoneInfo(self.loc_zone))
        return local_dt

    @staticmethod
    def datetime_to_decimal_year(dt):
        """

        :param dt: a datetime object
        :return: a decimal year, e.g. 2025.321 in local time?
        """
        # Ensure dt is timezone-naive by converting to UTC if it's aware
        if dt.tzinfo is not None:
            dt = dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        year_start = datetime.datetime(dt.year, 1, 1)
        year_end = datetime.datetime(dt.year + 1, 1, 1)
        year_length = (year_end - year_start).total_seconds()
        seconds_into_year = (dt - year_start).total_seconds()
        decimal_year = dt.year + seconds_into_year / year_length
        return decimal_year

    @staticmethod
    def decimal_year_to_datetime(decimal_year):
        """

        :param decimal_year:
        :return: structured datetime local
        """
        tz_str = 'Pacific/Auckland'
        # Extract the integer year and the fractional part
        year = int(decimal_year)
        fraction = decimal_year - year

        # Define start and end of the year in UTC
        start_of_year = datetime.datetime(year, 1, 1, tzinfo=datetime.timezone.utc)
        start_of_next_year = datetime.datetime(year + 1, 1, 1, tzinfo=datetime.timezone.utc)
        # Total seconds in the year
        year_duration = (start_of_next_year - start_of_year).total_seconds()
        # Seconds into the year
        seconds_into_year = fraction * year_duration
        # Final UTC datetime
        utc_dt = start_of_year + datetime.timedelta(seconds=seconds_into_year)
        # Convert to target timezone
        local_dt = utc_dt.astimezone(ZoneInfo("Pacific/Auckland"))

        return local_dt

    @staticmethod
    def local_to_UTC(local_dt):
        """

        :param local_dt: assumed timezone aware, as out of sec_to_date
        :return:
        """
        utc_dt = local_dt.astimezone(ZoneInfo("UTC"))
        return utc_dt

if __name__ == '__main__':
    t = INTERTIME('Pacific/Auckland')
    # check daylight saving aware between 2:00 and 3:00 am when the clock changes
    a = '28 September, 2025, 1:59 AM'
    b = '28 September, 2025, 3:01 AM'
    minute_before = t.date_to_sec(a)
    minute_after = t.date_to_sec(b)
    print("a min before_summer time =", minute_before)
    print("a min after summer time =", minute_after)
    print('difference =', (minute_after - minute_before) / 60, 'minutes between 1:59 am and 3:01 am')  # should be 2 mins
    # and might need decimal year for plotting
    asec = 1758981540
    bsec = 1758981660
    print('a sec =', asec)
    print('b sec =', bsec)
    a_date = t.sec_to_date(asec)
    b_date = t.sec_to_date(bsec)
    print('calc a date =', a_date)
    print('calc b date =', b_date)
    a_dec = t.datetime_to_decimal_year(t.sec_to_date(asec))
    b_dec = t.datetime_to_decimal_year(t.sec_to_date(bsec))
    print('calc a dec =', a_dec)
    print('calc b dec =', b_dec)
    rec_a_date = t.decimal_year_to_datetime(a_dec)
    rec_b_date = t.decimal_year_to_datetime(b_dec)
    print('recover a =', rec_a_date)
    print('recover b =', rec_b_date)

    # checking more daylight saving conversions
    # start with a summer time
    summer_test = '22 December, 2024, 1:30 PM'
    print('summer_test =', summer_test)
    summer_sec = t.date_to_sec(summer_test)
    summer_date = t.sec_to_date(summer_sec)
    print('summer_date =', summer_date)
    summer_dec = t.datetime_to_decimal_year(summer_date)
    print('summer_dec =', summer_dec)
    summer_date_recovered = t.decimal_year_to_datetime(summer_dec)
    print('summer_date_recovered =', summer_date_recovered)

    winter_test = '22 June, 2024, 1:30 PM'
    print('winter_test =', winter_test)
    winter_sec = t.date_to_sec(winter_test)
    winter_date = t.sec_to_date(winter_sec)
    print('winter_date =', winter_date)
    winter_dec = t.datetime_to_decimal_year(winter_date)
    print('winter_dec =', winter_dec)
    winter_date_recovered = t.decimal_year_to_datetime(winter_dec)
    print('winter_date_recovered =', winter_date_recovered)

    # need to look up utc timed temperature records

    summer_test = '22 December, 2024, 9:30 AM'
    print('summer_test =', summer_test)
    summer_sec = t.date_to_sec(summer_test)
    summer_date = t.sec_to_date(summer_sec)
    summer_utc = t.local_to_UTC(summer_date)
    print('summer_utc =', summer_utc)

