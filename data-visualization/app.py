import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go

import dash 
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = server = app.server

#dataset download link 
link = 'https://raw.githubusercontent.com/yuxuan0702/Summer-Research-Project-/master/data-visualization/final_0921_edited.csv'

# import dataset 
df1 = pd.read_csv('final_0921_edited.csv')
df1.drop(columns=['Unnamed: 0', 'index'], inplace=True)
print(df1.head(3))

#import dataset 
df2 = pd.read_csv('bar_data.csv')
print(df2.head(3))


# introduction card 
first_card = dbc.Card([
    dbc.CardHeader('Basic Information About Research'),
    dbc.CardBody(
        [
            html.P("This Research trying to find factors may related to the university reopenning decisions in the fall. "),
            html.P("From research, we think they gonna be five main factors related to the decisions:"),
            html.P("university information, covid situtaion,economic situation and politic situation"),
            html.P("We trying to keep all our variables in county level to keep all the data indicates in the same level"),
            html.P("So we can analysis without any considers to location level")
        ])])

second_card = dbc.Card([
    dbc.CardHeader('Data Source'),
    dbc.CardBody(
        [
            html.P("Data Comes from different source:"),
            html.P("- Univeristy Information is from Chronicle Higher Education"),
            html.P("- Covid data is mainly from CDC and NY Times Tracker"),
            html.P("- Economic data is from burearu "),
            html.P("- Politic data is from ")
        ]
    )],style={'height':'100%'})

# boxplot
available_indicators = ['2018 Fall Enrollment',
                        'Known_Cases_in_County_per_100k_Residents',
                        'AVG_All_Undergrad_Grant/Scholarship',
                        'AVG_Federal_Student_Loans_Amount',
                        'undergraduate_population',
                        'total_number_faculty',
                        'per_dem',
                        'per_gop',
                        'pi_2014',
                        'Total_Cases',
                        'Percent_of_State_Cases',
                        'Cases_per_100000',
                        'Total_Deaths',
                        'pct_change_gdp_avg',
                        'pct_change_income_avg']


# bar plot
indicators = ['City', 'Rural', 'Suburb', 'Town', 'two_year', 'four_year',
              'No_Housing', 'Yes_Housing', 'Distant', 'Fringe', 'Large', 'Midsize',
              'Remote', 'Small', 'Private', 'Public']

# pie 
labels = ['Online', 'TBD', 'In-Person', 'Hybrid', 'Other']
values = [552, 535, 493, 306, 61]
pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
colors = ['#4C78A8', '#F58518', '#E45756', '#72B7B2', '#54A24B']
pie.update_traces(hole=.4,
                  hoverinfo="label+percent",
                  marker=dict(colors=colors))
pie.update_layout(legend=dict(
    orientation="h",
    yanchor="top",
    xanchor="center",
    x = 0.5,
    y = 1.3),
    margin = dict(l=50, r=30, t=30, b=30))

pie_graph = dbc.Card(
    [
    dbc.CardHeader('University Plan Percentage'),
    dbc.CardBody(
        dcc.Graph(id='pie',figure=pie,responsive = True))
    ])

# sunburst 
sunburst = px.sunburst(df1,
                       path=['Control', 'Plan', 'Housing', 'college_year'],
                       values='college_year',
                       color='Plan',
                       color_discrete_sequence=px.colors.qualitative.T10)

sunburst.update_layout(title_x=0.5,
                        margin = dict(l=50, r=30, t=30, b=30))

sunburst_graph = dbc.Card([
    dbc.CardHeader('Sunburst Graph of University Features'),
    dbc.CardBody(
    dcc.Graph(id = 'sunburst',figure = sunburst,responsive = True))])
    

#map
# map
px.set_mapbox_access_token(
    'pk.eyJ1IjoieXV4dWFuMDgzMCIsImEiOiJja2ZjcmJoeGMxaWR1MnhycXhiejRweHk3In0.EeR8LofkaGjZqQ3itwaWyA')
