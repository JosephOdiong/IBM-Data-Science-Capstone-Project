### Install packages/commands
# python3.8 -m pip install pandas dash
## Download dataset
# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
## Download the skeleton
# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"
## Run the file
# python3.8 spacex_dash_app.py

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                ],
                                                value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                    100: '100'},
                                    value=[min_payload, max_payload]),



                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[['Launch Site', 'class']][spacex_df['class']==1].groupby('Launch Site', as_index = False).count()
        catg_name = filtered_df['Launch Site'].values.tolist()
        result = filtered_df['class'].values.tolist()
        fig = px.pie(values=result, names=catg_name, title='Total Success Launches by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[['Launch Site', 'class']][spacex_df['Launch Site']==entered_site]
        success_num = filtered_df[filtered_df['class']==1].shape[0]
        failure_num = filtered_df[filtered_df['class']==0].shape[0]
        result = [success_num, failure_num]
        catg_name = ['Success', 'Failure']
        fig_titles = 'Total Success Launches for Site ' + entered_site
        fig = px.pie(values=result, names=catg_name, title=fig_titles)
        return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, entered_payload):
    if entered_site == 'ALL':
        filtered_df = spacex_df[['Payload Mass (kg)', 'class', 'Booster Version Category']]
        fig =  px.scatter(filtered_df, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', range_x=[entered_payload[0], entered_payload[1]])
        fig.update_layout(title='Correlation Between Payload and Success for All Sites', xaxis_title='Payload Mass (kg)', yaxis_title='class')
        return fig
    else:
        filtered_df = spacex_df[['Payload Mass (kg)', 'class', 'Booster Version Category']][spacex_df['Launch Site']==entered_site]
        fig =  px.scatter(filtered_df, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', range_x=[entered_payload[0], entered_payload[1]])
        fig_title = 'Correlation Between Payload and Success for '+ entered_site
        fig.update_layout(title=fig_title , xaxis_title='Payload Mass (kg)', yaxis_title='class')
        return fig




# Run the app
if __name__ == '__main__':
    app.run_server(port = 8050)