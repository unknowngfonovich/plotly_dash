from dash import Dash, html, dcc
from matplotlib.axis import YAxis
from matplotlib.pyplot import xlabel, ylabel
import plotly.express as px
import pandas as pd

app = Dash(__name__)

colors = {
    'background': '#142341',
    'text': '#7FDBFF'
}
# layout describes what the applications looks like

data = pd.read_csv('datasets/hotel_bookings.csv')
calendar = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
]

df1 = data.groupby(['arrival_date_month', 'hotel'], as_index=False).agg({'arrival_date_year': 'count'}).set_index('arrival_date_month').loc[calendar].reset_index()
df1.columns = ['arrival_date_month', 'hotel', 'counter']

fig = px.histogram(df1, x='arrival_date_month', y='counter', color='hotel', ylabel='Number of bookings', xlabel='Month of arrival')


fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
)

app.layout = html.Div(children=[
    html.H1(
        children='Hotel booking',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    dcc.Graph(
        id='examle-graph',
        figure=fig,
    )],
    style={
            'textAlign': 'center',
            'color': colors['text']
        }
)

if __name__ == '__main__':
    app.run_server(debug=True)