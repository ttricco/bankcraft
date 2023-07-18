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