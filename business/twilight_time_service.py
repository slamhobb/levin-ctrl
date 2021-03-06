from datetime import date, datetime, timedelta
from pytz import timezone
from skyfield import almanac
from skyfield.api import N, E, wgs84, load, load_file

from lib.config import config


class TwilightTimeService:
    zone: timezone = timezone(config['TIME_ZONE'])
    date: date = None
    times: (datetime, datetime) = (None, None)

    def is_light_now(self) -> bool:
        now = self.zone.localize(datetime.now())
        start_time, end_time = self._get_times_with_cache(now)

        return start_time < now < end_time

    def _get_times_with_cache(self, now: datetime) -> [datetime, datetime]:
        today = now.date()

        if self.date == today:
            return self.times

        self.date = today
        start_date, end_date = self._get_times(now)
        self.times = start_date + timedelta(hours=1), end_date - timedelta(hours=1)

        return self.times

    def _get_times(self, now: datetime) -> (datetime, datetime):
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        next_midnight = midnight + timedelta(days=1)

        ts = load.timescale()
        t0 = ts.from_datetime(midnight)
        t1 = ts.from_datetime(next_midnight)
        eph = load_file(config['DE421_PATH'])
        bluffton = wgs84.latlon(config['COORDINATES']['N'] * N, config['COORDINATES']['E'] * E)
        f = almanac.dark_twilight_day(eph, bluffton)
        times, events = almanac.find_discrete(t0, t1, f)

        result = []
        previous_e = None
        for t, e in zip(times, events):
            if e == 4:
                result.append(t.astimezone(self.zone))
            if previous_e == 4:
                result.append(t.astimezone(self.zone))
            previous_e = e

        return result[0], result[1]
