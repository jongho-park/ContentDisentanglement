import datetime
import dateutil.tz
import platform
import time


_TAG = None
_T_START = None


def get_timestamp(tz=False):
    now = datetime.datetime.now(dateutil.tz.tzlocal())
    ts_format = '%Y-%m-%d %H:%M:%S'
    if platform.system() != 'Linux':
        ts_format = ts_format.replace(':', '-').replace(' ', '-')
    if tz:
        ts_format += ' %Z'
    timestamp = now.strftime(ts_format)
    return timestamp


def reset_timer():
    global _T_START
    _T_START = time.time()


def set_tag(tag):
    global _TAG
    _TAG = tag


def tprint(text):
    msg = '[' if _TAG is None else '[{} | '.format(_TAG)
    if _T_START is None:
        timestamp = get_timestamp(tz=False)
        msg += '{}] {}'.format(timestamp, text)
    else:
        t_elapsed = time.time() - _T_START
        m, s = divmod(int(t_elapsed), 60)
        h, m = divmod(m, 60)
        if h > 0:
            msg += '{}h '.format(h)
        msg += '{:02d}m {:02d}s] {}'.format(m, s, text)
    print(msg)

