#
# Copyright (C) 2007-2011 Edgewall Software, 2013-2022 the Babel team
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution. The terms
# are also available at http://babel.edgewall.org/wiki/License.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://babel.edgewall.org/log/.

import calendar
from datetime import date, datetime, time, timedelta
import unittest

import freezegun
import pytest
import pytz
from pytz import timezone

from babel import dates, Locale
from babel.dates import NO_INHERITANCE_MARKER
from babel.util import FixedOffsetTimezone


@pytest.fixture(params=["pytz.timezone", "zoneinfo.ZoneInfo"])
def timezone_getter(request):
    if request.param == "pytz.timezone":
        return timezone
    elif request.param == "zoneinfo.ZoneInfo":
        try:
            import zoneinfo
        except ImportError:
            try:
                from backports import zoneinfo
            except ImportError:
                pytest.skip("zoneinfo not available")
        return zoneinfo.ZoneInfo
    else:
        raise NotImplementedError


class DateTimeFormatTestCase(unittest.TestCase):

    def test_quarter_format(self):
        d = date(2006, 6, 8)
        fmt = dates.DateTimeFormat(d, locale='en_US')
        assert fmt['Q'] == '2'
        assert fmt['QQQQ'] == '2nd quarter'
        assert fmt['q'] == '2'
        assert fmt['qqqq'] == '2nd quarter'
        d = date(2006, 12, 31)
        fmt = dates.DateTimeFormat(d, locale='en_US')
        assert fmt['qqq'] == 'Q4'
        assert fmt['qqqqq'] == '4'
        assert fmt['QQQ'] == 'Q4'
        assert fmt['QQQQQ'] == '4'

    def test_month_context(self):
        d = date(2006, 2, 8)
        assert dates.DateTimeFormat(d, locale='mt_MT')['MMMMM'] == 'F'  # narrow format
        assert dates.DateTimeFormat(d, locale='mt_MT')['LLLLL'] == 'Fr'  # narrow standalone

    def test_abbreviated_month_alias(self):
        d = date(2006, 3, 8)
        assert dates.DateTimeFormat(d, locale='de_DE')['LLL'] == 'Mär'

    def test_week_of_year_first(self):
        d = date(2006, 1, 8)
        assert dates.DateTimeFormat(d, locale='de_DE')['w'] == '1'
        assert dates.DateTimeFormat(d, locale='en_US')['ww'] == '02'

    def test_week_of_year_first_with_year(self):
        d = date(2006, 1, 1)
        fmt = dates.DateTimeFormat(d, locale='de_DE')
        assert fmt['w'] == '52'
        assert fmt['YYYY'] == '2005'

    def test_week_of_year_last(self):
        d = date(2006, 12, 26)
        assert dates.DateTimeFormat(d, locale='de_DE')['w'] == '52'
        assert dates.DateTimeFormat(d, locale='en_US')['w'] == '52'

    def test_week_of_year_last_us_extra_week(self):
        d = date(2005, 12, 26)
        assert dates.DateTimeFormat(d, locale='de_DE')['w'] == '52'
        assert dates.DateTimeFormat(d, locale='en_US')['w'] == '53'

    def test_week_of_year_de_first_us_last_with_year(self):
        d = date(2018,12,31)
        fmt = dates.DateTimeFormat(d, locale='de_DE')
        assert fmt['w'] == '1'
        assert fmt['YYYY'] == '2019'
        fmt = dates.DateTimeFormat(d, locale='en_US')
        assert fmt['w'] == '53'
        assert fmt['yyyy'] == '2018'

    def test_week_of_month_first(self):
        d = date(2006, 1, 8)
        assert dates.DateTimeFormat(d, locale='de_DE')['W'] == '1'
        assert dates.DateTimeFormat(d, locale='en_US')['W'] == '2'

    def test_week_of_month_last(self):
        d = date(2006, 1, 29)
        assert dates.DateTimeFormat(d, locale='de_DE')['W'] == '4'
        assert dates.DateTimeFormat(d, locale='en_US')['W'] == '5'

    def test_day_of_year(self):
        d = date(2007, 4, 1)
        assert dates.DateTimeFormat(d, locale='en_US')['D'] == '91'

    def test_day_of_year_works_with_datetime(self):
        d = datetime(2007, 4, 1)
        assert dates.DateTimeFormat(d, locale='en_US')['D'] == '91'

    def test_day_of_year_first(self):
        d = date(2007, 1, 1)
        assert dates.DateTimeFormat(d, locale='en_US')['DDD'] == '001'

    def test_day_of_year_last(self):
        d = date(2007, 12, 31)
        assert dates.DateTimeFormat(d, locale='en_US')['DDD'] == '365'

    def test_day_of_week_in_month(self):
        d = date(2007, 4, 15)
        assert dates.DateTimeFormat(d, locale='en_US')['F'] == '3'

    def test_day_of_week_in_month_first(self):
        d = date(2007, 4, 1)
        assert dates.DateTimeFormat(d, locale='en_US')['F'] == '1'

    def test_day_of_week_in_month_last(self):
        d = date(2007, 4, 29)
        assert dates.DateTimeFormat(d, locale='en_US')['F'] == '5'

    def test_local_day_of_week(self):
        d = date(2007, 4, 1)  # a sunday
        assert dates.DateTimeFormat(d, locale='de_DE')['e'] == '7'  # monday is first day of week
        assert dates.DateTimeFormat(d, locale='en_US')['ee'] == '01'  # sunday is first day of week
        assert dates.DateTimeFormat(d, locale='ar_BH')['ee'] == '02'  # saturday is first day of week

        d = date(2007, 4, 2)  # a monday
        assert dates.DateTimeFormat(d, locale='de_DE')['e'] == '1'  # monday is first day of week
        assert dates.DateTimeFormat(d, locale='en_US')['ee'] == '02'  # sunday is first day of week
        assert dates.DateTimeFormat(d, locale='ar_BH')['ee'] == '03'  # saturday is first day of week

    def test_local_day_of_week_standalone(self):
        d = date(2007, 4, 1)  # a sunday
        assert dates.DateTimeFormat(d, locale='de_DE')['c'] == '7'  # monday is first day of week
        assert dates.DateTimeFormat(d, locale='en_US')['c'] == '1'  # sunday is first day of week
        assert dates.DateTimeFormat(d, locale='ar_BH')['c'] == '2'  # saturday is first day of week

        d = date(2007, 4, 2)  # a monday
        assert dates.DateTimeFormat(d, locale='de_DE')['c'] == '1'  # monday is first day of week
        assert dates.DateTimeFormat(d, locale='en_US')['c'] == '2'  # sunday is first day of week
        assert dates.DateTimeFormat(d, locale='ar_BH')['c'] == '3'  # saturday is first day of week

    def test_pattern_day_of_week(self):
        dt = datetime(2016, 2, 6)
        fmt = dates.DateTimeFormat(dt, locale='en_US')
        assert fmt['c'] == '7'
        assert fmt['ccc'] == 'Sat'
        assert fmt['cccc'] == 'Saturday'
        assert fmt['ccccc'] == 'S'
        assert fmt['cccccc'] == 'Sa'
        assert fmt['e'] == '7'
        assert fmt['ee'] == '07'
        assert fmt['eee'] == 'Sat'
        assert fmt['eeee'] == 'Saturday'
        assert fmt['eeeee'] == 'S'
        assert fmt['eeeeee'] == 'Sa'
        assert fmt['E'] == 'Sat'
        assert fmt['EE'] == 'Sat'
        assert fmt['EEE'] == 'Sat'
        assert fmt['EEEE'] == 'Saturday'
        assert fmt['EEEEE'] == 'S'
        assert fmt['EEEEEE'] == 'Sa'
        fmt = dates.DateTimeFormat(dt, locale='uk')
        assert fmt['c'] == '6'
        assert fmt['e'] == '6'
        assert fmt['ee'] == '06'

    def test_fractional_seconds(self):
        t = time(8, 3, 9, 799)
        assert dates.DateTimeFormat(t, locale='en_US')['S'] == '0'
        t = time(8, 3, 1, 799)
        assert dates.DateTimeFormat(t, locale='en_US')['SSSS'] == '0008'
        t = time(8, 3, 1, 34567)
        assert dates.DateTimeFormat(t, locale='en_US')['SSSS'] == '0346'
        t = time(8, 3, 1, 345678)
        assert dates.DateTimeFormat(t, locale='en_US')['SSSSSS'] == '345678'
        t = time(8, 3, 1, 799)
        assert dates.DateTimeFormat(t, locale='en_US')['SSSSS'] == '00080'

    def test_fractional_seconds_zero(self):
        t = time(15, 30, 0)
        assert dates.DateTimeFormat(t, locale='en_US')['SSSS'] == '0000'

    def test_milliseconds_in_day(self):
        t = time(15, 30, 12, 345000)
        assert dates.DateTimeFormat(t, locale='en_US')['AAAA'] == '55812345'

    def test_milliseconds_in_day_zero(self):
        d = time(0, 0, 0)
        assert dates.DateTimeFormat(d, locale='en_US')['AAAA'] == '0000'

    def test_timezone_rfc822(self):
        tz = timezone('Europe/Berlin')
        t = tz.localize(datetime(2015, 1, 1, 15, 30))
        assert dates.DateTimeFormat(t, locale='de_DE')['Z'] == '+0100'

    def test_timezone_gmt(self):
        tz = timezone('Europe/Berlin')
        t = tz.localize(datetime(2015, 1, 1, 15, 30))
        assert dates.DateTimeFormat(t, locale='de_DE')['ZZZZ'] == 'GMT+01:00'

    def test_timezone_name(self):
        tz = timezone('Europe/Paris')
        dt = tz.localize(datetime(2007, 4, 1, 15, 30))
        assert dates.DateTimeFormat(dt, locale='fr_FR')['v'] == 'heure : France'

    def test_timezone_location_format(self):
        tz = timezone('Europe/Paris')
        dt = datetime(2007, 4, 1, 15, 30, tzinfo=tz)
        assert dates.DateTimeFormat(dt, locale='fr_FR')['VVVV'] == 'heure : France'

    def test_timezone_walltime_short(self):
        tz = timezone('Europe/Paris')
        t = time(15, 30, tzinfo=tz)
        assert dates.DateTimeFormat(t, locale='fr_FR')['v'] == 'heure : France'

    def test_timezone_walltime_long(self):
        tz = timezone('Europe/Paris')
        t = time(15, 30, tzinfo=tz)
        assert dates.DateTimeFormat(t, locale='fr_FR')['vvvv'] == u'heure d’Europe centrale'

    def test_hour_formatting(self):
        l = 'en_US'
        t = time(0, 0, 0)
        assert dates.format_time(t, 'h a', locale=l) == '12 AM'
        assert dates.format_time(t, 'H', locale=l) == '0'
        assert dates.format_time(t, 'k', locale=l) == '24'
        assert dates.format_time(t, 'K a', locale=l) == '0 AM'
        t = time(12, 0, 0)
        assert dates.format_time(t, 'h a', locale=l) == '12 PM'
        assert dates.format_time(t, 'H', locale=l) == '12'
        assert dates.format_time(t, 'k', locale=l) == '12'
        assert dates.format_time(t, 'K a', locale=l) == '0 PM'


