hunger_rate = 1
fatigue_rate = 1
social_rate = 1
motivation_threshold = 20

steps = {'10min': 1}
steps['hour'] = 6 * steps['10min']
steps['day'] = 24 * 6 * steps['10min']
steps['week'] = 7 * 24 * 6 * steps['10min']
steps['biweekly'] = 14 * 24 * 6 * steps['10min']
steps['month'] = 30 * 24 * 6 * steps['10min']
steps['year'] = 365 * 24 * 6 * steps['10min']


def is_weekend(step):
    return (step % (steps['week'])) > (5*steps['day'])


def is_work_hour(step):
    day_time = step % steps['day']
    return (not is_weekend(step)) and (9*steps['hour'] <= day_time <= 12*steps['hour'] or
                                       13*steps['hour'] <= day_time <= 17*steps['hour'])


def is_bed_time(step):
    day_time = step % steps['day']
    return (0 <= day_time <= 6*steps['hour'] or
            22*steps['hour'] <= day_time <= 24*steps['hour'])


def is_weekday_evening(step):
    day_time = step % steps['day']
    return (not is_weekend(step)) and (17 * steps['hour'] < day_time < 22 * steps['hour'])



