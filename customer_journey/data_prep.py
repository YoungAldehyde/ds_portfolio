import pandas as pd

data = pd.read_csv('data/customer_events.csv')[['user_id', 'time_install', 'event_name', 'time_event']]

# Start with making sure that time_event and time_insrall are Pandas Datetime types:
data['time_event'] = pd.to_datetime(data['time_event'], unit='s') # Unit = "s" is required here since the raw data format is unique timestamp. Remove this param if your data is already a datetime like data.
data['time_install'] = pd.to_datetime(data['time_install'], unit='s')

# Make sure that there's no event occurring before time_install
data = data[data.time_event >= data.time_install]


# The initial data Pandas DataFrame must have these 4 columns:
# user_id | time_install | event_name | time_event
# - user_id (string): the unique identifier of a user
# - time_install (Pandas datetime): the time when the user installed the app (there should be 1 time_install per user_id)
# - event_name (string): the name of a specific in-app event (there can be many event_name per user_id)
# - time_event (Pandas datetime): the time of each event (there should be 1 time_event per user_id)

# Edit this dataframe so that installs are passed as events

# Create a new DF from the data DF containing only install data
installs = data[['user_id', 'time_install']].sort_values('time_install').drop_duplicates('user_id')

# Create an install column containing dummy "install" events
installs['event_name'] = 'install'

# Create an event_type column to keep the information of install vs other events
installs['event_type'] = 'install'

# Rename time_install to time_event

installs.rename(columns={'time_install': 'time_event'}, inplace=True)

# In the data DF, keep only events data and create the event_type column
data = data[['user_id', 'event_name','time_event']].drop_duplicates()
data['event_type'] = 'in_app_action'

# Concatenate the two DataFrames
data = pd.concat([data, installs[data.columns]])

# Based on the time of events, we can compute the rank of each action at the user_id level:

# a) Sort ascendingly per user_id and time_event
# sort by event_type to make sure installs come first
data.sort_values(['user_id', 'event_type', 'time_event'], ascending=[True, False, True], inplace=True)

# b) Group by user_id
grouped = data.groupby('user_id')

# c) Define a ranking function based on time_event (similar to window function in SQL), using the method = 'first' param to ensure no events have the same rank

def rank(x): return x['time_event'].rank(method='first').astype(int)

# d) Apply the ranking function to the data DF into a new "rank_event" column
data["rank_event"] = grouped.apply(rank).reset_index(0, drop=True)

# Add, each row, the information about the next_event

# a) Regroup by user_id
grouped = data.groupby('user_id')

# b) The shift function allows to access the next row's data. Here, we'll want the event name

def get_next_event(x): return x['event_name'].shift(-1)

# c) Apply the function into a new "next_event" column
data["next_event"] = grouped.apply(lambda x: get_next_event(x)).reset_index(0, drop=True)

# Likewise, we can compute time from each event to its next event:

# a) Regroup by user_id 
grouped = data.groupby('user_id')

# b) We make use one more time of the shift function:

def get_time_diff(
    x): return x['time_event'].shift(-1) - x['time_event']

# c) Apply the function to the data DF into a new "time_to_next" column
data["time_to_next"] = grouped.apply(
    lambda x: get_time_diff(x)).reset_index(0, drop=True)

# Here we'll plot the journey up to the 10th action. This can be achieved by filtering the dataframe based on the rank_event column that we computed:
data = data[data.rank_event < 10]

# Check that you have only installs at rank 1:
data[data['rank_event'] == 1].event_name.unique()