class FormatDateTestCase(unittest.TestCase):

    def test_with_time_fields_in_pattern(self):
        with pytest.raises(AttributeError):
            dates.format_date(date(2007, 4, 1), "yyyy-MM-dd HH:mm", locale='en_US')

    def test_with_time_fields_in_pattern_and_datetime_param(self):
        with pytest.raises(AttributeError):
            dates.format_date(datetime(2007, 4, 1, 15, 30), "yyyy-MM-dd HH:mm", locale='en_US')

    def test_with_day_of_year_in_pattern_and_datetime_param(self):
        # format_date should work on datetimes just as well (see #282)
        d = datetime(2007, 4, 1)
        assert dates.format_date(d, 'w', locale='en_US') == '14'


class FormatDatetimeTestCase(unittest.TestCase):

    def test_with_float(self):
        d = datetime(2012, 4, 1, 15, 30, 29, tzinfo=timezone('UTC'))
        epoch = float(calendar.timegm(d.timetuple()))
        formatted_string = dates.format_datetime(epoch, format='long', locale='en_US')
        assert formatted_string == u'April 1, 2012 at 3:30:29 PM UTC'

    def test_timezone_formats_los_angeles(self):
        dt = datetime(2016, 1, 13, 7, 8, 35)
        tz = dates.get_timezone('America/Los_Angeles')
        dt = tz.localize(dt)
        assert dates.format_datetime(dt, 'z', locale='en') == u'PST'
        assert dates.format_datetime(dt, 'zz', locale='en') == u'PST'
        assert dates.format_datetime(dt, 'zzz', locale='en') == u'PST'
        assert dates.format_datetime(dt, 'zzzz', locale='en') == u'Pacific Standard Time'
        assert dates.format_datetime(dt, 'Z', locale='en') == u'-0800'
        assert dates.format_datetime(dt, 'ZZ', locale='en') == u'-0800'
        assert dates.format_datetime(dt, 'ZZZ', locale='en') == u'-0800'
        assert dates.format_datetime(dt, 'ZZZZ', locale='en') == u'GMT-08:00'
        assert dates.format_datetime(dt, 'ZZZZZ', locale='en') == u'-08:00'
        assert dates.format_datetime(dt, 'OOOO', locale='en') == u'GMT-08:00'
        assert dates.format_datetime(dt, 'VV', locale='en') == u'America/Los_Angeles'
        assert dates.format_datetime(dt, 'VVV', locale='en') == u'Los Angeles'
        assert dates.format_datetime(dt, 'X', locale='en') == u'-08'
        assert dates.format_datetime(dt, 'XX', locale='en') == u'-0800'
        assert dates.format_datetime(dt, 'XXX', locale='en') == u'-08:00'
        assert dates.format_datetime(dt, 'XXXX', locale='en') == u'-0800'
        assert dates.format_datetime(dt, 'XXXXX', locale='en') == u'-08:00'
        assert dates.format_datetime(dt, 'x', locale='en') == u'-08'
        assert dates.format_datetime(dt, 'xx', locale='en') == u'-0800'
        assert dates.format_datetime(dt, 'xxx', locale='en') == u'-08:00'
        assert dates.format_datetime(dt, 'xxxx', locale='en') == u'-0800'
        assert dates.format_datetime(dt, 'xxxxx', locale='en') == u'-08:00'

    def test_timezone_formats_utc(self):
        dt = datetime(2016, 1, 13, 7, 8, 35)
        tz = dates.get_timezone('UTC')
        dt = tz.localize(dt)
        assert dates.format_datetime(dt, 'Z', locale='en') == u'+0000'
        assert dates.format_datetime(dt, 'ZZ', locale='en') == u'+0000'
        assert dates.format_datetime(dt, 'ZZZ', locale='en') == u'+0000'
        assert dates.format_datetime(dt, 'ZZZZ', locale='en') == u'GMT+00:00'
        assert dates.format_datetime(dt, 'ZZZZZ', locale='en') == u'Z'
        assert dates.format_datetime(dt, 'OOOO', locale='en') == u'GMT+00:00'
        assert dates.format_datetime(dt, 'VV', locale='en') == u'Etc/UTC'
        assert dates.format_datetime(dt, 'VVV', locale='en') == u'UTC'
        assert dates.format_datetime(dt, 'X', locale='en') == u'Z'
        assert dates.format_datetime(dt, 'XX', locale='en') == u'Z'
        assert dates.format_datetime(dt, 'XXX', locale='en') == u'Z'
        assert dates.format_datetime(dt, 'XXXX', locale='en') == u'Z'
        assert dates.format_datetime(dt, 'XXXXX', locale='en') == u'Z'
        assert dates.format_datetime(dt, 'x', locale='en') == u'+00'
        assert dates.format_datetime(dt, 'xx', locale='en') == u'+0000'
        assert dates.format_datetime(dt, 'xxx', locale='en') == u'+00:00'
        assert dates.format_datetime(dt, 'xxxx', locale='en') == u'+0000'
        assert dates.format_datetime(dt, 'xxxxx', locale='en') == u'+00:00'

    def test_timezone_formats_kolkata(self):
        dt = datetime(2016, 1, 13, 7, 8, 35)
        tz = dates.get_timezone('Asia/Kolkata')
        dt = tz.localize(dt)
        assert dates.format_datetime(dt, 'zzzz', locale='en') == u'India Standard Time'
        assert dates.format_datetime(dt, 'ZZZZ', locale='en') == u'GMT+05:30'
        assert dates.format_datetime(dt, 'ZZZZZ', locale='en') == u'+05:30'
        assert dates.format_datetime(dt, 'OOOO', locale='en') == u'GMT+05:30'
        assert dates.format_datetime(dt, 'VV', locale='en') == u'Asia/Calcutta'
        assert dates.format_datetime(dt, 'VVV', locale='en') == u'Kolkata'
        assert dates.format_datetime(dt, 'X', locale='en') == u'+0530'
        assert dates.format_datetime(dt, 'XX', locale='en') == u'+0530'
        assert dates.format_datetime(dt, 'XXX', locale='en') == u'+05:30'
        assert dates.format_datetime(dt, 'XXXX', locale='en') == u'+0530'
        assert dates.format_datetime(dt, 'XXXXX', locale='en') == u'+05:30'
        assert dates.format_datetime(dt, 'x', locale='en') == u'+0530'
        assert dates.format_datetime(dt, 'xx', locale='en') == u'+0530'
        assert dates.format_datetime(dt, 'xxx', locale='en') == u'+05:30'
        assert dates.format_datetime(dt, 'xxxx', locale='en') == u'+0530'
        assert dates.format_datetime(dt, 'xxxxx', locale='en') == u'+05:30'


