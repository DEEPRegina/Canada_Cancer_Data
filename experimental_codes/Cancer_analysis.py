#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 13:27:46 2020

@author: karthik
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
import pickle as pkl
#Names = ['REF_DATE','GEO','Age Group','Sex','Primary types of cancer (ICD-O-3)',
#         'Prevalence duration','Characteristics','VALUE']
#
#
#Cancer_Data = pd.read_csv("Cancer_Data.csv",sep=',',usecols=['REF_DATE'])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
pickle_file =open("MasterDict.pickle",'rb')
MasterDict = pkl.load(pickle_file)
pickle_file.close()
Cancer_Data = pd.read_csv("canada_cancer_data.zip",compression='zip',sep=',')
Cancer_Data.drop(['Unnamed: 0'],axis=1,inplace=True)
Column_Names = np.array(Cancer_Data.columns.values[1:-1],dtype=str)


YEAR = MasterDict['YEAR']

GeoNames = MasterDict['GEO']


AgeGroup = MasterDict['AGE']

PrevalanceDuration = MasterDict['PREVALENCE_DURATION']

Sex = MasterDict['SEX']

CancerType = MasterDict['CANCER_NAMES']

Characteristics = MasterDict['CHARACTERISTICS']
colors = {
    'background': '#111121',
    'text': '#7FDBFF'
}

ParaContent = '''We are currently analysing the Cancer Data from stats canada website
We are currently analysing the Cancer Data from stats canada website
We are currently analysing the Cancer Data from stats canada website'''
#dff = Cancer_Data[(Cancer_Data[Column_Names[0]]==GeoNames['Canada'])]

background_url = "https://www.elsetge.cat/myimg/f/137-1377768_there-will-be-blood-wallpaper-hd-cancer-cells.png"

selected_legend = ""
def selected_legend_func(legend):
    print(selected_legend)
    if(legend==selected_legend):
        return True
    else:
        return False

app.layout = html.Div(style = {'background-image':'url({})'.format(background_url)},children=[
#        html.Div(children=[html.Img(src='https://www.uregina.ca/external/communications/assets/identity1/Primary_Logo/Full%20Colour/UR_Logo_Primary_Full_COlour_RGB.png',width="200", height="100")]),
        html.Div(style= {'textAlign': 'center','color':'white'},children=[html.H1("Cancer Data Analysis",className='Custom_Header')]),
        html.Div(style = {'textAlign' : 'left', 'color' : 'white'},children= [html.H2("Introduction",className='Custom_H2')]),
        html.Div(style = {'color' : 'white'},className="Paragraph_New",children = [html.Div(ParaContent,className='Paragraph_New')]),
            html.Div([
            html.Div(children=[html.Label("Legend This is currently dummy")]),
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='Legend',
                options=[{'label': i, 'value': i} for i in Column_Names],
                value=Column_Names[1]
            )
        ],style={'width': '25%', 'display': 'inline-block'})
        
    ]),
            html.Div(id='Legend-Status'),
            html.Hr(),

        html.Div([
            dcc.Dropdown(
                id='GEO',
                options=[{'label': i[0], 'value': i[1]} for i in GeoNames.items()],
                value='Canada',disabled=selected_legend_func('GEO')
            )
        ],
        style={'width': '25%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='AgeGroup',
                options=[{'label': i[0], 'value': i[1]} for i in AgeGroup.items()],
                value=0,disabled=selected_legend_func(Column_Names[1])
            )
        ],
        style={'width': '25%', 'display': 'inline-block'}),


        html.Div([
            dcc.Dropdown(
                id='CancerType',
                options=[{'label': i[0], 'value': i[1]} for i in CancerType.items()],
                value=0,disabled=selected_legend_func(Column_Names[3])
            )
        ],
        style={'width': '40%', 'display': 'inline-block'})
        
    ]),
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='Sex',
                options=[{'label': i[0], 'value': i[1]} for i in Sex.items()],
                value='B',disabled=selected_legend_func(Column_Names[2])
            )
        ],style={'width': '15%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='PrevalenceDuration',
                options=[{'label': i[0], 'value': int(i[1])} for i in PrevalanceDuration.items()],
                value= '2',disabled=selected_legend_func(Column_Names[4])
            )
        ],
        style={'width': '25%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='Characteristics',
                options=[{'label': i[0], 'value': i[1]} for i in Characteristics.items()],
                value='P',disabled=selected_legend_func(Column_Names[5])
            )
        ],style={'width': '40%', 'display': 'inline-block'})
        
    ]),
    dcc.Graph(id='indicator-graphic',style={'width': '50%', 'display': 'inline-block'}),
#
#    dcc.Slider(
#        id='year--slider',
#        min=df['Year'].min(),
#        max=df['Year'].max(),
#        value=df['Year'].max(),
#        marks={str(year): str(year) for year in df['Year'].unique()},
#        step=None
#    )
])
@app.callback(
        Output('Legend-Status','children'),
        [Input('Legend','value')])
def Return(label_name):
    selected_legend = label_name
    return "You have chosen {}".format(selected_legend)


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('Legend', 'value'),
     Input('GEO', 'value'),
     Input('AgeGroup', 'value'),
     Input('CancerType', 'value'),
     Input('Sex', 'value'),
     Input('PrevalenceDuration', 'value'),
     Input('Characteristics', 'value')])
def Graph(label_name,geo,agegroup,cancertype,sex,prevalenceduration,characteristics):
    dff = Cancer_Data[(Cancer_Data[Column_Names[0]]==geo) &
                                (Cancer_Data[Column_Names[1]]==agegroup) &
                                (Cancer_Data[Column_Names[2]]==sex) &
                                (Cancer_Data[Column_Names[3]]==cancertype) &
                                (Cancer_Data[Column_Names[4]]==int(prevalenceduration)) &
                                (Cancer_Data[Column_Names[5]]==characteristics)]
#    dff = Cancer_Data[(Cancer_Data[Column_Names[0]]=='Canada') &
#                                (Cancer_Data[Column_Names[1]]==0) &
#                                (Cancer_Data[Column_Names[2]]=='B') &
#                                (Cancer_Data[Column_Names[3]]==0) &
#                                (Cancer_Data[Column_Names[4]]==int('2')) &
#                                (Cancer_Data[Column_Names[5]]=='P')]
    return {
        'data': [dict(
            x=dff["REF_DATE"],
            y=dff["VALUE"],
            line = {'color' : 'red',
                    'dash' : 'longdashdot'},
            mode='lines+markers',
            marker={
                    'symbol' : 17,
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'red'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': "YEAR"
            },
            yaxis={
                'title':  characteristics
            },
            margin={'l': 40, 'b': 40, 't': 40, 'r': 0},
            hovermode='closest',
            #title = characteristics + " for a period of " + prevalenceduration + " in " + geo + " for " + sex + " between " + agegroup + " of age " 
        )
    }    
    



if __name__ == '__main__':
    app.run_server(debug=True)