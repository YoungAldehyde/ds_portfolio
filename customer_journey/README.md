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