class FormatTimeTestCase(unittest.TestCase):

    def test_with_naive_datetime_and_tzinfo(self):
        assert dates.format_time(
            datetime(2007, 4, 1, 15, 30),
            'long',
            tzinfo=timezone('US/Eastern'),
            locale='en',
        ) == '11:30:00 AM EDT'

    def test_with_float(self):
        d = datetime(2012, 4, 1, 15, 30, 29, tzinfo=timezone('UTC'))
        epoch = float(calendar.timegm(d.timetuple()))
        assert dates.format_time(epoch, format='long', locale='en_US') == u'3:30:29 PM UTC'

    def test_with_date_fields_in_pattern(self):
        with pytest.raises(AttributeError):
            dates.format_time(datetime(2007, 4, 1), 'yyyy-MM-dd HH:mm', locale='en')

    def test_with_date_fields_in_pattern_and_datetime_param(self):
        with pytest.raises(AttributeError):
            dates.format_time(datetime(2007, 4, 1, 15, 30), "yyyy-MM-dd HH:mm", locale='en_US')


class FormatTimedeltaTestCase(unittest.TestCase):

    def test_zero_seconds(self):
        td = timedelta(seconds=0)
        assert dates.format_timedelta(td, locale='en') == '0 seconds'
        assert dates.format_timedelta(td, locale='en', format='short') == '0 sec'
        assert dates.format_timedelta(td, granularity='hour', locale='en') == '0 hours'
        assert dates.format_timedelta(td, granularity='hour', locale='en', format='short') == '0 hr'

    def test_small_value_with_granularity(self):
        td = timedelta(seconds=42)
        assert dates.format_timedelta(td, granularity='hour', locale='en') == '1 hour'
        assert dates.format_timedelta(td, granularity='hour', locale='en', format='short') == '1 hr'

    def test_direction_adding(self):
        td = timedelta(hours=1)
        assert dates.format_timedelta(td, locale='en', add_direction=True) == 'in 1 hour'
        assert dates.format_timedelta(-td, locale='en', add_direction=True) == '1 hour ago'

    def test_format_narrow(self):
        assert dates.format_timedelta(timedelta(hours=1), locale='en', format='narrow') == '1h'
        assert dates.format_timedelta(timedelta(hours=-2), locale='en', format='narrow') == '2h'

    def test_format_invalid(self):
        for format in (None, '', 'bold italic'):
            with pytest.raises(TypeError):
                dates.format_timedelta(timedelta(hours=1), format=format)


