
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
import plotly.io as pio
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import pickle as pkl
pio.templates.default = "plotly_dark"
#Names = ['REF_DATE','GEO','Age Group','Sex','Primary types of cancer (ICD-O-3)',
#         'Prevalence duration','Characteristics','VALUE']
#
#
#Cancer_Data = pd.read_csv("Cancer_Data.csv",sep=',',usecols=['REF_DATE'])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
pickle_file =open("../data/MasterDict.pickle",'rb')
MasterDict = pkl.load(pickle_file)
pickle_file.close()

pickle_file = open("../data/MasterDictInverse.pickle",'rb')
MasterDictInverse = pkl.load(pickle_file)
pickle_file.close()

Cancer_Data = pd.read_csv("../data/cancerdata.zip", compression='zip', sep=',')
#print(Cancer_Data.columns)
#Column_Names = np.array(Cancer_Data.columns.values[1:-1],dtype=str)

#print(Column_Names[:])

radioItems = ['Geo', 'AgeGroup', 'Sex', 'PrevalenceDuration']

#print(MasterDict['CHARACTERISTICS'], MasterDictInverse['CHARACTERISTICS'])
def getEntries(group):
    '''
    Used to selectt the profiles to plot 
    '''
    name_dict = [{'label': i[0], 'value': i[1]} for i in group.items()]
    name_dict.append({'label': 'ALL', 'value': 999})
    return name_dict



year = MasterDict['RefDate']

GeoNames = MasterDict['Geo']


AgeGroup = MasterDict['AgeGroup']

PrevalanceDuration = MasterDict['PrevalenceDuration']

Sex = MasterDict['Sex']

CancerType = MasterDict['PrimaryCancer']

Characteristics = MasterDict['Characteristics']


AgeGroupInverse = MasterDictInverse['AgeGroup']

PrevalanceDurationInverse = MasterDictInverse['PrevalenceDuration']

SexInverse = MasterDictInverse['Sex']

CancerTypeInverse = MasterDictInverse['PrimaryCancer']

CharacteristicsInverse = MasterDictInverse['Characteristics']


colors = {
    'background': '#111121',
    'text': '#7FDBFF'
}

ParaContent = '''We are currently analysing the Cancer Data from stats canada website
We are currently analysing the Cancer Data from stats canada website
We are currently analysing the Cancer Data from stats canada website'''
#dff = Cancer_Data[(Cancer_Data[Column_Names[0]]==GeoNames['Canada'])]

background_url = "https://www.elsetge.cat/myimg/f/137-1377768_there-will-be-blood-wallpaper-hd-cancer-cells.png"


app.layout = html.Div(style = {'background-image':'url({})'.format(background_url)},
                      children=[
#        html.Div(children=[html.Img(src='https://www.uregina.ca/external/communications/assets/identity1/Primary_Logo/Full%20Colour/UR_Logo_Primary_Full_COlour_RGB.png',width="200", height="100")]),
        html.Div(style= {'textAlign': 'center','color':'white'},children=[html.H1("Cancer Data Analysis",className='Custom_Header')]),
        html.Div(style = {'textAlign' : 'left', 'color' : 'white'},children= [html.H2("Introduction",className='Custom_H2')]),
        html.Div(style = {'color' : 'white'},className="Paragraph_New",children = [html.Div(ParaContent,className='Paragraph_New')]),
            html.Div([
            html.Div(children=[html.Label("Legend This is currently dummy")]),
    html.Div([

        html.Div([
            dcc.RadioItems(
                id='Legend',
                options=[{'label': i, 'value': i} for i in radioItems],
                value=radioItems[1],
                labelStyle={'display': 'inline-block'}
            )
        ])

    ]),

        html.Div([
            dcc.Dropdown(
                id='GEO',
                options=[{'label': i[0], 'value': i[1]} for i in GeoNames.items()],
                value='Canada'
            )
        ],
        style={'width': '25%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='AgeGroup',
                options=[{'label': i[0], 'value': i[1]} for i in AgeGroup.items()],
                value=0
            )
        ],
        style={'width': '25%', 'display': 'inline-block'}),


        html.Div([
            dcc.Dropdown(
                id='CancerType',
                options=[{'label': i[0], 'value': i[1]} for i in CancerType.items()],
                value=0
            )
        ],
        style={'width': '40%', 'display': 'inline-block'})

    ]),
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='Sex',
                options=[{'label': i[0], 'value': i[1]} for i in Sex.items()],
                value='F'
            )
        ],style={'width': '15%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='PrevalenceDuration',
                options=[{'label': i[0], 'value': int(i[1])} for i in PrevalanceDuration.items()],
                value= '2'
            )
        ],
        style={'width': '25%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='Characteristics',
                options=[{'label': i[0], 'value': i[1]} for i in Characteristics.items()],
                value='P'
            )
        ],style={'width': '40%', 'display': 'inline-block'})

    ]),
    dcc.Graph(id='indicator-graphic',style={'width' : '100%','display': 'inline-block'}),
    dcc.Graph(id='pie-graphic',style={'width' : '100%','height' : '800px','display' : 'inline-block'})
