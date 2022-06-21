from tokenize import group
from dash import Dash, html, dcc, Input, Output
from matplotlib.axis import YAxis
from matplotlib.pyplot import xlabel, ylabel
import plotly.express as px
import pandas as pd

from datetime import date

app = Dash(__name__)

colors = {
    'background': '#142341',
    'text': '#7FDBFF'
}
# layout describes what the applications looks like

data = pd.read_csv('datasets/hotel_bookings.csv')

data['full_date'] = pd.to_datetime(data['arrival_date_year'].astype(str) + ' ' + data['arrival_date_month'].astype(str) + ' ' + data['arrival_date_day_of_month'].astype(str) )

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

app.layout = html.Div(children=[
    html.H1(
        children='Hotel booking Dashboard info',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    dcc.Graph(
        id='examle-graph'
    ),

    html.Div(children=[dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=data['full_date'].min(),
        max_date_allowed=data['full_date'].max(),
        initial_visible_month=data['full_date'].max(),
        start_date=data['full_date'].min(),
        end_date=data['full_date'].max()
    )])],
    
    style={
            'textAlign': 'center',
            'color': colors['text']
        }
)


@app.callback(
    Output('examle-graph', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):

    df1 = data[(data['full_date'] >= pd.to_datetime(start_date)) & (data['full_date'] <= pd.to_datetime(end_date))]

    
    df1 = df1.groupby(['arrival_date_month', 'hotel'], as_index=False).agg({'arrival_date_year': 'count'})

    df1['csort'] = df1.arrival_date_month.astype('category')

    df1.csort.cat.set_categories(calendar, inplace=True)

    df1.sort_values(["csort"], inplace=True)

    df1.columns = ['arrival_date_month', 'hotel', 'counter', 'sorter']

    fig = px.histogram(df1, x='arrival_date_month', y='counter', color='hotel', barmode='group', text_auto=True)

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        title_text='Graph #1', # title of plot
        xaxis_title_text='Month of arrival', # xaxis label
        yaxis_title_text='Number of reservations', # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1 # gap between bars of the same location coordinates
    )

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)