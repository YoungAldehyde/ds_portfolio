# Customer Journey Visualization using Plotly - Sankey #

Sankey diagram is a handy visualization tool for displaying multiple types of data over two dimensions, which makes it a great tool to visualize your application or website’s user journey from start to finish. For this implementation, we will need Pandas and [Plotly](https://plotly.com/python/getting-started/?utm_source=mailchimp-jan-2015&utm_medium=email&utm_campaign=generalemail-jan2015&utm_term=bubble-chart) 

We will use the dataset from [this source](https://gist.github.com/nicolasesnis/eb3b35545e97926ab53e0617c5e4b639). For simplicity, this app only contains 4 types of user events: installs, opens, signup and purchase. We can think of these events as an engagement or purchase funnel. As a user must first install the app, and then open it *(obviously, but you never know how many people download the app and never even open it a single time).*

### Here's what the data looks like ###

|       user_id       |    time_install     | event_name |     time_event      |
| :-----------------: | :-----------------: | :--------: | :-----------------: |
| f3049eac4788ffak... | 2020-03-06 05:17:20 |  purchase  | 2020-03-06 05:19:31 |
| 9c1e35e89a3742e1... | 2020-03-06 18:54:48 |   reopen   | 2020-03-06 02:35:06 |
| 723fba1295b9a7fb... | 2020-03-02 00:00:04 |   reopen   | 2020-03-03 13:51:35 |


Note that:
* The nodes of the graph will represent in-app events, starting from install to the $N^{th}$ event
* Every time we see a user completing an event, will link this event to the event of the same user that comes immediately before it

```python

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

```

Plotly's Sankey requires a structure made of two dictionaries: `node` and `link`.

The `link` takes 4 lists as inputs:
*  `source`: a list of each flow's source node. In order to have a source per event, need to append a unique index per event rank to this list.
*  `target`: a list of target nodes. Need to map every source event to its immediate target event.
*  `value`: a list containing each flow's counts.
*  `label` : a list of metadata displayed when hovering over mouse pointer over each link. 

The `node` takes 4 lists as inputs:
*  `label`: a list of nodes names, which is event names in this case.
*  `color`: optional list containing nodes' color info

You can check out [Plotly's docs](https://plotly.com/python/sankey-diagram/) for more details.

Let's create a unique source_index for each event at each step of the journey, while keeping track of every event’s name. The result will be something like below:

```
1: {
    'sources': ['install'], 
    'color': [(80, 190, 151)],
    'sources_index': [0]
  },
2: {
    'sources': ['signup', 'purchase', 'reopen'],
    'color': [(228, 101, 92), (191, 214, 222), (252, 200, 101)],
    'sources_index': [1, 2, 3]
  },
3: {
    'sources': ['reopen', 'purchase', 'signup'],
    'color': [(252, 200, 101), (191, 214, 222), (228, 101, 92)],
    'sources_index': [4, 5, 6]
  }
}
```
Also store a unique source_index instead of event names, because some events may occur multiple times within the journey. Let's also assign a color to each event. Below is the script that does this:

```python
import seaborn as sns

# Working on the nodes_dict

all_events = list(data.event_name.unique())

# Create a set of colors that you'd like to use in your plot.
palette = ['50BE97', 'E4655C', 'FCC865',
           'BFD6DE', '3E5066', '353A3E', 'E6E6E6']
#  Here, I passed the colors as HEX, but we need to pass it as RGB. This loop will convert from HEX to RGB:
for i, col in enumerate(palette):
    palette[i] = tuple(int(col[i:i+2], 16) for i in (0, 2, 4))

# Append a Seaborn complementary palette to your palette in case you did not provide enough colors to style every event
complementary_palette = sns.color_palette(
    "deep", len(all_events) - len(palette))
if len(complementary_palette) > 0:
    palette.extend(complementary_palette)

output = dict()
output.update({'nodes_dict': dict()})

i = 0
for rank_event in data.rank_event.unique(): # For each rank of event...
    # Create a new key equal to the rank...
    output['nodes_dict'].update(
        {rank_event: dict()}
    )
    
    # Look at all the events that were done at this step of the funnel...
    all_events_at_this_rank = data[data.rank_event ==
                                   rank_event].event_name.unique()
    
    # Read the colors for these events and store them in a list...
    rank_palette = []
    for event in all_events_at_this_rank:
        rank_palette.append(palette[list(all_events).index(event)])
    
    # Keep trace of the events' names, colors and indices.
    output['nodes_dict'][rank_event].update(
        {
            'sources': list(all_events_at_this_rank),
            'color': rank_palette,
            'sources_index': list(range(i, i+len(all_events_at_this_rank)))
        }
    )
    # Finally, increment by the length of this rank's available events to make sure next indices will not be chosen from existing ones
    i += len(output['nodes_dict'][rank_event]['sources_index'])
```

Then, we need to count, for each step of the funnel (i.e. each rank_event), how many times each user has gone from a source to a target, and keep track of how long it took, using our time_to_next column. Here again, a Python dict will do the job — we’ll name it links_dict this time. The 1st level keys will be our source indices, and the 2nd level keys the target indices of each flow. The target indices of rank N are retrieved from the source indices of rank N+1.

For every user’s sequence of events, we’ll need to:
1) Read in nodes_dict the unique source_index of every event in the sequence.
2) Likewise, read the source_index of each event’s next event (the target indices of rank N are retrieved from the source indices of rank N+1) and store it into a target_index variable.
3) Check if the combination of the source_index and the target_index is already a key of links_dict. If not, we’ll create it. If it is, we’ll increment the count of unique users, and add the time_to_next information. Later, by dividing the time_to_next by the count of unique users, we’ll have the average time from an event to another.


