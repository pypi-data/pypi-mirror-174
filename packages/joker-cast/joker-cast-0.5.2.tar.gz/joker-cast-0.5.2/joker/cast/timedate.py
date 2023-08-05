#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import collections
import datetime
import functools
import math
import re
import sys
import time
from datetime import timedelta
from typing import NamedTuple

from joker.cast import want_unicode

_sexagesimal_chars = '0123456789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyY'
_sexagesimal_remap = {ic[1]: ic[0] for ic in enumerate(_sexagesimal_chars)}


def sexagesimal_format(num, precision=0):
    from joker.cast.numeric import numsys_cast

    idigits, fdigits = numsys_cast(num, 60, precision)
    rs = ''.join(_sexagesimal_chars[i] for i in idigits) or '0'

    if isinstance(num, int) and not precision:
        return rs
    return rs + '.' + ''.join(_sexagesimal_chars[i] for i in fdigits)


def sexagesimal_parse(numstr):
    from joker.cast.numeric import numsys_revcast

    if '.' not in numstr:
        digits = [_sexagesimal_remap[c] for c in numstr]
        return numsys_revcast(60, digits, [])

    parts = numstr.split('.', 1)
    idigits = [_sexagesimal_remap[c] for c in parts[0]]
    fdigits = [_sexagesimal_remap[c] for c in parts[1]]
    return numsys_revcast(60, idigits, fdigits or [0])


def start_of_this_year() -> datetime.datetime:
    today = datetime.date.today()
    return datetime.datetime(today.year, 1, 1)


def start_of_this_month() -> datetime.datetime:
    today = datetime.date.today()
    return datetime.datetime(today.year, today.month, 1)


def start_of_today() -> datetime.datetime:
    today = datetime.date.today()
    return datetime.datetime(today.year, today.month, today.day)


def seconds_to_hms(seconds):
    """
    >>> seconds_to_hms(4000)
    (1, 6, 40)
    :return:
    """
    # https://stackoverflow.com/a/775075/2925169
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return h, m, s


def _smart_time_parse(s):
    """
    :param s: (str)
    :return:  [seconds, minutes, hours]
    """
    if ':' in s:
        parts = [float(x or 0) for x in s.split(':')][:3]
        parts.reverse()
        # len(parts) must be 2 or 3
        if len(parts) == 2:
            parts.append(0)
    else:
        sc = s
        parts = []
        for _ in range(3):
            parts.append(int(sc[-2:] or 0))
            sc = sc[:-2]
    return parts


def smart_time_parse(s):
    sec, m, h = _smart_time_parse(s)
    return datetime.time(h, m, sec)


def smart_time_parse_to_seconds(s):
    """
    >>> smart_time_parse_to_seconds('2:3')  # 1min 2sec
    123
    >>> smart_time_parse_to_seconds('1:1:2')  # 1hour 1min 2sec
    3662
    >>> smart_time_parse_to_seconds('1::2')  # 1hour 2sec
    3602
    >>> smart_time_parse_to_seconds('1::')  # 1hour
    3600
    >>> smart_time_parse_to_seconds('10102')  # 1hour 1min 2sec
    3662
    >>> smart_time_parse_to_seconds('200')  # 2min
    120
    :param s: a string representing time
    :return:
    """
    seconds = 0
    for i, x in enumerate(_smart_time_parse(s)):
        seconds += x * 60 ** i
    return seconds


parse_time_to_seconds = smart_time_parse_to_seconds


def smart_time_parse_to_timedelta(s):
    seconds = smart_time_parse_to_seconds(s)
    return datetime.timedelta(seconds=seconds)


