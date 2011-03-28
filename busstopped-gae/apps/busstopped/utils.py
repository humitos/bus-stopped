import pytz
import datetime


def now_time():
    # This is an horrible hack because GAE saves time object in 01/01/1970
    now_time = datetime.datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
    now_1970 = datetime.datetime(1970, 1, 1, now_time.hour, now_time.minute, 0)

    # Testing
    # now_1970 = datetime.datetime(1970, 1, 1, 23, 45, 0)

    return now_1970

def get_weekday_display():
    now = datetime.datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
    date = now.date()
    weekday = date.weekday()

    # This import MUST be here because if we put this at the top
    # a circular import is created between models.py and utils.py
    from models import Holiday

    # Check if today is declarated as Holiday and use that times
    holiday = Holiday.all()
    holiday.filter('date =', date)
    if holiday.count():
        return holiday[0].time_days

    # Testing
    # weekday = 6
    if weekday == 5:
        weekday = 'Sabados'
    elif weekday == 6:
        weekday = 'Domingos'
    else:
        weekday = 'Habiles'
    return weekday
