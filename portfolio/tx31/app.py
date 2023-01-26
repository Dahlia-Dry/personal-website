"""
Campaign Data Dashboard
Dahlia Dry | Bluebonnet Data | Donna Imam for TX31 | 2020
Dash app visualizer for data mapped by precinct/zipcode
Usage: Refer to README.md, see requirements.txt for dependencies
"""
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd
import numpy as np
import json
import plotly.graph_objects as go
from utilities import *
import dash_auth
from plotly.subplots import make_subplots
import textwrap
import os
import time

#Uncomment the following block if you want to password protect
#Create a credentials txt file in private location with username on first line, pass on second line
#Set filepath to credentials file as path_to_creds
"""
path_to_creds = 'user.txt'
user_secret = open(path_to_creds,'r')
user = user_secret.readline().replace('\n','')
password = user_secret.readline().replace('\n','')
VALID_USERNAME_PASSWORD_PAIRS ={user:password}
"""
#**IMPORTANT SET VALUES HERE***************************************************
resultscatalog = pd.read_csv('catalogs/election_results.csv')
targetingcatalog = pd.read_csv('catalogs/targeting.csv')
pctgeopath ="geometry/json/geojson-precincts.json"
zipgeopath ="geometry/json/geojson-zips.json"
#******************************************************************************
#Initialize Data Params
election_results_zip = []
election_results_prec =resultscatalog['title'].tolist()
target_metrics =targetingcatalog['title'].tolist()
graphvars = [election_results_prec[0],election_results_prec[-1]] #just set starting defaults
#_______________________________________________________________________________
#Initialize Dash stuff__________________________________________________________
suppress_callback_exceptions=True #hide annoying stuff, set False to debug
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
"""auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)"""
server = app.server
#_______________________________________________________________________________
#Initialize sort scores for targeting___________________________________________
startermetrics =target_metrics[:3] #just set starting defaults
weights = [1 for i in range(len(startermetrics))] #just set starting defaults
sorted = calc_targetscore(startermetrics,weights,targetingcatalog)
sorted = sorted[['PrecinctKey','score','City']]
#_______________________________________________________________________________
#Initialize Chloropleths
fastload = False #set as True if you're finding the page loads too slowly
if fastload:
    fig = go.Figure()
    fig2 = go.Figure()
    targetfig = go.Figure()
else:
    merged = aggregate('Precincts', election_results_prec[0],resultscatalog)
    with open(pctgeopath) as geofile:
        j_file = json.load(geofile)
    df = merged[['PrecinctKey',election_results_prec[0]]]
    fig = go.Figure(data=go.Choropleth(
        locations= df['PrecinctKey'],
        colorbar={"len": 0.7,"x": 0,"y": 0.5,
                    'title': {"text": election_results_prec[0], "side": "top"}},
        geojson = j_file,
        featureidkey = 'properties.PCTKEY', # Spatial coordinates
        z = df[election_results_prec[0]], # Data to be color-coded
        colorscale = 'Teal',
        hoverinfo='location+z',
        hovertemplate="PrecinctKey: %{location} | Value: %{z}<extra></extra>"
    ))
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    merged2 = aggregate('Precincts', election_results_prec[-1],resultscatalog)
    with open(pctgeopath) as geofile:
        j_file = json.load(geofile)
    df = merged2[['PrecinctKey',election_results_prec[-1]]]
    fig2 = go.Figure(data=go.Choropleth(
        locations= df['PrecinctKey'],
        colorbar={"len": 0.7,"x": 0,"y": 0.5,
                    'title': {"text": election_results_prec[-1], "side": "top"}},
        geojson = j_file,
        featureidkey = 'properties.PCTKEY', # Spatial coordinates
        z = df[election_results_prec[-1]], # Data to be color-coded
        colorscale = 'Burg',
        hoverinfo='location+z',
        hovertemplate="PrecinctKey: %{location} | Value: %{z}<extra></extra>"
    ))
    fig2.update_geos(fitbounds="locations", visible=False)
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    merge_target= aggregate('Precincts','score',targetingcatalog,startermetrics,weights)
    with open(pctgeopath) as geofile:
        j_file = json.load(geofile)
    df = merge_target[['PrecinctKey','score','City']]
    targetfig = go.Figure(data=go.Choropleth(
        locations= df['PrecinctKey'],
        colorbar={"len": 0.7,"x": 0,"y": 0.5,
                    'title': {"text": 'score', "side": "top"}},
        geojson = j_file,
        featureidkey = 'properties.PCTKEY', # Spatial coordinates
        z = df['score'], # Data to be color-coded
        colorscale = 'Teal',
        hoverinfo='location+z',
        hovertemplate="PrecinctKey: %{location} | Value: %{z}<extra></extra>"
    ))
    targetfig.update_geos(fitbounds="locations", visible=False)
    targetfig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#_______________________________________________________________________________