class TimeZoneAdjustTestCase(unittest.TestCase):

    def _utc(self):
        class EvilFixedOffsetTimezone(FixedOffsetTimezone):

            def localize(self, dt, is_dst=False):
                raise NotImplementedError()
        UTC = EvilFixedOffsetTimezone(0, 'UTC')
        # This is important to trigger the actual bug (#257)
        assert hasattr(UTC, 'normalize') is False
        return UTC

    def test_can_format_time_with_non_pytz_timezone(self):
        # regression test for #257
        utc = self._utc()
        t = datetime(2007, 4, 1, 15, 30, tzinfo=utc)
        formatted_time = dates.format_time(t, 'long', tzinfo=utc, locale='en')
        assert formatted_time == '3:30:00 PM UTC'


def test_get_period_names():
    assert dates.get_period_names(locale='en_US')['am'] == u'AM'


def test_get_day_names():
    assert dates.get_day_names('wide', locale='en_US')[1] == u'Tuesday'
    assert dates.get_day_names('short', locale='en_US')[1] == u'Tu'
    assert dates.get_day_names('abbreviated', locale='es')[1] == u'mar'
    de = dates.get_day_names('narrow', context='stand-alone', locale='de_DE')
    assert de[1] == u'D'


def test_get_month_names():
    assert dates.get_month_names('wide', locale='en_US')[1] == u'January'
    assert dates.get_month_names('abbreviated', locale='es')[1] == u'ene'
    de = dates.get_month_names('narrow', context='stand-alone', locale='de_DE')
    assert de[1] == u'J'