def smart_date_parse(s):
    """  
    >>> smart_date_parse(0)
    datetime.date(2017, 5, 5) 
    >>> smart_date_parse('today')
    datetime.date(2017, 5, 5) 
    
    >>> smart_date_parse(-1)
    datetime.date(2017, 5, 4) 
    >>> smart_date_parse('yesterday')
    datetime.date(2017, 5, 4)
    
    >>> smart_date_parse(1)
    datetime.date(2017, 5, 6) 
    >>> smart_date_parse('tomorrow')
    datetime.date(2017, 5, 6) 
    
    >>> smart_date_parse(datetime.date.today())
    datetime.date(2017, 5, 5) 
    >>> smart_date_parse(datetime.datetime.now())
    datetime.date(2017, 5, 5) 
    
    >>> smart_date_parse('20170505')
    datetime.date(2017, 5, 5) 
    >>> smart_date_parse('2017-05-06')
    datetime.date(2017, 5, 6) 
    >>> smart_date_parse('05-06')
    datetime.date(2017, 5, 6) 
    >>> smart_date_parse('0506')
    datetime.date(2017, 5, 6) 
    
    :param s: a string representing a date
    :return: a datetime.date instance
    """
    day = datetime.timedelta(days=1)
    today = datetime.date.today()
    if isinstance(s, int):
        return today + s * day
    elif isinstance(s, datetime.date):
        return s
    elif isinstance(s, datetime.datetime):
        return s.date()
    elif isinstance(s, str):
        s = want_unicode(s).lower()
    else:
        t = s.__class__.__name__
        raise TypeError('cannot convert type {} to date'.format(t))

    if s == 'today':
        return smart_date_parse(0)
    if s == 'yesterday':
        return smart_date_parse(-1)
    if s == 'tomorrow':
        return smart_date_parse(1)

    if re.match(r'\d{8}$', s):
        return datetime.datetime.strptime(s, '%Y%m%d').date()

    if re.match(r'\d{4}$', s):
        s = '{}{}'.format(today.year, s)
        return datetime.datetime.strptime(s, '%Y%m%d').date()

    if re.match(r'\d{4}-\d{1,2}-\d{1,2}$', s):
        return datetime.datetime.strptime(s, '%Y-%m-%d').date()

    if re.match(r'\d{1,2}-\d{1,2}$', s):
        s = '{}-{}'.format(today.year, s)
        return datetime.datetime.strptime(s, '%Y-%m-%d').date()
    raise ValueError('unknow date format')


easy_date = smart_date_parse


def time_format(fmt=None, tm=None):
    if fmt is None:
        fmt = '%y%m%d-%H%M%S'
    if tm is None:
        tm = datetime.datetime.now()
    return tm.strftime(fmt)


def date_range(start, stop=0, step=1):
    """
    >>> list(date_range(-3, 0))  # last 3 days
    [datetime.date(2017, 5, 2),
     datetime.date(2017, 5, 3),
     datetime.date(2017, 5, 4)]
     
    :param start: 
    :param stop: 
    :param step: 
    :return: 
    """
    start = smart_date_parse(start)
    stop = smart_date_parse(stop)
    delta = datetime.timedelta(days=step)
    while (start - stop).total_seconds() * step < 0:
        yield start
        start += delta


class Timer:
    def __init__(self, name: str = '', offset: float = 0.):
        self.name = name
        self.started_at = time.time() + offset
        self.entered_at = None

    def __repr__(self):
        parts = self.__class__.__name__, repr(self.name), -self.seconds
        return '{}({}, {})'.format(*parts)

    def __str__(self):
        tmr = 'Timer {}'.format(self.name).strip()
        if self.entered_at is None:
            return '{}: {}'.format(tmr, self.seconds)
        since_entering = round(time.time() - self.entered_at, 3)
        return '{}: {}, {}'.format(tmr, self.seconds, since_entering)

    def __enter__(self):
        self.entered_at = time.time()
        return self

    def __exit__(self, typ, value, traceback):
        print(self, file=sys.stderr)
        self.entered_at = None

    @property
    def seconds(self):
        diff = time.time() - self.started_at
        return round(diff, 3)

    def as_json_serializable(self):
        return self.seconds


