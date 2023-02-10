import time
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import base64
import datetime
import io
import plotly.graph_objs as go
import cufflinks as cf
from dash import dash_table
import dash_bootstrap_components as dbc
import skimage.io as sio
import base64
from PIL import Image
import numpy as np
import requests
import pandas as pd
from skimage import data
import xml.etree.ElementTree as ET
img = data.chelsea()  # or any image represented as a numpy array
mask = np.zeros((512, 512))

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP, "./test.css"])
server = app.server

app.layout = html.Div([
    dbc.Card(
        dbc.Row([        dbc.Col([html.H1('Annotation Brain Tumor Server')]),
        dbc.Col([html.P('This is the submission for MHacks21 which provides a tool to annotate brain tumor which is computer aided(the initial mask comes for radiologists).Automatic segmentation of brain tumors from medical images is important for clinical assessment and treatment planning of brain tumors. '),])
]), className='divHeader'),
    dbc.Card(
        dbc.Row([dbc.Col(dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='dropdown',
                options=[{'label': i, 'value': i}
                         for i in ['GCP server', 'Heroku Server', 'Local Server']],
                value='Local Server'
            )),
            dbc.Col(html.Div(id='display-value')),
            # dbc.Col(html.Button('Show Mask', id='button-mask-show')),
            # dbc.Col(html.Button('Show Graph', id='button')),
            dbc.Col([html.Button('Save Mask', id='mask-save'), dcc.Download(id="mask-save-index")]),
            # dbc.Col([html.Button('Save Graph', id='graph-save'),
            #          dcc.Download(id="graph-save-index")]),
        ]),), dbc.Col(dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'padding':'10px',
                'width': 'auto',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'height':'35px',
            },
            multiple=True
        ),)]),
        className="buttons"
    ),
    # dbc.Card(
    #     [dbc.Row([
    #     dbc.Col([dbc.Row([html.P("Image")]), dbc.Row(html.Div(id='output-image-upload'))], className='divImg1'),
    #     dbc.Col([dbc.Row([html.P("Mask")]), dbc.Row(html.Div(id='mask-image-upload'))], className='div2'),
    #     dbc.Col([dbc.Row([html.P("Graph")]), dbc.Row(html.Div(id='graph'))], className='div3'),
    # ]
    # )], className='div4'),
    
    dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col([dbc.Row([dbc.Button(html.A('Image')), html.Div(html.Img(id='output-image-upload', style={'height':'10%', 'width':'10%'}))], className="h-50" ), dbc.Row([dbc.Button(html.A('Mask')), html.Div(html.Img(id='mask-image-upload', style={'height':'10%', 'width':'10%'}))], className="h-50")], width=3),
                dbc.Col([dbc.Row([dbc.Button(html.A('Graph'))]), dbc.Row(html.Div(html.Img(id='graph', style={'height':'10%', 'width':'10%'})))]),
            ],
            className="g-0",
        )
    ], className='div4'),
    dbc.Card(
        [dbc.Row([
        dbc.Col(html.Button(html.A('Github', href='https:/github.com', target="_blank"), id='button5', style={'width': '100%'})),
        dbc.Col(html.Button(html.A('Devpost', href='https:/github.com', target="_blank"), id='button6', style={'width': '100%'})),
        dbc.Col(html.Button(html.A('Linkedin', href='https:/github.com', target="_blank"), id='button7', style={'width': '100%'})),
        dbc.Col(html.Button(html.A('Youtube Vid', href='https:/github.com', target="_blank"), id='button8', style={'width': '100%'})),
    ]
    )], className='divfooter'),

])

@app.callback(Output("mask-save-index", "data"), Input("mask-save", "n_clicks"))
def func(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        return dcc.send_file(
        "./mask.png"
    )

def parse_contents(contents, filename, date, x):
    global mask
    data = contents[contents.find(','):-1]+'=='
    imgdata = np.array(Image.open(io.BytesIO(base64.b64decode(data))))
    # sio.imsave('img.png', imgdata)
    if x =="GCP server":
        resp = requests.post("https://julia-braintumorseg.et.r.appspot.com/predict",
                            files={"file": open('img.png', 'rb')})
    elif(x == "Heroku Server"):
        resp = requests.post("https://brain-segment-api.herokuapp.com/predict",
                            files={"file": open('img.png', 'rb')})
    else:
        resp = requests.post("http://localhost:5000/predict", files={"file": open('img.png', 'rb')})
        
    json_load = resp.json()
    mask = ~np.asarray(json_load["mask"])
    # sio.imsave('mask.png', mask)
    print("mask updated")
    return [html.Div([
        html.Img(src=contents),
    ], className='divimg')], mask


@app.callback(Output('output-image-upload', 'children'), Output('mask-image-upload', 'children'), Output('graph', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'),State('dropdown', 'value'))
def update_output(list_of_contents, list_of_names, list_of_dates,data):
    if list_of_contents is not None:
        print(list_of_contents, list_of_names, list_of_dates, data)
        print(data)
        children, mask = parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0], data)
        
        with open("mask.png", "rb") as image_file:
            contents = "data:image/png;base64, " + \
                str(base64.b64encode(image_file.read()))[2:-1]
                
        contents = "data:image/png;base64, " + str(base64.b64encode(image_file.read()))[2:-1]
        code3 = html.Div([
            html.Img(src=contents),
            html.Hr(),
        ], className='divmask')
        
        data1 = list_of_contents[0][list_of_contents[0].find(','):-1]+'=='
        imgdata1 = np.array(Image.open(io.BytesIO(base64.b64decode(data1))))
        fig = px.imshow(imgdata1)
        resp = requests.post("http://localhost:3000/tosvg", files={"file": open('mask.png', 'rb')})
        json_load = resp.json()
        a_restored = np.asarray(json_load["output"])
        root = ET.fromstring("""<?xml version="1.0"?>"""+str(a_restored))
        fig.add_shape(editable=True, type="path",
                      path=root.attrib["d"]+" Z",
                      line_color="SkyBlue", line_width=5)

        fig.update_layout(
            dragmode='drawrect',  # define dragmode
            newshape=dict(line_color='cyan'))
        fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20), width=700, height=500)
        
        code4 =  [dcc.Graph(figure=fig,config={'modeBarButtonsToAdd':['drawline',
                                            'drawopenpath',
                                            'drawclosedpath',
                                            'drawcircle',
                                            'drawrect',
                                            'eraseshape'
                                           ]}, className='divgraph',)]
        return children, code3, code4


@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