def test_get_quarter_names():
    assert dates.get_quarter_names('wide', locale='en_US')[1] == u'1st quarter'
    assert dates.get_quarter_names('abbreviated', locale='de_DE')[1] == u'Q1'
    assert dates.get_quarter_names('narrow', locale='de_DE')[1] == u'1'


def test_get_era_names():
    assert dates.get_era_names('wide', locale='en_US')[1] == u'Anno Domini'
    assert dates.get_era_names('abbreviated', locale='de_DE')[1] == u'n. Chr.'


def test_get_date_format():
    us = dates.get_date_format(locale='en_US')
    assert us.pattern == u'MMM d, y'
    de = dates.get_date_format('full', locale='de_DE')
    assert de.pattern == u'EEEE, d. MMMM y'


def test_get_datetime_format():
    assert dates.get_datetime_format(locale='en_US') == u'{1}, {0}'


def test_get_time_format():
    assert dates.get_time_format(locale='en_US').pattern == u'h:mm:ss a'
    assert (dates.get_time_format('full', locale='de_DE').pattern ==
            u'HH:mm:ss zzzz')


def test_get_timezone_gmt():
    dt = datetime(2007, 4, 1, 15, 30)
    assert dates.get_timezone_gmt(dt, locale='en') == u'GMT+00:00'
    assert dates.get_timezone_gmt(dt, locale='en', return_z=True) == 'Z'
    assert dates.get_timezone_gmt(dt, locale='en', width='iso8601_short') == u'+00'
    tz = timezone('America/Los_Angeles')
    dt = tz.localize(datetime(2007, 4, 1, 15, 30))
    assert dates.get_timezone_gmt(dt, locale='en') == u'GMT-07:00'
    assert dates.get_timezone_gmt(dt, 'short', locale='en') == u'-0700'
    assert dates.get_timezone_gmt(dt, locale='en', width='iso8601_short') == u'-07'
    assert dates.get_timezone_gmt(dt, 'long', locale='fr_FR') == u'UTC-07:00'