def timed(func):
    """A decorator reporting execution time"""

    @functools.wraps(func)
    def retfunc(*args, **kwargs):
        name = getattr(func, '__name__', None) or func.__class__.__name__
        with Timer(name + '()'):
            return func(*args, **kwargs)

    return retfunc


class TimeMachine(object):
    def __init__(self, start=None, speed=None):
        self._initpoint = datetime.datetime.now()
        self._imaginary = not (start or speed)
        self._start = start or self._initpoint
        self._speed = speed or 1.

    def now(self):
        if not self._imaginary:
            return datetime.datetime.now()
        delta = datetime.datetime.now() - self._initpoint
        return self._start + delta * self._speed

    @staticmethod
    def convert_time_to_timedelta(t):
        return datetime.timedelta(
            hours=t.hour, minutes=t.minute, seconds=t.second,
            microseconds=t.microsecond
        )


class TimeSlicer(TimeMachine):
    EPOCH = datetime.datetime(1970, 1, 1)

    def __init__(self, start=None, speed=None, ts_size=600):
        super(TimeSlicer, self).__init__(start, speed)
        self._ts_delta = datetime.timedelta(seconds=ts_size)

    def get_current_timeslice(self, relative=True):
        dt = self.now()
        return self.convert_datetime_to_timeslice(dt, relative=relative)

    @staticmethod
    def guess_slice_size(ts):
        """
        assuming slice size a multiple of 60
        :param ts:
        :return:
        """
        t = time.time()
        return int(round(t / ts / 60.)) * 60

    def convert_timeslice_to_time(self, ts):
        dt = self.EPOCH + self._ts_delta * ts
        return dt.time()

    def convert_timeslice_to_datetime(self, ts, relative=True):
        """
        If relative is true, given ts is considered relative to
        00:00:00 of today.

        :param ts: an integer, serial number of timeslice
        :param relative: bool
        :return: a datetime instance
        """
        if not relative:
            return self.EPOCH + self._ts_delta * ts
        d = self.now().date()
        t = self.convert_timeslice_to_time(ts)
        return datetime.datetime.combine(d, t)

    def convert_time_to_timeslice(self, t):
        delta = self.convert_time_to_timedelta(t)
        # use .total_seconds to be compat with python 2.x
        return int(delta.total_seconds() / self._ts_delta.total_seconds())

    def convert_datetime_to_timeslice(self, dt, relative=True):
        if relative:
            return self.convert_time_to_timeslice(dt.time())
        delta = dt - self.EPOCH
        # use .total_seconds to be compat with python 2.x
        return int(delta.total_seconds() / self._ts_delta.total_seconds())


class Year(object):
    __slots__ = ['val']

    def __init__(self, num, trad=True):
        # 0 => 1 AD, 1 => 1 AD, -1 => 1 BC
        self.val = num + 1 if trad and num < 1 else num

    def __repr__(self):
        c = self.__class__.__name__
        v = self.val
        num = self.val - 1 if self.val < 1 else self.val
        return '{}({})'.format(c, num)

    def __str__(self):
        if self.val > 0:
            return str(self.val)
        return '{} BC'.format(1 - self.val)

    def __sub__(self, other):
        if isinstance(other, Year):
            return self.val - other.val
        if isinstance(other, int):
            return Year(self.val - other, trad=False)
        return NotImplemented

    def __isub__(self, other):
        if isinstance(other, int):
            self.val -= other
            return self
        raise TypeError('unsupported operation')

    def __add__(self, other):
        if isinstance(other, int):
            return Year(self.val + other, trad=False)
        raise TypeError('unsupported operation')

    def __iadd__(self, other):
        if isinstance(other, int):
            self.val += other
            return self
        raise TypeError('unsupported operation')

    def __eq__(self, other):
        return self.val == other.val

    @classmethod
    def parse(cls, s):
        try:
            return cls(int(s))
        except ValueError:
            pass
        parts = re.split(r'(\d+)', s)
        if parts[0] and parts[-1]:
            raise ValueError("bad format: '{}'".format(s))
        affix = parts[0] or parts[-1]
        affix = affix.strip()
        if affix.upper() in {'BC', 'B.C.', 'BCE', 'B.C.E.'}:
            return cls(-int(parts[1]))
        if affix.upper() in {'AD', 'A.D.', 'CE', 'C.E.'}:
            return cls(int(parts[1]))
        raise ValueError("bad token: '{}'".format(affix))