```python
# Working on the links_dict

output.update({'links_dict': dict()})

# Group the DataFrame by user_id and rank_event
grouped = data.groupby(['user_id', 'rank_event'])

# Define a function to read the souces, targets, values and time from event to next_event:
def update_source_target(user):
    try:
        # user.name[0] is the user's user_id; user.name[1] is the rank of each action
        # 1st we retrieve the source and target's indices from nodes_dict
        source_index = output['nodes_dict'][user.name[1]]['sources_index'][output['nodes_dict']
                                                                           [user.name[1]]['sources'].index(user['event_name'].values[0])]
        target_index = output['nodes_dict'][user.name[1] + 1]['sources_index'][output['nodes_dict']
                                                                               [user.name[1] + 1]['sources'].index(user['next_event'].values[0])]

         # If this source is already in links_dict...
        if source_index in output['links_dict']:
            # ...and if this target is already associated to this source...
            if target_index in output['links_dict'][source_index]:
                # ...then we increment the count of users with this source/target pair by 1, and keep track of the time from source to target
                output['links_dict'][source_index][target_index]['unique_users'] += 1
                output['links_dict'][source_index][target_index]['avg_time_to_next'] += user['time_to_next'].values[0]
            # ...but if the target is not already associated to this source...
            else:
                # ...we create a new key for this target, for this source, and initiate it with 1 user and the time from source to target
                output['links_dict'][source_index].update({target_index:
                                                           dict(
                                                               {'unique_users': 1,
                                                                'avg_time_to_next': user['time_to_next'].values[0]}
                                                           )
                                                           })
        # ...but if this source isn't already available in the links_dict, we create its key and the key of this source's target, and we initiate it with 1 user and the time from source to target
        else:
            output['links_dict'].update({source_index: dict({target_index: dict(
                {'unique_users': 1, 'avg_time_to_next': user['time_to_next'].values[0]})})})
    except Exception as e:
        pass

# Apply the function to your grouped Pandas object:
grouped.apply(lambda user: update_source_target(user)) 
```

And finally, need to create the `targets`, `sources`, `values`, `labels` and `colors` lists from our dictionaries, that will be passed as parameters in the plotting function. This can be achieved easily by iterating over our nodes_dict and links_dict.

```python
targets = []
sources = []
values = []
time_to_next = []

for source_key, source_value in output['links_dict'].items():
    for target_key, target_value in output['links_dict'][source_key].items():
        sources.append(source_key)
        targets.append(target_key)
        values.append(target_value['unique_users'])
        time_to_next.append(str(pd.to_timedelta(
            target_value['avg_time_to_next'] / target_value['unique_users'])).split('.')[0]) # Split to remove the milliseconds information

labels = []
colors = []
for key, value in output['nodes_dict'].items():
    labels = labels + list(output['nodes_dict'][key]['sources'])
    colors = colors + list(output['nodes_dict'][key]['color'])

for idx, color in enumerate(colors):
    colors[idx] = "rgb" + str(color) + ""
```
Everything is now ready and we just have to plot the figure. We can add some styling to the nodes with the line and thickness parameters, and make use of hovertemplate to rephrase the hovering metadata and fit our needs. The update_layout Plotly function allows us to play with the chart’s size, title text, font size and background color.

```python
import plotly.graph_objects as go
import chart_studio.plotly as py
import plotly

fig = go.Figure(data=[go.Sankey(
    node=dict(
        thickness=10,  # default is 20
        line=dict(color="black", width=0.5),
        label=labels,
        color=colors
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        label=time_to_next,
        hovertemplate='%{value} unique users went from %{source.label} to %{target.label}.<br />' +
        '<br />It took them %{label} in average.<extra></extra>',
    ))])

fig.update_layout(autosize=True, title_text="Medium app", font=dict(size=15), plot_bgcolor='white')

publish_to_web = False
if publish_to_web:
   py.iplot(fig, filename='user_journey')
else:
   fig.update_layout(width= 900, height=600)
   fig.show()
```

Here is the final chart:

![demo](images/sankey_demo1.png)