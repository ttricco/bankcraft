hunger_rate = 0.3 # threshold * 3 * (1/step['day']) 
fatigue_rate = 0.2 # threshold * 3 * (1/step['day'])* 0.5
social_rate = 0.1
consumerism_rate = 0.04
motivation_threshold = 20

steps = {'10min': 1}
steps['hour'] = 6 * steps['10min']
steps['day'] = 24 * 6 * steps['10min'] 
steps['week'] = 7 * 24 * 6 * steps['10min']
steps['biweekly'] = 14 * 24 * 6 * steps['10min']
steps['month'] = 30 * 24 * 6 * steps['10min']
steps['year'] = 365 * 24 * 6 * steps['10min']