#Initialize histogram, scatter__________________________________________________
var1 = election_results_prec[0]
var2 = election_results_prec[1]
merged1 = aggregate('Precincts', var1,resultscatalog)
df1 = merged1[['PrecinctKey',var1]]
merged2 = aggregate('Precincts', var2,resultscatalog)
df2 = merged2[['PrecinctKey',var2]]
box =make_subplots(rows=1,cols=2)
box.add_trace(go.Box(y=df1[var1], boxpoints='all',
                name=var1,text=df1['PrecinctKey'],hoverinfo='y+text',selectedpoints=[],
                hovertemplate="PrecinctKey: %{text} | Value: %{y}<extra></extra>"),
                row=1,col=1)
box.add_trace(go.Box(y=df2[var2], boxpoints='all',
                name=var2,text=df2['PrecinctKey'],hoverinfo='y+text',selectedpoints=[],
                hovertemplate="PrecinctKey: %{text} | Value: %{y}<extra></extra>"),
                row=1,col=2)
box.update_layout(showlegend=False)
df = df1.merge(df2,left_on='PrecinctKey',right_on='PrecinctKey')
scat = px.scatter(df,x=var1,y=var2,trendline='ols',hover_data=['PrecinctKey'])
scat.update_layout(xaxis_title=var1,yaxis_title=var2)


