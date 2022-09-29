import datetime

dt2 = datetime.datetime(2023, 9, 24, 9, 30, 35)
print(dt2)
res = dt2 + datetime.timedelta(minutes=30)
print(res)