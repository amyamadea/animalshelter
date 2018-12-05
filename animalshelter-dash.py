
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import numpy as np
from sklearn import preprocessing
import pickle

le = preprocessing.LabelEncoder()

animalDf = pd.read_csv('AnimalDf.csv')
animalDf.drop(['DateTime'], axis=1, inplace=True)

app = dash.Dash()
app.title = 'Latihan Ujian'

# color
leColor = le.fit_transform(animalDf['Color'])
color = animalDf.copy()
color['nColor'] = leColor
color = color[['Color', 'nColor']].groupby(['Color', 'nColor']).sum()

def setOptColor():
    opt = []
    for i in range (len(color.index)):
        opt.append({'label': color.index[i][0], 'value': color.index[i][1]})

    return opt

# sex
leSex = le.fit_transform(animalDf['SexuponOutcome'])
sex = animalDf.copy()
sex['nSex'] = leSex
sex = sex[['SexuponOutcome', 'nSex']].groupby(['SexuponOutcome', 'nSex']).sum()

def setOptSex():
    opt = []
    for i in range (len(sex.index)):
        opt.append({'label': sex.index[i][0], 'value': sex.index[i][1]})

    return opt

app.layout = html.Div(
    children=[
        dcc.Tabs(id='tabs', value='tab-1', 
            children=[
                dcc.Tab(label='Tabel Data', value='tab-1', children=[
                    html.Div([
                        html.Table(
                            [
                                html.Tr([
                                    html.Td([html.P('Filter ')]),
                                    html.Td([
                                        dcc.Dropdown(
                                            id='ddl-filter-tbl',
                                            options=[
                                                {'label': 'Outcome Type', 'value': 'outcome_type'},
                                                {'label': 'Animal Type', 'value': 'animal_type'},
                                                {'label': 'Breed', 'value': 'breed'},
                                                {'label': 'Adoption', 'value': 'Adoption'},
                                            ],
                                            value='breed'
                                        ),
                                    ]),
                                ]),
                                html.Tr([
                                    html.Td([]),
                                    html.Td(
                                        html.Div(
                                            id='div-ddl-filter',
                                            children=[
                                                dcc.Dropdown(
                                                    options=[],
                                                    value='',
                                                    id='ddl-filter-val'
                                                ),
                                            ]
                                        )
                                    ),
                                ]),
                            ], 
                            style = {'width' : '400px'}
                        ),
                        dcc.Graph(
                            id='tbl-animal',
                            figure = { 
                                'data': [
                                    go.Table(
                                        header=dict(values=list(animalDf.columns),
                                            fill = dict(color='#C2D4FF'),
                                            align = ['center'] * 5
                                        ),  
                                        cells=dict(values=[animalDf[col] for col in animalDf.columns], align=['left'])
                                    )
                                ],
                                'layout' : go.Layout(
                                    height=600, margin={'t': 10}, width=900
                                )
                            }
                        ),
                    ])
                ]),
                dcc.Tab(label='Graph', value='tab-2', children=[
                    html.Br(),
                    dcc.Graph(
                        id='gobar-tab1',
                        figure = { 
                            'data': 
                            [
                                go.Bar (
                                    y = list(animalDf[animalDf['adoption']==1].groupby('month').count()['adoption']),
                                    x = ['Jan','Feb','Maret','April','Mei','Juni','July','Agustus','Sept','Okt','Nov','Des'],
                                    opacity=0.7,
                                    name='Adopted'
                                ),
                                go.Bar (
                                    y = list(animalDf[animalDf['adoption']==0].groupby('month').count()['adoption']),
                                    x = ['Jan','Feb','Maret','April','Mei','Juni','July','Agustus','Sept','Okt','Nov','Des'],
                                    opacity=0.7,
                                    name='Not Adopted'
                                )
                            ],
                            'layout' : go.Layout(
                                xaxis=dict(tickangle=-45),
                                yaxis = {'title' : 'Hewan'},
                                margin = {'l': 40, 'b': 40, 't':40, 'r':10},
                                hovermode = 'closest',
                                barmode='group',
                                title='Jumlah Data Hewan yang Diadopsi (per bulan)'
                            )
                        }
                    ),
                    html.Br(), 
                    html.Br(), 
                    html.Br(), 
                    html.Br(),       
                    dcc.Graph(
                        id='gopie-tab1',
                        figure = { 
                            'data': 
                            [
                                go.Pie (
                                    labels = ['Adoption','Died','Euthanasia','Return_to_owner','Transfer'],
                                    values = list(animalDf.groupby('OutcomeType').count()['adoption']),
                                    opacity=0.7,
                                    # name='Adopted'
                                ),
                            ],
                            'layout' : go.Layout(
                                margin = {'l': 40, 'b': 40, 't':40, 'r':10},
                                hovermode = 'closest',
                                title='Perbandingan Outcome Type'
                            )
                        }
                    ),             
                    html.Br(), 
                    html.Br(), 
                    html.Br(), 
                    html.Br(),       
                    html.Div([
                        html.Table(
                            [
                                html.Tr([
                                    html.Td([html.P('Group by: ')]),
                                    html.Td([
                                        dcc.Dropdown(
                                            id='ddl-group',
                                            options=[
                                                {'label': 'Breed', 'value': 'breed'},
                                                {'label': 'Animal Type', 'value': 'animal_type'}
                                            ],
                                            value='breed'
                                        ),
                                    ]),
                                ]),
                            ], 
                            style = {'width' : '400px'}
                        ),
                        dcc.Graph(
                            id='gostack',
                            figure = { 
                                'data': [],
                                'layout' : go.Layout(
                                    margin = {'l': 35, 'b': 40, 't':40, 'r':10},
                                    hovermode = 'closest',
                                    barmode='stack'
                                )
                            }
                        ),
                    ]),
                ]),
                dcc.Tab(label='Form', value='tab-3', children=[
                    html.Table(
                        [
                            html.Tr([
                                html.Td([html.P('Type')]),
                                html.Td([
                                    dcc.Dropdown(
                                        id='ddl-type',
                                        options=[
                                            {'label': 'Dog', 'value': '1'},
                                            {'label': 'Cat', 'value': '0'},
                                        ],
                                        value='1'
                                    ),
                                ]),
                            ]),
                            html.Tr([
                                html.Td([html.P('Bulan')]),
                                html.Td(
                                    dcc.Dropdown(
                                        id='ddl-month',
                                        options=[
                                            {'label': 'Jan', 'value': '1'},
                                            {'label': 'Feb', 'value': '2'},
                                            {'label': 'Mar', 'value': '3'},
                                            {'label': 'Apr', 'value': '4'},
                                            {'label': 'May', 'value': '5'},
                                            {'label': 'Jun', 'value': '6'},
                                            {'label': 'Jul', 'value': '7'},
                                            {'label': 'Aug', 'value': '8'},
                                            {'label': 'Sep', 'value': '9'},
                                            {'label': 'Oct', 'value': '10'},
                                            {'label': 'Nov', 'value': '11'},
                                            {'label': 'Dec', 'value': '12'},
                                        ],
                                        value='1'
                                    ),
                                ),
                            ]),
                            html.Tr([
                                html.Td([html.P('Umur')]),
                                html.Td(
                                    dcc.Input(
                                        id='input-ages',
                                        type='text'
                                    ),
                                ),
                            ]),
                            html.Tr([
                                html.Td([html.P('Breed')]),
                                html.Td(
                                    html.Div(
                                        id='div-ddl-breed',
                                        children=[
                                            dcc.Dropdown(
                                                id='ddl-breed',
                                                options=[],
                                                value=''
                                            ),
                                        ]
                                    ),
                                ),
                            ]),
                            html.Tr([
                                html.Td([html.P('Color')]),
                                html.Td(
                                    dcc.Dropdown(
                                        id='ddl-color',
                                        options=setOptColor(),
                                        value='0'
                                    ),
                                ),
                            ]),
                            html.Tr([
                                html.Td([html.P('Sex')]),
                                html.Td(
                                    dcc.Dropdown(
                                        id='ddl-sex',
                                        options=setOptSex(),
                                        value='0'
                                    ),
                                ),
                            ]),
                            html.Tr([
                                html.Td([]),
                                html.Td(
                                    html.Button('Submit', id='button'),
                                ),
                            ]),
                        ], 
                        style = {'width' : '400px'}
                    ),
                    html.Br(), 
                    html.Br(), 
                    html.Br(), 
                    html.Div(id='output-container-button', children='')
                ]),
            ],
            style = {
                'fontFamily' : 'system-ui'
            },
            content_style = {
                'fontFamily' : 'Calibri',
                'borderLeft' : '1px solid #d6d6d6',
                'borderRight' : '1px solid #d6d6d6',
                'borderBottom' : '1px solid #d6d6d6',
                'padding' : '40px'
            },
        ),
    ],
    style = {
            'maxWidth' : '1000px',
            'margin' : '0 auto'
        }
)

