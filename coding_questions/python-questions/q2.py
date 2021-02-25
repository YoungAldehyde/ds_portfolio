# Suppose you had a dataset like this. You want to plot and compare growth, but the two platforms are on different scales.
# 
# date app num_users
# 2013-01-02 iphone 1010
# 2013-01-01 iphone 1000
# 2013-01-03 iphone 100
# 2013-01-04 iphone 1050
# ...
# 2013-01-03 web 105
# 2013-01-04 web 10
# 2013-01-02 web 100
# 2013-01-05 web 135
# ...
# 
# You really want a dataset like this. How can you make it?
# 
# date app user_growth
# 2013-01-02 iphone 1.01
# 2013-01-01 iphone 1.00
# 2013-01-03 iphone 0.10
# 2013-01-04 iphone 1.05
# ...
# 2013-01-03 web 1.05
# 2013-01-04 web 0.10
# 2013-01-02 web 1.00
# 2013-01-05 web 1.35
# ...

raw_data = [
    {'date': '2013-01-02', 'app': 'iphone', 'num_users': 1010},
    {'date': '2013-01-01', 'app': 'iphone', 'num_users': 1000},
    {'date': '2013-01-03', 'app': 'iphone', 'num_users': 100},
    {'date': '2013-01-04', 'app': 'iphone', 'num_users': 1050},

    {'date': '2013-01-03', 'app': 'web', 'num_users': 105},
    {'date': '2013-01-04', 'app': 'web', 'num_users': 10},
    {'date': '2013-01-02', 'app': 'web', 'num_users': 100},
    {'date': '2013-01-05', 'app': 'web', 'num_users': 135},
]

# Answer
def normalize_daily(lst = None):
    
    rslt = []

    unique_apps = set([i['app'] for i in lst])

    for app in unique_apps:
        daily_data = [x for x in raw_data if x['app'] == app]
        min_date = min([x['date'] for x in daily_data])
        min_date_num_users = [x for x in daily_data if x['date'] == min_date][0]['num_users']
        
        for day in daily_data:
            day['user_growth'] = day['num_users']/min_date_num_users
        rslt.append(daily_data)
        # print("App Name: ", app)
        # print(daily_data)
        # print('\n')       
    return rslt

# test
print(normalize_daily(raw_data))    