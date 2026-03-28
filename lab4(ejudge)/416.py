from datetime import datetime, timedelta, timezone

def parse_dt(s):
    dt_part, tz_part = s.rsplit(' ', 1)
    dt = datetime.strptime(dt_part, "%Y-%m-%d %H:%M:%S")
    sign = 1 if tz_part[3] == '+' else -1
    hours, minutes = map(int, tz_part[4:].split(':'))
    tz = timezone(timedelta(hours=sign*hours, minutes=sign*minutes))
    dt = dt.replace(tzinfo=tz)
    return dt

start = parse_dt(input())
end = parse_dt(input())

duration = int((end.astimezone(timezone.utc) - start.astimezone(timezone.utc)).total_seconds())
print(duration)