def _n_minutes_floor(n: int, dt: datetime.datetime):
    minutes = math.floor(dt.minute / n) * n
    return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, minutes)


def _n_minutes_ceil(n: int, dt: datetime.datetime):
    dti = datetime.datetime(dt.year, dt.month, dt.day, dt.hour)
    # minutes can be 60
    minutes = math.ceil(dt.minute / n + dt.second / 60. / n) * n
    return dti + timedelta(minutes=minutes)


def quarter_floor(dt: datetime.datetime):
    return _n_minutes_floor(15, dt)


def quarter_ceil(dt: datetime.datetime):
    return _n_minutes_ceil(15, dt)


def quintminute_floor(dt: datetime.datetime):
    return _n_minutes_floor(5, dt)


def quintminute_ceil(dt: datetime.datetime):
    return _n_minutes_ceil(5, dt)


class TimeSpan(NamedTuple):
    a: datetime.datetime
    b: datetime.datetime

    @classmethod
    def from_timestamps(cls, a: float, b: float):
        return cls(
            datetime.datetime.fromtimestamp(a),
            datetime.datetime.fromtimestamp(b)
        )

    @property
    def duration(self):
        delta = self.b - self.a
        return delta.total_seconds()

    def __contains__(self, v: datetime.datetime) -> bool:
        return self.a <= v <= self.b

    @property
    def as_dict(self):
        return {'a': self.a, 'b': self.b}

    @property
    def as_json_serializable(self):
        return {
            'a': self.a.strftime("%Y-%m-%d %H:%M:%S"),
            'b': self.b.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @property
    def as_mongo_filter(self):
        return {'$gte': self.a, '$lte': self.b}

    @property
    def as_timestamps(self):
        return self.a.timestamp(), self.b.timestamp()

    def fmt_for_human(self):
        if self.a.date() == self.b.date():
            return f'{self.a:%Y-%m-%d %H:%M:%S} ~ {self.b:%H:%M:%S}'
        return f'{self.a:%Y-%m-%d %H:%M:%S} ~ {self.b:%Y-%m-%d %H:%M:%S}'

    def expand(self, a_seconds: int, b_seconds: int = None):
        if b_seconds is None:
            b_seconds = a_seconds
        a_delta = timedelta(seconds=a_seconds)
        b_delta = timedelta(seconds=b_seconds)
        return TimeSpan(self.a - a_delta, self.b + b_delta)

    def expand_to_quarters(self):
        return TimeSpan(quarter_floor(self.a), quarter_ceil(self.b))

    def expand_to_quintminutes(self):
        return TimeSpan(quintminute_floor(self.a), quintminute_ceil(self.b))

    def iter_quarter_time_spans(self):
        whole = self.expand_to_quarters()
        queue = collections.deque([whole.a], maxlen=2)
        delta = timedelta(minutes=15)
        while queue[-1] < whole.b:
            queue.append(queue[-1] + delta)
            yield TimeSpan(*queue)

    def iter_quintminute_time_spans(self):
        whole = self.expand_to_quarters()
        queue = collections.deque([whole.a], maxlen=2)
        delta = timedelta(minutes=5)
        while queue[-1] < whole.b:
            queue.append(queue[-1] + delta)
            yield TimeSpan(*queue)
