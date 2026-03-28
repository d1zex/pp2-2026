from datetime import datetime, timedelta, timezone

def parse_dt(s):
    date_part, tz_part = s.split()
    dt = datetime.strptime(date_part, "%Y-%m-%d")
    
    sign = 1 if tz_part[3] == '+' else -1
    hours, minutes = map(int, tz_part[4:].split(':'))
    
    tz = timezone(timedelta(hours=sign*hours, minutes=sign*minutes))
    return dt.replace(tzinfo=tz)

dt1 = parse_dt(input())
dt2 = parse_dt(input())

utc1 = dt1.astimezone(timezone.utc)
utc2 = dt2.astimezone(timezone.utc)

diff = abs((utc1 - utc2).total_seconds())

print(int(diff // 86400))