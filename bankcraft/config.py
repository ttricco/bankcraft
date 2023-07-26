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


def time_of_the_day(step):
    day_time = step % steps['day']
    if 6*steps['hour'] <= day_time <= 9*steps['hour']:
        return 'breakfast time'
    elif 12*steps['hour'] <= day_time <= 13*steps['hour']:
        return 'lunch time'
    elif 17*steps['hour'] <= day_time <= 20*steps['hour']:
        return 'supper time'
    else:
        return 'None'


def is_weekend(step):
    return (step % (steps['week'])) > (5*steps['day'])