@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('ddl-type', 'value'), dash.dependencies.State('input-ages', 'value'), dash.dependencies.State('ddl-month', 'value'), dash.dependencies.State('ddl-breed', 'value'), dash.dependencies.State('ddl-color', 'value'), dash.dependencies.State('ddl-sex', 'value')])

def update_output(n_clicks, type, ages, month, breed, color, sex):
    loadModel = pickle.load(open('animalshelter.sav', 'rb'))
    arr = np.array([month, ages, sex, type, color, breed]).reshape(1, 6)
    # arr = np.array([1,730,2,1,86,1066]).reshape(1, 6)
    
    rfc_pred = loadModel.predict(arr)

    if (rfc_pred[0]==0):
        pred = 'Tidak Diadopsi'
    else:
        pred = 'Diadopsi'

    return 'Hasil prediksi: "{}".'.format(
        pred,
        n_clicks
    )


@app.callback(
    Output('div-ddl-breed', 'children'), 
    [Input('ddl-type', 'value')]
)

def setBreedOpt(type):
    leBreed = le.fit_transform(animalDf['Breed'])
    breedDf = animalDf.copy()
    breedDf['nBreed'] = leBreed

    if (type=='1'):
        type = 'Dog'
    else:
        type = 'Cat'

    breedDf = breedDf[breedDf['AnimalType']==type][['Breed', 'nBreed']].groupby(['Breed', 'nBreed']).sum()
    opt = []
    for i in range (len(breedDf.index)):
        opt.append({'label': breedDf.index[i][0], 'value': breedDf.index[i][1]})
    
    return dcc.Dropdown(
                id='ddl-breed',
                options=opt,
                value= breedDf.index[0][1]
            )

