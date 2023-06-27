

class TimeStep:
    steps = {'10min': 1}
    steps['hour'] = 6 * steps['10min']
    steps['day'] = 24 * 6 * steps['10min']
    steps['week'] = 7 * 24 * 6 * steps['10min']
    steps['biweek'] = 14 * 24 * 6 * steps['10min']
    steps['month'] = 30 * 24 * 6 * steps['10min']
    steps['year'] = 365 * 24 * 6 * steps['10min']

    def __init__(self):
        pass