usamap = px.scatter_mapbox(df1,
                           lat="lat",
                           lon="lng",
                           hover_name="institution",
                           color='Plan',
                           zoom=10,
                           color_discrete_sequence=px.colors.qualitative.T10)

usamap.update_layout(geo_scope='usa',
                     mapbox_zoom=3,
                     mapbox_center={
                         "lat": df1['lat'].mean(),
                         "lon": df1['lng'].mean()
                     },
                     margin={
                         "r": 0,
                         "t": 0,
                         "l": 0,
                         "b": 0
                     })

usamap.update_layout(legend=dict(
    orientation="h", yanchor="top", xanchor="center", x=0.3, y=1.2))

map_graph = dbc.Card([
    dbc.CardHeader('Location Pattern of University Plan'),
    dbc.CardBody(
    dcc.Graph(id = 'map',figure = usamap,responsive = True))],style = {'height':'100%'})

#app layout 
app.layout = html.Div(
[
# Title and Name 
html.Div(dbc.Jumbotron(
        [
            html.H1("School Reopening Decisions Research",
                    style={'textAlign': 'center'}),
            html.Hr(className="my-2"),
            html.P(
                "Led By Bentley Univerisity Students ",
                className="lead",
                style={'textAlign': 'center'})
        ])),
# First Row Introduction, pie and sunburst
html.Div(
    [
dbc.CardDeck([first_card,
              pie_graph,
              sunburst_graph])],style={'padding': 20}),

# second row: text and map 
html.Div([dbc.Row([
            dbc.Col(second_card,width = 4),
            dbc.Col(map_graph,width = 8)   
        ])],style={'padding': 20}),

# third rows variables inspections 
html.Div([
dbc.Row([dbc.Col(
    dbc.Alert(
    [
        html.H4("Variable Inspection", className="alert-heading"),
        html.Hr(className="my-2"),
        html.P("Using barplot and boxplot to inspect the relationship between Plan and other variables"),
],color = 'light'))
])
    ],style={'padding': 20}),

# boxplot and barplot 
html.Div([
        html.Label('Y axis Choose'),
        dcc.Dropdown(id='yaxis-column',
                     options=[{'label': i, 'value': i}
                              for i in available_indicators]
                     ),
        dcc.Graph(id='boxplot-with-checklist')], style={'width': '49%', 'display': 'inline-block','padding': 20}),

html.Div([
        html.Label('Multi-Variables Choose'),
        dcc.Dropdown(id='xaxis-column',
                     options=[{'label': i, 'value': i}
                              for i in indicators], multi=True
                     ),
        dcc.Graph(id='barplot-with-checklist')], style={'width': '49%', 'display': 'inline-block', 'float': 'right','padding': 20}),

# model performance and interpretation 
html.Div([dbc.Row([
    dbc.Col(
    dbc.Alert(
    [
        html.H4("Model Performance and Interpretation", className="heading"),
        html.Hr(className="my-2"),
        html.P("Actual model performance and interpretation"),
],color = 'light'))
])],style={'padding': 20}),
# download button 
html.Div([
    dbc.Button("Data Download", color="primary", outline=True, block = True,href=link)],style={'padding': 20})    
    ],
    style={'padding': 20})

# callback
@app.callback(
    Output('boxplot-with-checklist', 'figure'),
    [Input('yaxis-column', 'value')]
)
# box
def boxgraph(yaxis_column):
    fig = px.box(data_frame=df1,
                 x='Plan',
                 y=yaxis_column,
                 color_discrete_sequence=px.colors.qualitative.T10,
                 title='Box Plot of '+str(yaxis_column))
    return fig

# callback
@app.callback(
    Output('barplot-with-checklist', 'figure'),
    [Input('xaxis-column', 'value')])

def bargraph(xaxis_column):
    figure = px.bar(data_frame=df2,
                    x='Plan',
                    y=xaxis_column,
                    color_discrete_sequence=px.colors.qualitative.T10,
                    title='Bar Plot of '+str(xaxis_column))
    return figure

        

if __name__ == '__main__':
    app.run_server(debug=True)
