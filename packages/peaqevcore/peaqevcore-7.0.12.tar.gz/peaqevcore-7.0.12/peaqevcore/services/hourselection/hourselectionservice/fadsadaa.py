import datetime



date_time_str = '2022-10-30T00:00:00+02:00'
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%f')


'2022-10-30T01:00:00+02:00'