def test_get_timezone_location(timezone_getter):
    tz = timezone_getter('America/St_Johns')
    assert (dates.get_timezone_location(tz, locale='de_DE') ==
            u"Kanada (St. John\u2019s) Zeit")
    assert (dates.get_timezone_location(tz, locale='en') ==
            u'Canada (St. John’s) Time')
    assert (dates.get_timezone_location(tz, locale='en', return_city=True) ==
            u'St. John’s')

    tz = timezone_getter('America/Mexico_City')
    assert (dates.get_timezone_location(tz, locale='de_DE') ==
            u'Mexiko (Mexiko-Stadt) Zeit')

    tz = timezone_getter('Europe/Berlin')
    assert (dates.get_timezone_location(tz, locale='de_DE') ==
            u'Deutschland (Berlin) Zeit')


@pytest.mark.parametrize(
    "tzname, params, expected",
    [
        ("America/Los_Angeles", {"locale": "en_US"}, u"Pacific Time"),
        ("America/Los_Angeles", {"width": "short", "locale": "en_US"}, u"PT"),
        ("Europe/Berlin", {"locale": "de_DE"}, u"Mitteleurop\xe4ische Zeit"),
        ("Europe/Berlin", {"locale": "pt_BR"}, u"Hor\xe1rio da Europa Central"),
        ("America/St_Johns", {"locale": "de_DE"}, u"Neufundland-Zeit"),
        (
            "America/Los_Angeles",
            {"locale": "en", "width": "short", "zone_variant": "generic"},
            u"PT",
        ),
        (
            "America/Los_Angeles",
            {"locale": "en", "width": "short", "zone_variant": "standard"},
            u"PST",
        ),
        (
            "America/Los_Angeles",
            {"locale": "en", "width": "short", "zone_variant": "daylight"},
            u"PDT",
        ),
        (
            "America/Los_Angeles",
            {"locale": "en", "width": "long", "zone_variant": "generic"},
            u"Pacific Time",
        ),
        (
            "America/Los_Angeles",
            {"locale": "en", "width": "long", "zone_variant": "standard"},
            u"Pacific Standard Time",
        ),
        (
            "America/Los_Angeles",
            {"locale": "en", "width": "long", "zone_variant": "daylight"},
            u"Pacific Daylight Time",
        ),
        ("Europe/Berlin", {"locale": "en_US"}, u"Central European Time"),
    ],
)
def test_get_timezone_name_tzinfo(timezone_getter, tzname, params, expected):
    tz = timezone_getter(tzname)
    assert dates.get_timezone_name(tz, **params) == expected


@pytest.mark.parametrize("timezone_getter", ["pytz.timezone"], indirect=True)
@pytest.mark.parametrize(
    "tzname, params, expected",
    [
        ("America/Los_Angeles", {"locale": "en_US"}, u"Pacific Standard Time"),
        (
            "America/Los_Angeles",
            {"locale": "en_US", "return_zone": True},
            u"America/Los_Angeles",
        ),
        ("America/Los_Angeles", {"width": "short", "locale": "en_US"}, u"PST"),
    ],
)
def test_get_timezone_name_time_pytz(timezone_getter, tzname, params, expected):
    """pytz (by design) can't determine if the time is in DST or not,
    so it will always return Standard time"""
    dt = time(15, 30, tzinfo=timezone_getter(tzname))
    assert dates.get_timezone_name(dt, **params) == expected


