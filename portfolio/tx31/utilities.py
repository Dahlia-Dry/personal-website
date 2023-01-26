import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import json
from re import sub
import os
from decimal import Decimal
from bs4 import BeautifulSoup
import requests
import csv
from io import StringIO

def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Polygon',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[0],row[1]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

def aggregate(type,title,catalog,target_metrics=None,weights=None):
    """
       -construct and return pandas df matching type and var constraints
       -for cookie-cutter stuff, use catalog format: see the else block
       -can code in exceptions for when you want to do some processing before
         defining a var instead of just using the titlevar column;
         see if and elif blocks for examples
       Parameters:
       -----------
       -type: str, Zipcodes or Precincts
       -title: str, from catalog file
       -titlevar: str, from catalog file
       -locvar: str, from catalog file
       -filename: str, from catalog file
    """
    #define the path to your precincts &/or zipcodes geojson files here
    #geovar and locvar should map 1:1, geovar is from geojson and locvar is from data file
    #eg. for precinct 104, geom_var and loc_var should both be 104
    zip_path = 'geometry/zipcodes_gpd.geojson'
    prec_path = 'geometry/precincts_gpd.geojson'
    geovar = 'PCTKEY'
    #Some initialization steps__________________________________________________
    if type == 'Zipcodes':
        gdf = gpd.read_file(zip_path)
    elif type == 'Precincts':
        gdf = gpd.read_file(prec_path)
    titlevar = catalog[catalog['title']==title]['titlevar'].iloc[0]
    locvar = catalog[catalog['title']==title]['locvar'].iloc[0]
    filename = catalog[catalog['title']==title]['filename'].iloc[0]
    #__________________________________________________________________________
    if title == 'Live Early Vote Tally':
        r =requests.get('https://www.livevoterturnout.com/williamson-nov-03-2020/TurnoutByPrecinctTable.html',
                        verify='canvasstracking/trusted-certs.pem')
        soup = BeautifulSoup(r.text,'html.parser')
        table = soup.find_all("tbody")[3]
        data = ""
        for table_row in table.findAll('tr'):
            columns = table_row.findAll('td')
            output_row = []
            for column in columns:
                output_row.append(column.text)
            data = data + ';'.join(output_row) + '\n'
        df = pd.read_csv(StringIO(data),header=None,sep=';',
                        names=['Precinct','Registered Voters','Early Vote',
                        'Provisional','Turnout'])
        df = df.iloc[:-1]
        df['PrecinctKey'] = '4910'+df['Precinct'].astype('str')
        df['Registered Voters'] = [x.replace(',','') for x in df['Registered Voters']]
        df['Early Vote'] = [x.replace(',','') for x in df['Early Vote']]
        gdf = gdf[gdf['PCTKEY'].str.startswith('491')]
        df[var] = df['Early Vote']
        merged = gdf.merge(df,'left',left_on=['PCTKEY'],right_on=['PrecinctKey'])
        merged = merged.fillna(0)
        merged = merged[merged['PCTKEY'].str.startswith('491')]
    elif title == 'TX31 2020 July Runoff-March Primary Vote Margin Difference':
        df1 = pd.read_csv('data/2020runoffvotesbyprecinct.csv')
        df2 = pd.read_csv('data/2020pvotesbyprecinct.csv')
        df1[title] = df1['Margin']-df2['Margin']
        df1[locvar] = [str(x) for x in df1[locvar]]
        merged = gdf.merge(df1,'left',left_on=[geovar],right_on=[locvar])
    elif title == 'score':
        df = calc_targetscore(target_metrics,weights,catalog)
        merged = gdf.merge(df,'left',left_on=[geovar],right_on=[locvar])
    else:
        df = pd.read_csv(filename)
        df[locvar] = [str(x) for x in df[locvar]]
        df[title] = df[titlevar]
        merged = gdf.merge(df,'left',left_on=[geovar],right_on=[locvar])
    try:
        return merged
    except:
        print(var)

def calc_targetscore(targets,weights,catalog,score=True):
    if 'score' in targets:
        targets.remove('score')
    data = aggregate('Precincts',targets[0],catalog)
    data = data[['PrecinctKey',targets[0]]]
    data[targets[0]+'_zscore'] = (data[targets[0]] - data[targets[0]].mean())/data[targets[0]].std()
    data[targets[0]+'_weighted'] = data[targets[0]+'_zscore']*weights[0]
    index = 1
    for var in targets[1:]:
        df = aggregate('Precincts',var,catalog)
        df = df[['PrecinctKey',var]]
        data = data.merge(df,on='PrecinctKey')
        data[var+'_zscore'] = (data[var] - data[var].mean())/data[var].std()
        data[var+'_weighted'] = data[var+'_zscore']*weights[index]
        index = index + 1
    data['score'] = [0 for i in range(len(data))]
    for col in data.columns:
        if '_weighted' in col:
            data['score'] = data['score']+data[col]
    data['score'] = data['score'].round(2)
    if not score:
        data=aggregate('Precincts',targets[0],catalog)
        data['score'] = data[targets[0]]
    cities= pd.read_csv('data/precinctcities.csv')
    cities = cities.fillna('-')
    cities['PrecinctKey'] = cities['PrecinctKey'].astype('str')
    data = data.merge(cities,on='PrecinctKey')
    data = data.sort_values(by=['City','score'],ascending=[False,False])
    data = data.dropna()
    if 'score' not in targets:
        targets.insert(0,'score')
    return data

def scrape_evtotals():
    r =requests.get('https://www.livevoterturnout.com/williamson-nov-03-2020/EarlyVotingTable.html',verify='canvasstracking/trusted-certs.pem')
    soup = BeautifulSoup(r.text,'html.parser')
    table = soup.find_all("tbody")[3]
    data = ""
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        data = data + ';'.join(output_row) + '\n'
    df = pd.read_csv(StringIO(data),header=None,sep=';',
                    names=['Date','Early Vote','Provisional','Total'])
    df['Day Number'] = ['Day '+str(i) for i in range(1,len(df)+1)]
    return df

def scrape_pptotals():
    r =requests.get('https://www.livevoterturnout.com/williamson-nov-03-2020/VoteTypeByLocationTable.html',verify='canvasstracking/trusted-certs.pem')
    soup = BeautifulSoup(r.text,'html.parser')
    table = soup.find_all("tbody")[3]
    data = ""
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        data = data + ';'.join(output_row) + '\n'
    df = pd.read_csv(StringIO(data),header=None,sep=';',
                    names=['Location','Early Vote'])
    df['Location Code'] = [x.split(' ')[0] for x in df['Location']]
    df = df.iloc[:-1]
    return df
