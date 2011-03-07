import pytz
import datetime

def now_time():
    # This is a horrible hack because GAE saves time object in 01/01/1970
    now_time = datetime.datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
    now_1970 = datetime.datetime(1970, 1, 1, now_time.hour, now_time.minute, 0)
    return now_1970

def get_weekday_display():
    weekday = datetime.datetime.now(pytz.timezone('America/Argentina/Buenos_Aires')).date().weekday()
    # Testing
    # weekday = 6
    if weekday == 5:
        weekday = 'Sabados'
    elif weekday == 6:
        weekday = 'Domingos'
    else:
        weekday = 'Habiles'
    return weekday