def test_get_timezone_name_misc(timezone_getter):
    localnow = datetime.utcnow().replace(tzinfo=timezone_getter('UTC')).astimezone(dates.LOCALTZ)
    assert (dates.get_timezone_name(None, locale='en_US') ==
            dates.get_timezone_name(localnow, locale='en_US'))

    assert (dates.get_timezone_name('Europe/Berlin', locale='en_US') == "Central European Time")

    assert (dates.get_timezone_name(1400000000, locale='en_US', width='short') == "Unknown Region (UTC) Time")
    assert (dates.get_timezone_name(time(16, 20), locale='en_US', width='short') == "UTC")


def test_format_date():
    d = date(2007, 4, 1)
    assert dates.format_date(d, locale='en_US') == u'Apr 1, 2007'
    assert (dates.format_date(d, format='full', locale='de_DE') ==
            u'Sonntag, 1. April 2007')
    assert (dates.format_date(d, "EEE, MMM d, ''yy", locale='en') ==
            u"Sun, Apr 1, '07")


def test_format_datetime():
    dt = datetime(2007, 4, 1, 15, 30)
    assert (dates.format_datetime(dt, locale='en_US') ==
            u'Apr 1, 2007, 3:30:00 PM')

    full = dates.format_datetime(dt, 'full', tzinfo=timezone('Europe/Paris'),
                                 locale='fr_FR')
    assert full == (u'dimanche 1 avril 2007 à 17:30:00 heure '
                    u'd\u2019\xe9t\xe9 d\u2019Europe centrale')
    custom = dates.format_datetime(dt, "yyyy.MM.dd G 'at' HH:mm:ss zzz",
                                   tzinfo=timezone('US/Eastern'), locale='en')
    assert custom == u'2007.04.01 AD at 11:30:00 EDT'


def test_format_time():
    t = time(15, 30)
    assert dates.format_time(t, locale='en_US') == u'3:30:00 PM'
    assert dates.format_time(t, format='short', locale='de_DE') == u'15:30'

    assert (dates.format_time(t, "hh 'o''clock' a", locale='en') ==
            u"03 o'clock PM")

    t = datetime(2007, 4, 1, 15, 30)
    tzinfo = timezone('Europe/Paris')
    t = tzinfo.localize(t)
    fr = dates.format_time(t, format='full', tzinfo=tzinfo, locale='fr_FR')
    assert fr == u'15:30:00 heure d\u2019\xe9t\xe9 d\u2019Europe centrale'
    custom = dates.format_time(t, "hh 'o''clock' a, zzzz",
                               tzinfo=timezone('US/Eastern'), locale='en')
    assert custom == u"09 o'clock AM, Eastern Daylight Time"

    t = time(15, 30)
    paris = dates.format_time(t, format='full',
                              tzinfo=timezone('Europe/Paris'), locale='fr_FR')
    assert paris == u'15:30:00 heure normale d\u2019Europe centrale'
    us_east = dates.format_time(t, format='full',
                                tzinfo=timezone('US/Eastern'), locale='en_US')
    assert us_east == u'3:30:00 PM Eastern Standard Time'


def test_format_skeleton():
    dt = datetime(2007, 4, 1, 15, 30)
    assert (dates.format_skeleton('yMEd', dt, locale='en_US') == u'Sun, 4/1/2007')
    assert (dates.format_skeleton('yMEd', dt, locale='th') == u'อา. 1/4/2007')

    assert (dates.format_skeleton('EHm', dt, locale='en') == u'Sun 15:30')
    assert (dates.format_skeleton('EHm', dt, tzinfo=timezone('Asia/Bangkok'), locale='th') == u'อา. 22:30 น.')


def test_format_timedelta():
    assert (dates.format_timedelta(timedelta(weeks=12), locale='en_US')
            == u'3 months')
    assert (dates.format_timedelta(timedelta(seconds=1), locale='es')
            == u'1 segundo')

    assert (dates.format_timedelta(timedelta(hours=3), granularity='day',
                                   locale='en_US')
            == u'1 day')

    assert (dates.format_timedelta(timedelta(hours=23), threshold=0.9,
                                   locale='en_US')
            == u'1 day')
    assert (dates.format_timedelta(timedelta(hours=23), threshold=1.1,
                                   locale='en_US')
            == u'23 hours')


def test_parse_date():
    assert dates.parse_date('4/1/04', locale='en_US') == date(2004, 4, 1)
    assert dates.parse_date('01.04.2004', locale='de_DE') == date(2004, 4, 1)
    assert dates.parse_date('2004-04-01', locale='sv_SE', format='short') == date(2004, 4, 1)


