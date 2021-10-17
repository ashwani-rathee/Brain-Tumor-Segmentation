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


app = dash.Dash(__name__, external_stylesheets=[
                'https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP, "./test.css"])
server = app.server


app.layout = html.Div([
    dbc.Card([
        html.H1('Annotation Brain Tumor Server'),
        html.P('This is the submission for MHacks21 which provides a tool to annotate brain tumor which is computer aided(the initial mask comes for radiologists).Automatic segmentation of brain tumors from medical images is important for clinical assessment and treatment planning of brain tumors. '),
        html.P(' ')
        
        ], className='divHeader'),
    dbc.Card(
        dbc.Row([dbc.Col(dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='dropdown',
                options=[{'label': i, 'value': i}
                         for i in ['GCP server', 'Heroku Server']],
                value='GCP server'
            )),
            dbc.Col(html.Div(id='display-value')),
            dbc.Col(html.Button('Show Mask', id='button-mask-show')),
            dbc.Col(html.Button('Show Graph', id='button')),
            dbc.Col([html.Button('Save Mask', id='mask-save'),
                     dcc.Download(id="mask-save-index")]),
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

    dbc.Row([
        dbc.Col(html.Button('Image', id='button2', style={'width': '100%'})),
        dbc.Col(html.Button('Mask', id='button3', style={'width': '100%'})),
        dbc.Col(html.Button('Graph', id='button4', style={'width': '100%'})),
    ], className='divmarks'
    ),
    dbc.Row([
        dbc.Col(html.Div(id='output-image-upload', className='div1')),
        dbc.Col(html.Div(id='mask-image-upload'), className='div1'),
        dbc.Col(html.Div(id='graph'), className='div1'),
    ], className='divbig', no_gutters=True
    ),
    dbc.Row([
        dbc.Col(html.Button(html.A('Github', href='https:/github.com', target="_blank"), id='button5', style={'width': '100%'})),
        dbc.Col(html.Button(html.A('Devpost', href='https:/github.com', target="_blank"), id='button6', style={'width': '100%'})),
        dbc.Col(html.Button(html.A('Linkedin', href='https:/github.com', target="_blank"), id='button7', style={'width': '100%'})),
        dbc.Col(html.Button(html.A('Youtube Vid', href='https:/github.com', target="_blank"), id='button8', style={'width': '100%'})),
    ], className='divfooter'
    ),

])

@app.callback(Output("mask-save-index", "data"), Input("mask-save", "n_clicks"))
def func(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        return dcc.send_file(
        "./mask.png"
    )
    
# @app.callback(Output("graph-save-index", "data"), Input("graph-save", "n_clicks"))
# def func2(n_clicks):
#     print("Here")
#     if n_clicks:
#         print("Her1")
#         if n_clicks is None:
#             raise dash.exceptions.PreventUpdate
#         else:
#             return dcc.send_file(
#             "./graph.png"
#         )
#     return ' '
    
def parse_contents(contents, filename, date, x):
    global mask
    data = contents[contents.find(','):-1]+'=='
    imgdata = np.array(Image.open(io.BytesIO(base64.b64decode(data))))
    sio.imsave('img.png', imgdata)
    if x =="GCP server":
        resp = requests.post("https://brain-tumor-segment-api.as.r.appspot.com/predict",
                            files={"file": open('img.png', 'rb')})
    else:
        resp = requests.post("https://brain-segment-api.herokuapp.com/predict",
                            files={"file": open('img.png', 'rb')})
    json_load = resp.json()
    mask = ~np.asarray(json_load["mask"])
    sio.imsave('mask.png', mask)
    print("mask updated")
    return html.Div([
        html.Img(src=contents),
        html.Hr(),
        html.P("Filename: " + filename),
        html.P("Time of Upload: " + str(datetime.datetime.fromtimestamp(date))),
    ], className='divimg')


@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'),State('dropdown', 'value'))
def update_output(list_of_contents, list_of_names, list_of_dates,data):
    print(data)
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d, x) for c, n, d, x in
            zip(list_of_contents, list_of_names, list_of_dates,data)]
        return children


@app.callback(Output('mask-image-upload', 'children'),
              [Input('button-mask-show', 'n_clicks')], State('upload-image', 'contents'))
def show_mask(n_clicks, contents):
    if n_clicks:
        filename = "mask.png"
        with open("mask.png", "rb") as image_file:
            contents = "data:image/png;base64, " + \
                str(base64.b64encode(image_file.read()))[2:-1]
        return html.Div([
            html.Img(src=contents),
            html.Hr(),
            html.P("Filename: " + filename),
            # html.Div('Raw Content'),
            # html.Pre(contents[0:50] + '...', style={
            #     'whiteSpace': 'pre-wrap',
            #     'wordBreak': 'break-all'
            # })
        ], className='divmask')
    return ''


@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


@app.callback(
    dash.dependencies.Output('graph', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')], State('upload-image', 'contents'))
def update_output1(n_clicks, list_of_contents):
    if n_clicks:
        contents = list_of_contents[0]
        data = contents[contents.find(','):-1]+'=='
        imgdata = np.array(Image.open(io.BytesIO(base64.b64decode(data))))
        fig = px.imshow(imgdata)
        resp = requests.post("https://vectorization-server.herokuapp.com/tosvg",
                             files={"file": open('mask.png', 'rb')})
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
        return [dcc.Graph(figure=fig,config={'modeBarButtonsToAdd':['drawline',
                                            'drawopenpath',
                                            'drawclosedpath',
                                            'drawcircle',
                                            'drawrect',
                                            'eraseshape'
                                           ]}, className='divgraph',)]
    return ''


if __name__ == '__main__':
    app.run_server(debug=True)
