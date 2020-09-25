import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)
server = app.server

# import dataset 
df1 = pd.read_csv('final_0921_edited.csv')
df1.drop(columns  = ['Unnamed: 0','index'],inplace = True)
print(df1.head(3))
df2 = pd.read_csv('bar_data.csv')
print(df2.head(3))

# markddown text 
markdown_text = '''
## Reopening Project 
This is the Dashboard for Research Project of Reopening decision by univeristy this fall 
'''

# pie chart 
labels = ['Online','TBD','In-Person','Hybrid','Other']
values = [552,535,493,306,61]
pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
pie.update_traces(hole=.4, hoverinfo="label+percent")

# sunburst 
sunburst = px.sunburst(df1,
                  path=['Control', 'Plan', 'Housing', 'college_year'],
                  values='college_year',
                  color='Plan')

#map 
px.set_mapbox_access_token('pk.eyJ1IjoieXV4dWFuMDgzMCIsImEiOiJja2ZjcmJoeGMxaWR1MnhycXhiejRweHk3In0.EeR8LofkaGjZqQ3itwaWyA')
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
                  height=400,
                  margin={
                      "r": 0,
                      "t": 30,
                      "l": 0,
                      "b": 0
                  })

usamap.update_layout(legend=dict(
    orientation="h", yanchor="bottom", xanchor="center", x=0.3, y=1))

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

#app layout 
app.layout = html.Div([
     dcc.Markdown(children=markdown_text),
     
     html.Div(children=[
     html.H2(children='Pie Chart of University Plan',style = {'textAlign':'center'}),

    dcc.Graph(
        id='pie',
        figure=pie
    )
],style={'width': '49%', 'display': 'inline-block'}),
     
     html.Div(children=[
     html.H2(children='Sunburst Chart of University Plan',style = {'textAlign':'center'}),

    dcc.Graph(
        id='sunburst',
        figure=sunburst
    )
], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),     
     
     html.Div(children=[
     html.H2(children='School Reopening Decision',style = {'textAlign':'center'}),

    dcc.Graph(
        id='map',
        figure=usamap
    )
]),
  html.Div([
            html.Label('Y axis Choose'),
            dcc.Dropdown(id='yaxis-column',
                    options=[{'label': i, 'value': i}
                                for i in available_indicators]
                ),
            dcc.Graph(id = 'boxplot-with-checklist')],style={'width': '49%', 'display': 'inline-block'}),
            html.Div([
            html.Label('Multi-Variables Choose'),
            dcc.Dropdown(id='xaxis-column',
                    options=[{'label': i, 'value': i}
                                for i in indicators],multi=True
                ),
            dcc.Graph(id = 'barplot-with-checklist')],style={'width': '49%', 'display': 'inline-block','float':'right'})

])


# callback 
@app.callback(
    Output('boxplot-with-checklist','figure'),
    [Input('yaxis-column','value')]
)

#box 
def boxgraph(yaxis_column):
    fig = px.box(data_frame=df1,
                         x = 'Plan',
                         y = yaxis_column,
                         color_discrete_sequence=px.colors.qualitative.T10,
                         title = 'Box Plot of '+str(yaxis_column))  
    return fig

# callback 
@app.callback(
    Output('barplot-with-checklist','figure'),
    [Input('xaxis-column','value')])

def bargraph(xaxis_column):
    figure = px.bar(data_frame=df2,
                         x = 'Plan',
                         y = xaxis_column,
                         color_discrete_sequence=px.colors.qualitative.T10,
                         title = 'Bar Plot of '+str(xaxis_column))  
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)