#
#    dcc.Slider(
#        id='year--slider',
#        min=df['year'].min(),
#        max=df['year'].max(),
#        value=df['year'].max(),
#        marks={str(year): str(year) for year in df['year'].unique()},
#        step=None
#    )
])


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('Legend', 'value'),
     Input('GEO', 'value'),
     Input('AgeGroup', 'value'),
     Input('CancerType', 'value'),
     Input('Sex', 'value'),
     Input('PrevalenceDuration', 'value'),
     Input('Characteristics', 'value')])

def Graph(label_name, geo, agegroup, cancertype, sex, prevalenceduration, characteristics):

    legend_dict = {'Geo': geo, 'AgeGroup': agegroup, 'Sex':sex, 'PrimaryCancer': cancertype,  'PrevalenceDuration': int(prevalenceduration), 'Characteristics': characteristics}

    traces = []
    legend_list = list(legend_dict.keys())
    legend_list.remove(label_name)
    
    #curve_labels = MasterDict[label_name]
    
    #print(curve_labels)


    for k, i in enumerate(Cancer_Data[label_name].unique()):
        dff = Cancer_Data[(Cancer_Data[legend_list[0]]==legend_dict[legend_list[0]]) &
                          (Cancer_Data[legend_list[1]]==legend_dict[legend_list[1]]) &
                          (Cancer_Data[legend_list[2]]==legend_dict[legend_list[2]]) &
                          (Cancer_Data[legend_list[3]]==legend_dict[legend_list[3]]) &
                          (Cancer_Data[legend_list[4]]==legend_dict[legend_list[4]]) &
                          (Cancer_Data[label_name]==i)]
        
        dff.head()
        
        #print('Reached here')

        traces.append(dict(
                    x=dff["RefDate"],
                    y=dff["Value"],
                    line = {'color' : k,
                            'dash' : 'longdashdot'},
                    mode='lines+markers',
                    marker={
                            'symbol' : i,
                        'size': 10,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color':i}
                    },
                    name=MasterDictInverse[label_name][i], hoverinfo="Geo"
                    )
                    )




    return {
        'data': traces,
        'layout': dict(
            xaxis={
                'title': "year"
            },
            yaxis={
                'title':  MasterDictInverse['Characteristics'][characteristics]
            },
            margin={'l': 40, 'b': 40, 't': 40, 'r': 0},
            hovermode='closest',
            template = "plotly_dark",
            paper_bgcolor = '#fff'
            #title = characteristics + " for a period of " + prevalenceduration + " in " + geo + " for " + sex + " between " + agegroup + " of age "
        )
    }

@app.callback(Output('pie-graphic','figure'),
[Input('indicator-graphic','clickData'),
 Input('GEO', 'value'),
 Input('AgeGroup', 'value'),
 Input('Sex', 'value'),
 Input('PrevalenceDuration', 'value'),
 Input('Characteristics', 'value')])
                
def Piechart(clickData,geo,agegroup,sex,prevalenceduration,characteristics):

    if(clickData==None): year = 2010
    else: year = clickData['points'][0]['x']
    print(clickData)
    dff = Cancer_Data[(Cancer_Data['Geo'] == geo) &
    (Cancer_Data['AgeGroup'] == agegroup) &
    (Cancer_Data['Sex'] == sex) &
    (Cancer_Data['PrevalenceDuration'] == int(prevalenceduration)) &
    (Cancer_Data['Characteristics'] == characteristics) &
    (Cancer_Data['RefDate'] == year) &
    (Cancer_Data['PrimaryCancer'] != 0) &
    (Cancer_Data['Value'] > 0)    
    ]
    traces = []
    
    #print(list(MasterDictInverse['PrimaryCancer'].values()))
    #print(len(dff['Value'].values))    
    
    #print(len(dff["PrimaryCancer"].replace(MasterDictInverse['PrimaryCancer']).values))
    
    #dff = dff[dff['Value'].values > 1]
    
    traces.append(
            go.Pie(labels=dff["PrimaryCancer"].replace(MasterDictInverse['PrimaryCancer']),
                   values = dff['Value'], 
                   textinfo = 'label+percent',
                   textposition = 'inside',
                   hole = 0.3
                   )
            )
    
    title = "Distribution of different types of cancers with a prevalence of \n" + str(MasterDictInverse["PrevalenceDuration"][str(prevalenceduration)]) +  "in" + MasterDictInverse["Geo"][geo] + "\n the for a year" + str(MasterDictInverse["RefDate"][year]) + " for " + MasterDictInverse["Sex"][sex] + "\n belonging to " + MasterDictInverse["AgeGroup"][agegroup] + " of age."
    
    return {
        'data': traces,
        'layout': dict(
            margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
            hovermode='closest',
            template = "plotly_dark",
            title = {'text':title, 
                     'xanchor': 'left',
                     'yanchor': 'top',
                     'x': 0.0,
                     'y': 0.8
                     },
            uniformtext_minsize = 12,
            uniformtext_mode = "hide"
        )
    }

xy=0

if __name__ == '__main__':
    app.run_server(debug=True)