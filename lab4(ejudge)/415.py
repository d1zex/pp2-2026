from datetime import datetime, timedelta, timezone

def parse_dt(s):
    date_part, tz_part = s.split()
    dt = datetime.strptime(date_part, "%Y-%m-%d")
    sign = 1 if tz_part[3] == '+' else -1
    hours, minutes = map(int, tz_part[4:].split(':'))
    tz = timezone(timedelta(hours=sign*hours, minutes=sign*minutes))
    dt = dt.replace(tzinfo=tz)
    return dt

def next_birthday(birth, current):
    year = current.year
    month, day = birth.month, birth.day
    # handle Feb 29
    if month == 2 and day == 29:
        try:
            target = datetime(year, 2, 29, tzinfo=birth.tzinfo)
        except ValueError:
            target = datetime(year, 2, 28, tzinfo=birth.tzinfo)
    else:
        target = datetime(year, month, day, tzinfo=birth.tzinfo)
    # convert to UTC for comparison
    target_utc = target.astimezone(timezone.utc)
    current_utc = current.astimezone(timezone.utc)
    if target_utc < current_utc:
        year += 1
        if month == 2 and day == 29:
            try:
                target = datetime(year, 2, 29, tzinfo=birth.tzinfo)
            except ValueError:
                target = datetime(year, 2, 28, tzinfo=birth.tzinfo)
        else:
            target = datetime(year, month, day, tzinfo=birth.tzinfo)
        target_utc = target.astimezone(timezone.utc)
    delta = target_utc - current_utc
    return delta.days

birth = parse_dt(input())
current = parse_dt(input())
print(next_birthday(birth, current))
