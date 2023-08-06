from datetime import datetime, timedelta
import pytz

def utcnow() -> datetime:
    '''returns the aware datetime object'''
    return pytz.timezone('UTC').localize(datetime.utcnow())

def aware(naive='now', tz='UTC'):
    '''accepts a tuple, list, timestamp (s, ms, us or ns) aware or naive datetime
    returns tz aware datetime.
    naive datetimes are considered UTC
    Lists and tuples are only accepted in UTC and can be converted to TZ
    Aware datetimes will be CONVERTED to TZ'''
    if naive in [None, 'now']:
        return utcnow().astimezone(pytz.timezone(tz))
    elif isinstance(naive,(tuple, list)):
        return pytz.timezone('UTC').localize(datetime(*naive)).astimezone(pytz.timezone(tz))
    elif isinstance(naive,(int, float)):
        if naive > 1e17:
            naive = naive/1e9
        elif naive > 1e14:
            naive = naive/1e6
        elif naive > 1e11:
            naive = naive/1e3
        return pytz.timezone('UTC').localize(datetime.utcfromtimestamp(naive)).astimezone(pytz.timezone(tz))
        
    elif isinstance(naive, (datetime)):
        if naive.tzinfo is None or naive.tzinfo.utcoffset(naive) is None:
            return pytz.timezone('UTC').localize(naive).astimezone(pytz.timezone(tz))
        else:
            return naive.astimezone(pytz.timezone(tz))

def my_sql_dt_format(dt='now'):
    """
    accepts the same params as aware
    gets the aware datetime
    transformes it into UTC
    returns the dtstring in the fomat necessary for the mysql datetime object
    """
    dt = aware(dt)
    return dt.strftime('%Y-%m-%d %H:%M:%S')
    

if __name__ == '__main__':
    print(my_sql_dt_format())