@app.callback(
    Output('gostack', 'figure'), 
    [Input('ddl-group', 'value')]
)

def setDataGoStack(group):
    if (group=='breed'):
        x = ['pure', 'mixed']
    else:
        x = ['Dog', 'Cat']
    
    goBar = []

    sex = animalDf['SexuponOutcome'].unique()
    for i in range(len(sex)):
        countAdopt = []
        for a in x:
            if (group=='breed'):
                countAdopt.append(
                    len(animalDf[(animalDf['SexuponOutcome']==sex[i]) & (animalDf['adoption']==1) & (animalDf['nBreed']==str.lower(a))])
                )
            else:
                countAdopt.append(
                    len(animalDf[(animalDf['SexuponOutcome']==sex[i]) & (animalDf['adoption']==1) & (animalDf['AnimalType']==a)])
                )
        
        goBar.append(
            go.Bar(
                x=x,
                y=countAdopt,
                name=sex[i]
            )
        )
     
    return {
        'data': goBar,
        'layout' : go.Layout(
            margin = {'l': 40, 'b': 40, 't':40, 'r':10},
            hovermode = 'closest',
            barmode='group',
            title='Hewan yang Diadopsi'
        )
    }

@app.callback(
    Output('div-ddl-filter', 'children'), 
    [Input('ddl-filter-tbl', 'value')]
)

def setFilterOption(flt):
    if (flt=='outcome_type'):
        opt = [
            {'label': 'Return_to_owner', 'value': 'Return_to_owner'},
            {'label': 'Euthanasia', 'value': 'Euthanasia'},
            {'label': 'Adoption', 'value': 'Adoption'},
            {'label': 'Died', 'value': 'Died'},
            {'label': 'Transfer', 'value': 'Transfer'},
        ]
        val = 'Return_to_owner'

    elif (flt=='animal_type'):
        opt = [
            {'label': 'Dog', 'value': 'Dog'},
            {'label': 'Cat', 'value': 'Cat'},
        ]
        val = 'Dog'

    elif (flt=='breed'):
        opt = [
            {'label': 'Mixed', 'value': 'mixed'},
            {'label': 'Pure', 'value': 'pure'},
        ]
        val = 'mixed'

    else:
        opt = [
            {'label': 'Adopted', 'value': 1},
            {'label': 'Not Adopted', 'value': 0},
        ]
        val = 1
    
    return [
        dcc.Dropdown(
            options=opt,
            value=val,
            id='ddl-filter-val'
            ),
    ]
    

@app.callback(
    Output('tbl-animal', 'figure'), 
    [Input('ddl-filter-val', 'value'), Input('ddl-filter-tbl', 'value')]
)

def filterTable(key, col):
    if (col=='outcome_type'):
        tempDf = animalDf[animalDf['OutcomeType']==key]
    elif (col=='animal_type'):
        tempDf = animalDf[animalDf['AnimalType']==key]
    elif (col=='breed'):
        tempDf = animalDf[animalDf['nBreed']==key]
    elif (col=='adoption'):
        tempDf = animalDf[animalDf['adoption']==key]

    return { 
        'data': [
            go.Table(
                header=dict(values=list(tempDf.columns),
                    fill = dict(color='#C2D4FF'),
                    align = ['center'] * 5
                ),  
                cells=dict(values=[tempDf[col] for col in tempDf.columns], align=['left'])
            )
        ],
        'layout' : go.Layout(
            height=600, margin={'t': 10}, width=900
        )
    }

if __name__ == '__main__': 
    app.run_server(debug=True, port = 2828)