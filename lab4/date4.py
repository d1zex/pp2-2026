from datetime import datetime

date1 = datetime(2025, 7, 1)
date2 = datetime(2025, 9, 24)

difference = date2 - date1
difference_in_seconds = difference.total_seconds()

print("Difference in seconds:", difference_in_seconds)