#______________________________________________________________________________
#Main App Layout_______________________________________________________________
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-2', children=[
        dcc.Tab(label='Targeting', value='tab-1'),
        dcc.Tab(label='2018 Electorate Case Study', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(dash.dependencies.Output('tabs-content', 'children'),
              [dash.dependencies.Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-2': #Election Results [example]
        return html.Div(children=[
            html.H1(children='TX31 Data Dashboard'), #page title goes here
            html.Div([dcc.RadioItems(
                id='granularity',
                options=[{'label': i, 'value': i} for i in ['Precincts']],
                value='Precincts',
                labelStyle={'display': 'inline-block'}
            ),]),
            dbc.Row([
                dbc.Col(html.Div([
                    dcc.Graph(
                        id='chloropleth',
                        figure=fig,
                    ),
                    dcc.Dropdown(
                        id='variable',
                        options=[{'label': i, 'value': i} for i in election_results_prec],
                        value= election_results_prec[-1]
                    ),
                    dcc.Graph(id='scatter',figure = scat),
                ],
                ),),
                dbc.Col(html.Div([
                    dcc.Graph(id='box',figure = box),
                    dcc.Dropdown(
                        id='variable2',
                        options=[{'label': i, 'value': i} for i in election_results_prec],
                        value= election_results_prec[-1]
                    ),
                    dcc.Graph(
                        id='chloropleth2',
                        figure=fig2,
                    ),
                    ]
                    ),)
                ],)],style={'height':'50vh'},)

    elif tab == 'tab-1': #Targeting
        return html.Div(children=[
            html.H1(children='TX31 Data Dashboard'),
            dbc.Row([
                dbc.Col(html.Div([
                    dcc.Graph(
                        id='targetmap',
                        figure=targetfig,
                    ),
                    dcc.Dropdown(
                        id='targetvariable',
                        options=[{'label': i, 'value': i} for i in target_metrics],
                        value= 'score'
                    ),
                    dcc.Markdown(id='stats',children=''),
                ],
                ),),
                dbc.Col(html.Div([
                    dash_table.DataTable(
                        id = 'scoretable',
                        columns=[{"name": i, "id": i} for i in sorted.columns],
                        data=sorted.to_dict('records'),
                        style_cell={'textAlign': 'center'},
                        style_table={
                                    'height':430,
                                    'width':720,
                                    'overflowY': 'auto',
                                    'overflowX':'scroll',
                                    },
                        fixed_rows={'headers': True},
                        style_header={
					                   'backgroundColor': 'rgb(230, 230, 230)',
					                    'fontWeight': 'bold'
				                      },
                        ),
                    dcc.Dropdown(
                        id='includemetrics',
                        options=[{'label': i, 'value': i} for i in target_metrics if i != 'score'],
                        value= startermetrics,
                        multi=True
                    ),
                    html.Div(id='input_container')
                    ]
                    ),)
                ],)],style={'height':'50vh'},)

#_______________________________________________________________________________
#Demographics/Case Study Callbacks______________________________________________
@app.callback([dash.dependencies.Output('variable', 'options'),
    dash.dependencies.Output('variable2', 'options')],
    [dash.dependencies.Input('granularity', 'value'),
    dash.dependencies.Input('tabs', 'value')])
def update_options(gran,tab):
    """Changes what granularity options are available depending on the page"""
    if gran == 'Precincts':
        if tab == 'tab-2':
            return [{'label': i, 'value': i} for i in election_results_prec],[{'label': i, 'value': i} for i in election_results_prec]
        #can add tabs for multiple pages
        #elif tab == 'tab-1':
            #return [{'label': i, 'value': i} for i in election_results_prec],[{'label': i, 'value': i} for i in election_results_prec]
    else: #use zipcode mappings instead
        return [{'label': i, 'value': i} for i in election_results_zip],[{'label': i, 'value': i} for i in election_results_zip]

@app.callback([dash.dependencies.Output('variable', 'value'),
    dash.dependencies.Output('variable2', 'value')],
    [dash.dependencies.Input('granularity', 'value')])
def update_value(gran):
    """Responds to radio button input changing between Precinct/Zipcode level data"""
    if gran == 'Precincts':
        return election_results_prec[0], election_results_prec[-1]
    else: #use zipcode mappings instead
        return election_results_zip[0],election_results_zip[-1]

@app.callback([dash.dependencies.Output('chloropleth', 'figure'),
    dash.dependencies.Output('chloropleth2', 'figure')],
    [dash.dependencies.Input('granularity', 'value'),
    dash.dependencies.Input('variable', 'value'),
    dash.dependencies.Input('variable2', 'value')])
def update_chloropleths(type, var,var2):
    """Updates chloropleths in response to change in granularity or vars"""
    merged = aggregate(type, var,resultscatalog)
    if type == 'Precincts':
        with open(pctgeopath) as geofile:
            j_file = json.load(geofile)
        df = merged[['PrecinctKey',var]]
        fig = go.Figure(data=go.Choropleth(
            locations= df['PrecinctKey'],
            colorbar={"len": 0.7,"x": 0,"y": 0.5,
                    'title': {"text": var, "side": "top"}},
            geojson = j_file,
            featureidkey = 'properties.PCTKEY', # Spatial coordinates
            z = df[var], # Data to be color-coded
            colorscale = 'Teal',
            hoverinfo='location+z',
            hovertemplate="PrecinctKey: %{location} | Value: %{z}<extra></extra>"
        ))
    else:
        with open(zipgeopath) as geofile:
            j_file = json.load(geofile)
        df = merged[['zipcode', var]]
        fig = go.Figure(data=go.Choropleth(
            locations= df['zipcode'],
            geojson = j_file,
            colorbar={"len": 0.7,"x": 0,"y": 0.5,
                        'title': {"text": var, "side": "top"}},
            featureidkey = 'properties.zip', # Spatial coordinates
            z = df[var], # Data to be color-coded
            colorscale = 'Teal',
            hoverinfo='location+z',
            hovertemplate="Zipcode: %{location} | Value: %{z}<extra></extra>"
        ))
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    merged = aggregate(type, var2,resultscatalog)
    if type == 'Precincts':
        with open(pctgeopath) as geofile:
            j_file = json.load(geofile)
        df = merged[['PrecinctKey',var2]]
        fig2 = go.Figure(data=go.Choropleth(
            locations= df['PrecinctKey'],
            colorbar={"len": 0.7,"x": 0,"y": 0.5,
                    'title': {"text": var2, "side": "top"}},
            geojson = j_file,
            featureidkey = 'properties.PCTKEY', # Spatial coordinates
            z = df[var2], # Data to be color-coded
            colorscale = 'Burg',
            hoverinfo='location+z',
            hovertemplate="PrecinctKey: %{location} | Value: %{z}<extra></extra>"
        ))
    else:
        with open(zipgeopath) as geofile:
            j_file = json.load(geofile)
        df = merged[['zipcode', var2]]
        fig2 = go.Figure(data=go.Choropleth(
            locations= df['zipcode'],
            geojson = j_file,
            colorbar={"len": 0.7,"x": 0,"y": 0.5,
                        'title': {"text": var2, "side": "top"}},
            featureidkey = 'properties.zip', # Spatial coordinates
            z = df[var2], # Data to be color-coded
            colorscale = 'Burg',
            hoverinfo='location+z',
            hovertemplate="Zipcode: %{location} | Value: %{z}<extra></extra>"
        ))
    fig2.update_geos(fitbounds="locations", visible=False)
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig, fig2

@app.callback(
    dash.dependencies.Output('box', 'figure'),
    [dash.dependencies.Input('chloropleth', 'hoverData'),
     dash.dependencies.Input('chloropleth2', 'hoverData'),
     dash.dependencies.Input('variable', 'value'),
     dash.dependencies.Input('variable2', 'value'),
     dash.dependencies.Input('granularity', 'value')])
def update_box(hoverData1,hoverData2, var1,var2, type):
    """Updates box plot in response to change in granularity, vars,
        or which precinct user is hovering over"""
    if type == 'Precincts':
        try:
            precinctkey1 = hoverData1['points'][0]['location']
            precinctkey2 = hoverData2['points'][0]['location']
        except TypeError:
            precinctkey1 = 270402
            precinctkey2 = 270402
        merged1 = aggregate('Precincts', var1,resultscatalog)
        merged2 = aggregate('Precincts',var2,resultscatalog)
        df1 = merged1[['PrecinctKey',var1]]
        df2 = merged2[['PrecinctKey',var2]]
        index1 = df1.index[df1['PrecinctKey'] == precinctkey1].tolist()
        index2 = df2.index[df2['PrecinctKey'] == precinctkey2].tolist()
        box =make_subplots(rows=1,cols=2)
        box.add_trace(go.Box(y=df1[var1], boxpoints='all',
                        name=var1,text=df1['PrecinctKey'],hoverinfo='y+text',selectedpoints=index1,
                        hovertemplate="PrecinctKey: %{text} | Value: %{y}<extra></extra>"),
                        row=1,col=1)
        box.add_trace(go.Box(y=df2[var2], boxpoints='all',
                        name=var2,text=df2['PrecinctKey'],hoverinfo='y+text',selectedpoints=index2,
                        hovertemplate="PrecinctKey: %{text} | Value: %{y}<extra></extra>"),
                        row=1,col=2)
        box.update_layout(showlegend=False)
    else: #for zipcode mappings
        try:
            zip1 = hoverData1['points'][0]['location']
            zip2 = hoverData2['points'][0]['location']
        except TypeError:
            zip1 = 76543
            zip2 = 76543
        merged1 = aggregate('Zipcodes',var1,resultscatalog)
        merged2 = aggregate('Zipcodes',var2,resultscatalog)
        df1 = merged1[['zipcode',var1]]
        df2 = merged2[['zipcode',var2]]
        index1 = df1.index[df1['zipcode'] == zip1].tolist()
        index2 = df2.index[df2['zipcode'] == zip2].tolist()
        box =make_subplots(rows=1,cols=2)
        box.add_trace(go.Box(y=df1[var1], boxpoints='all',
                        name=var1,text=df1['PrecinctKey'],hoverinfo='y+text',selectedpoints=index1,
                        hovertemplate="PrecinctKey: %{text} | Value: %{y}<extra></extra>"),
                        row=1,col=1)
        box.add_trace(go.Box(y=df2[var2], boxpoints='all',
                        name=var2,text=df2['PrecinctKey'],hoverinfo='y+text',selectedpoints=index2,
                        hovertemplate="PrecinctKey: %{text} | Value: %{y}<extra></extra>"),
                        row=1,col=2)
        box.update_layout(showlegend=False)
    return box

@app.callback(
    dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('chloropleth2', 'hoverData'),
     dash.dependencies.Input('variable', 'value'),
     dash.dependencies.Input('variable2', 'value'),
     dash.dependencies.Input('granularity', 'value')])
def update_scatter_c1(hoverData,var1,var2,type):
    """Updates scatter plot in response to change in granularity, vars,
        or which precinct user is hovering over"""
    if type == 'Precincts':
        try:
            precinctkey = hoverData['points'][0]['location']
        except TypeError:
            precinctkey = 270402
        merged1 = aggregate('Precincts', var1,resultscatalog)
        df1 = merged1[['PrecinctKey',var1]]
        merged2 = aggregate('Precincts', var2,resultscatalog)
        df2 = merged2[['PrecinctKey',var2]]
        df = df1.merge(df2,left_on='PrecinctKey',right_on='PrecinctKey')
        index = df.index[df['PrecinctKey'] == precinctkey].tolist()
        scat = px.scatter(df,x=var1,y=var2,trendline='ols',hover_data=['PrecinctKey'])
        scat.update_layout(xaxis_title=var1,yaxis_title=var2)
        results = px.get_trendline_results(scat)
        print(results.px_fit_results.iloc[0].summary())
    else: #for zipcode mappings
        try:
            zip = hoverData['points'][0]['location']
        except TypeError:
            zip = 76543
        merged1 = aggregate('Zipcodes', var1,resultscatalog)
        df1 = merged1[['zipcode',var1]]
        merged2 = aggregate('Zipcodes', var2,resultscatalog)
        df2 = merged2[['zipcode',var2]]
        df = df1.merge(df2,left_on='zipcode',right_on='zipcode')
        index = df.index[df['zipcode'] == zip].tolist()
        scat = px.scatter(df,x=var1,y=var2,trendline='ols',hover_data=['zipcode'])
        scat.update_layout(xaxis_title=var1,yaxis_title=var2)
        results = px.get_trendline_results(scat)
        print(results.px_fit_results.iloc[0].summary())
    return scat
#_______________________________________________________________________________
#Targeting Callbacks____________________________________________________________
@app.callback(dash.dependencies.Output('targetvariable', 'options'),
    [dash.dependencies.Input('includemetrics', 'value')])
def update_targetoptions(include):
    """update options for var to map depending on which metrics user chooses to include"""
    if 'score' not in include:
        include.insert(0,'score')
    return [{'label': i, 'value': i} for i in include]

@app.callback(dash.dependencies.Output('targetmap', 'figure'),
    [dash.dependencies.Input('targetvariable', 'value'),
    dash.dependencies.Input('includemetrics', 'value'),
    dash.dependencies.Input({'type': 'weight-slider', 'index': ALL}, 'value')])
def update_targetmap(var,include,weights):
    """update chloropleth if user changes weights, metrics, or var to map"""
    if var == 'score':
        merged= aggregate('Precincts',var,targetingcatalog,include,weights)
        df = merged[['PrecinctKey',var]]
    else:
        merged = aggregate('Precincts', var,resultscatalog)
        df = merged[['PrecinctKey',var]]
    with open(pctgeopath) as geofile:
        j_file = json.load(geofile)
    fig = go.Figure(data=go.Choropleth(
        locations= df['PrecinctKey'],
        colorbar={"len": 0.7,"x": 0,"y": 0.5,
                'title': {"text": var, "side": "top"}},
        geojson = j_file,
        featureidkey = 'properties.PCTKEY', # Spatial coordinates
        z = df[var], # Data to be color-coded
        colorscale = 'Teal',
        hoverinfo='location+z',
        hovertemplate="PrecinctKey: %{location} | Value: %{z}<extra></extra>"
    ))
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@app.callback(dash.dependencies.Output('scoretable', 'data'),
    [dash.dependencies.Input('includemetrics', 'value'),
    dash.dependencies.Input({'type': 'weight-slider', 'index': ALL}, 'value')])
def update_scoretable(include,weights):
    """Update precinct rankings if user changes metrics or weights"""
    sorted = calc_targetscore(include,weights,targetingcatalog)
    sorted = sorted[['PrecinctKey','score','City']]
    return sorted.to_dict('records')

@app.callback(dash.dependencies.Output('stats', 'children'),
            [dash.dependencies.Input('targetmap', 'hoverData'),
            dash.dependencies.Input('includemetrics', 'value'),
            dash.dependencies.Input({'type': 'weight-slider', 'index': ALL}, 'value')])
def update_stattext(hoverData,include,w):
    """update lower left stats readout if user changes which precinct they hover on,
    weights, or target vars"""
    try:
        precinctkey = hoverData['points'][0]['location']
    except TypeError:
        precinctkey = 270402
    stats = []
    targets = []
    weights = []
    index = 0
    for var in include:
        if var != 'score':
            merged = aggregate('Precincts', var,resultscatalog)
            df = merged[['PrecinctKey',var]]
            stat = df[df['PrecinctKey'] == precinctkey][var].values[0]
            stats.append(stat)
            targets.append(var)
            weights.append(w[index])
            index = index + 1
    s = "#   \n #   \n #   \n### &nbsp; &nbsp;  Stats for Precinct " + str(precinctkey) + '   \n'
    for i in range(len(targets)):
        s = s + ' &nbsp; &nbsp; *%s*: %.2f (weight=%s)   \n'%(targets[i],stats[i],str(weights[i]))
    return s

@app.callback(dash.dependencies.Output('input_container', 'children'),
            [dash.dependencies.Input('includemetrics', 'value')])
def update_sliders(include):
    """update weight sliders if user adds/removes target vars"""
    if 'score' in include:
        include.remove('score')
    sliders = [html.Div([dcc.Markdown(include[i]),
                        dcc.Slider(id={
                                        'type': 'weight-slider',
                                        'index': include[i]
                                        },min=-5,
                                max=5,
                                step=1,
                                marks={-5:'-5x',
                                        0:'0x',
                                        5:'5x'},
                                value=1),],style={'width': '49%', 'display': 'inline-block'}
                    ) for i in range(len(include))]
    if 'score' not in include:
        include.insert(0,'score')
    return sliders
#_______________________________________________________________________________
#Turfcutter Callbacks, disabled_________________________________________________
"""@app.callback(dash.dependencies.Output('turfmap', 'figure'),
    [dash.dependencies.Input('turfdata-json', 'children')])
def update_turfmap(jsonified_data):
    proxy = gpd.read_file(jsonified_data)
    turfgeo = json.loads(jsonified_data)
    turfmap = go.Figure(data=go.Choropleth(
        locations=proxy['GEO_ID'],
        colorbar={"len": 0.7,"x": 0,"y": 0.5,
                    'title': {"text": 'score', "side": "top"}},
        geojson = turfgeo,
        featureidkey = 'properties.GEO_ID', # Spatial coordinates
        z = proxy['Score'], # Data to be color-coded
        zmin=0,
        zmax=7,
        colorscale = 'dense',
        hoverinfo='location+z',
        hovertemplate="GEO_ID: %{location} | Score: %{z}<extra></extra>"
    ))
    turfmap.update_geos(fitbounds="locations", visible=False)
    turfmap.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return turfmap

@app.callback([dash.dependencies.Output('includepcts', 'children'),
    dash.dependencies.Output('selectmap', 'figure')],
    [dash.dependencies.Input('selectmap', 'clickData')],
    [dash.dependencies.State('includepcts','children')])
def update_pctselections(click,jsondata):
    try:
        includepcts = pd.read_json(jsondata, orient='split')
    except:
        includepcts=  pd.DataFrame({'PCTKEY':killeen})
    pctkey = str(click['points'][0]['location'])
    print(pctkey)
    include = [str(x) for x in includepcts['PCTKEY'].tolist()]
    if pctkey in include:
        include.remove(pctkey)
    else:
        include.append(pctkey)
    merge_target= aggregate('Precincts','score',turfcatalog,startermetrics,weights)
    with open(pctgeopath) as geofile:
        j_file = json.load(geofile)
    df = merge_target[['PrecinctKey','score','City']]
    #df['score'] = [0 for x in range(len(df))]
    def isselected(pct):
        if str(pct) in include:
            return 1
        else:
            return 0
    df['score'] =df.apply(lambda row: isselected(row['PrecinctKey']), axis=1)
    selectmap = go.Figure(data=go.Choropleth(
        locations= df['PrecinctKey'],
        geojson = j_file,
        featureidkey = 'properties.PCTKEY', # Spatial coordinates
        z = df['score'], # Data to be color-coded
        colorscale = [[0,'rgb(230,240,240)'],[1,'rgb(100,31,104)']],
        zmin=0,
        zmax=1,
        hoverinfo='location+z',
        hovertemplate="PrecinctKey: %{location}"
    ))
    selectmap.update_geos(fitbounds="locations", visible=False)
    selectmap.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    includepcts = pd.DataFrame({'PCTKEY':[str(x) for x in include]})
    print(includepcts)
    return includepcts.to_json(orient='split'),selectmap

@app.callback([dash.dependencies.Output('activatedturfs-json', 'children'),
    dash.dependencies.Output('turf_buffers', 'children'),
    dash.dependencies.Output('turfdata-json','children')],
    [dash.dependencies.Input('includepcts', 'children'),
    dash.dependencies.Input('turfmap', 'clickData'),
    dash.dependencies.Input({'type': 'turf-buffer', 'index': ALL}, 'value')],
    [dash.dependencies.State('activatedturfs-json', 'children'),
    dash.dependencies.State('turfdata-json', 'children')])
def update_activatedturfs(include,click,buff,activatedjson,turfjson):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    try:
        include = pd.read_json(include, orient='split')
        include = [str(x) for x in include['PCTKEY'].tolist()]
    except:
        include= killeen
    try:
        activated = pd.read_json(activatedjson, orient='split')
    except:
        activated = pd.DataFrame({'GID':[],'Address':[],'Buffer':[],'PCTKEY':[],'n_homes':[]})
    turfs = turfdata
    print('include:',include)
    print('click:',click)
    print('buff:',buff)
    try:
        gid = click['points'][0]['location']
    except:
        gid=None
    current = [str(x) for x in activated['GID'].tolist()]
    if buff is None:
        buff = [0.02 for x in current]
    if gid is not None:
        if trigger == 'turfmap':
            if gid in current:
                index= current.index(gid)
                current.remove(gid)
                buff.pop(index)
            else:
                current.append(gid)
                buff.append(0.02)
    print(current)
    n_homes = []
    pct = []
    address = []
    homecount =0
    turfs['Score'] = [0 for x in range(len(turfs))]
    def isinside(circle,center,geom,score):
        if geom.centroid.within(circ):
            homecount.append(1)
            if geom == center:
                return 7
            else:
                return score + 2
        else:
            return score
    print('calculating ')
    print(len(current),len(buff))
    for i in range(len(current)):
        homecount = []
        data =turfs[turfs['GEO_ID']==str(current[i])].iloc[0]
        address.append(data['Address'])
        pct.append(data['PCTKEY'])
        circ = data['geometry'].centroid.buffer(float(buff[i]))
        print('CENTROID',data['geometry'].centroid)
        turfs['Score'] = turfs.apply(lambda row: isinside(circ, data['geometry'],row['geometry'],row['Score']), axis=1)
        print('SCORE',turfs[turfs['GEO_ID']==str(current[i])].iloc[0]['Score'])
        print('AREA',circ.area)
        n_homes.append(len(homecount))
    print(len(current),len(address),len(buff),len(pct),len(n_homes))
    activated = pd.DataFrame({'GID':[str(x) for x in current],'Address':address,'Buffer':buff,'PCTKEY':pct,'n_homes':n_homes})
    sliders = [html.Div([dcc.Markdown('Turf '+str(i)+':gid='+str(activated['GID'].iloc[i])),
                        dcc.Slider(id={
                                        'type': 'turf-buffer',
                                        'index': i
                                        },
                                min=0.005,
                                max=0.05,
                                step=0.0001,
                                marks={0.005:'0.005',
                                        0.01:'0.01',
                                        0.02:'0.02',
                                        0.03:'0.03',
                                        0.04:'0.04',
                                        0.05:'0.05'},
                                value=buff[i]),
                        dcc.Markdown('n_homes:'+str(activated['n_homes'].iloc[i]))],style={'width': '49%', 'display': 'inline-block'}
                    ) for i in range(len(activated))]
    turfs = turfs[turfs['PCTKEY'].isin(include)]
    turfs.to_file('bellturfs.json',driver='GeoJSON')
    return activated.to_json(orient='split'), sliders, turfs.to_json()

@app.callback(dash.dependencies.Output('turftable', 'data'),
    [dash.dependencies.Input('activatedturfs-json', 'children')])
def update_turftable(activatedjson):
    try:
        activated = pd.read_json(activatedjson, orient='split')
    except:
        activated = pd.DataFrame({'GID':[],'Address':[],'PCTKEY':[]})
    activated = activated[['GID','Address','PCTKEY']]
    return activated.to_dict('records')
    """
#_________________________________________________________________________________________________
#Canvass/Live Vote Tracking Functions, disabled______________________________________________________________________________________________________
"""@app.callback([dash.dependencies.Output('tracking1', 'figure'),
    dash.dependencies.Output('tracking2', 'figure')],
    [dash.dependencies.Input('trackingvar1', 'value'),
    dash.dependencies.Input('trackingvar2', 'value')])
def update_chloropleths(var,var2):
    merged = aggregate('Precincts', var,canvasscatalogue)
    with open("geometry/json/geojson-willco-precincts.json") as geofile:
        j_file = json.load(geofile)

    df = merged[['PCTKEY',var]]
    fig = go.Figure(data=go.Choropleth(
        locations= df['PCTKEY'],
        colorbar={"len": 0.7,"x": 0,"y": 0.5,
                'title': {"text": var, "side": "top"}},
        geojson = j_file,
        featureidkey = 'properties.PCTKEY', # Spatial coordinates
        z = df[var], # Data to be color-coded
        colorscale = 'Teal',
        hoverinfo='location+z',
        hovertemplate="PrecinctKey: %{location} | Value: %{z}<extra></extra>"
    ))
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    merged = aggregate('Precincts', var2,canvasscatalogue)
    with open("geometry/json/geojson-willco-precincts.json") as geofile:
        j_file = json.load(geofile)
    df = merged[['PCTKEY',var2]]
    fig2 = go.Figure(data=go.Choropleth(
        locations= df['PCTKEY'],
        colorbar={"len": 0.7,"x": 0,"y": 0.5,
                'title': {"text": var2, "side": "top"}},
        geojson = j_file,
        featureidkey = 'properties.PCTKEY', # Spatial coordinates
        z = df[var2], # Data to be color-coded
        colorscale = 'Burg',
        hoverinfo='location+z',
        hovertemplate="PrecinctKey: %{location} | Value: %{z}<extra></extra>"
    ))
    fig2.update_geos(fitbounds="locations", visible=False)
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig, fig2

@app.callback(
    dash.dependencies.Output('trackingfig', 'figure'),
    [dash.dependencies.Input('figtype', 'value')])
def update_fig(fig):
    if fig == 'Day':
        evdata = pd.read_csv('canvasstracking/evdata-williamson.csv')
        newev = scrape_evtotals()
        trackfig = go.Figure(data=[
            go.Scatter(name='Williamson 2016',x=evdata['Day Number'], y=evdata['2016 in person'],hovertext = evdata['2016 Day'],mode='lines+markers'),
            go.Scatter(name='Williamson 2018',x=evdata['Day Number'], y=evdata['2018 in person'],hovertext = evdata['2018 Day'],mode='lines+markers'),
            go.Scatter(name='Williamson 2020',x=newev['Day Number'], y=newev['Early Vote'],hovertext = newev['Date'],mode='lines+markers')
        ])
        trackfig.update_layout(title='# Votes in Person per Day of Early Vote',yaxis_title='Votes in Person')
    elif fig == 'Polling Place':
        ppdata = scrape_pptotals()
        trackfig = go.Figure(data=[
            go.Bar(x=ppdata['Location Code'], y=ppdata['Early Vote'],text=ppdata['Early Vote'],textposition='auto'),
        ])
        trackfig.update_layout(title='Total Early Vote by Polling Place')
    return trackfig

@app.callback(
    dash.dependencies.Output('trackingscatter', 'figure'),
    [dash.dependencies.Input('trackingvar1', 'value'),
     dash.dependencies.Input('trackingvar2', 'value')])
def update_canvass_scatter(var1,var2):
    merged1 = aggregate('Precincts', var1,canvasscatalogue)
    df1 = merged1[['PrecinctKey',var1]]
    merged2 = aggregate('Precincts', var2,canvasscatalogue)
    df2 = merged2[['PrecinctKey',var2]]
    df = df1.merge(df2,left_on='PrecinctKey',right_on='PrecinctKey')
    scat = px.scatter(df,x=var1,y=var2,trendline='ols',hover_data=['PrecinctKey'])
    scat.update_layout(xaxis_title=var1,yaxis_title=var2)
    results = px.get_trendline_results(scat)
    print(results.px_fit_results.iloc[0].summary())
    return scat
"""

#Run app
if __name__ == '__main__':
    app.run_server(debug=True)