@pytest.mark.parametrize('input, expected', [
    # base case, fully qualified time
    ('15:30:00', time(15, 30)),
    # test digits
    ('15:30', time(15, 30)),
    ('3:30', time(3, 30)),
    ('00:30', time(0, 30)),
    # test am parsing
    ('03:30 am', time(3, 30)),
    ('3:30:21 am', time(3, 30, 21)),
    ('3:30 am', time(3, 30)),
    # test pm parsing
    ('03:30 pm', time(15, 30)),
    ('03:30 pM', time(15, 30)),
    ('03:30 Pm', time(15, 30)),
    ('03:30 PM', time(15, 30)),
    # test hour-only parsing
    ('4 pm', time(16, 0)),
])
def test_parse_time(input, expected):
    assert dates.parse_time(input, locale='en_US') == expected


@pytest.mark.parametrize('case', ['', 'a', 'aaa'])
@pytest.mark.parametrize('func', [dates.parse_date, dates.parse_time])
def test_parse_errors(case, func):
    with pytest.raises(dates.ParseError):
        func(case, locale='en_US')


def test_datetime_format_get_week_number():
    format = dates.DateTimeFormat(date(2006, 1, 8), Locale.parse('de_DE'))
    assert format.get_week_number(6) == 1

    format = dates.DateTimeFormat(date(2006, 1, 8), Locale.parse('en_US'))
    assert format.get_week_number(6) == 2


def test_parse_pattern():
    assert dates.parse_pattern("MMMMd").format == u'%(MMMM)s%(d)s'
    assert (dates.parse_pattern("MMM d, yyyy").format ==
            u'%(MMM)s %(d)s, %(yyyy)s')
    assert (dates.parse_pattern("H:mm' Uhr 'z").format ==
            u'%(H)s:%(mm)s Uhr %(z)s')
    assert dates.parse_pattern("hh' o''clock'").format == u"%(hh)s o'clock"


def test_lithuanian_long_format():
    assert (
        dates.format_date(date(2015, 12, 10), locale='lt_LT', format='long') ==
        u'2015 m. gruodžio 10 d.'
    )


def test_zh_TW_format():
    # Refs GitHub issue #378
    assert dates.format_time(datetime(2016, 4, 8, 12, 34, 56), locale='zh_TW') == u'中午12:34:56'


def test_format_current_moment():
    frozen_instant = datetime.utcnow()
    with freezegun.freeze_time(time_to_freeze=frozen_instant):
        assert dates.format_datetime(locale="en_US") == dates.format_datetime(frozen_instant, locale="en_US")


@pytest.mark.all_locales
def test_no_inherit_metazone_marker_never_in_output(locale):
    # See: https://github.com/python-babel/babel/issues/428
    tz = pytz.timezone('America/Los_Angeles')
    t = tz.localize(datetime(2016, 1, 6, 7))
    assert NO_INHERITANCE_MARKER not in dates.format_time(t, format='long', locale=locale)
    assert NO_INHERITANCE_MARKER not in dates.get_timezone_name(t, width='short', locale=locale)


def test_no_inherit_metazone_formatting():
    # See: https://github.com/python-babel/babel/issues/428
    tz = pytz.timezone('America/Los_Angeles')
    t = tz.localize(datetime(2016, 1, 6, 7))
    assert dates.format_time(t, format='long', locale='en_US') == "7:00:00 AM PST"
    assert dates.format_time(t, format='long', locale='en_GB') == "07:00:00 Pacific Standard Time"
    assert dates.get_timezone_name(t, width='short', locale='en_US') == "PST"
    assert dates.get_timezone_name(t, width='short', locale='en_GB') == "Pacific Standard Time"


def test_russian_week_numbering():
    # See https://github.com/python-babel/babel/issues/485
    v = date(2017, 1, 1)
    assert dates.format_date(v, format='YYYY-ww',locale='ru_RU') == '2016-52'  # This would have returned 2017-01 prior to CLDR 32
    assert dates.format_date(v, format='YYYY-ww',locale='de_DE') == '2016-52'


def test_en_gb_first_weekday():
    assert Locale.parse('en').first_week_day == 0  # Monday in general
    assert Locale.parse('en_US').first_week_day == 6  # Sunday in the US
    assert Locale.parse('en_GB').first_week_day == 0  # Monday in the UK


def test_issue_798():
    assert dates.format_timedelta(timedelta(), format='narrow', locale='es_US') == '0s'
