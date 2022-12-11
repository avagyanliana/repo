from dash import Dash, dcc, html, Input, Output, State

import dash

# external CSS stylesheets

app = dash.Dash(__name__, use_pages=True,suppress_callback_exceptions=True)
server=app.server

#image
image_filename = 'CLV.png'

app.layout=html.Div([
    html.Div([
    html.Div([],  id="data-description-container01"),
     html.Div([],  id="data-description-container02"),
        html.Div(
        [
             html.Img(src=app.get_asset_url(image_filename), id = 'clv-image')
        ], className='twelve columns', id = 'clvcontainer'
    ),    



	html.Div([
            dcc.Link(html.Button('Data Description', className="data-description-text4"), href='/page1')
        ], id = 'data-description-button2'),
        html.Hr(),  
   	html.Div([
            dcc.Link(html.Button('CLV', className="data-description-text"), href='/page2')
        ], id = 'data-description-button'),
        html.Hr(),   
	html.Div([
            dcc.Link(html.Button('Model Visuals', className="data-description-text3"), href='/page3')
        ], id = 'data-description-button1'),
        html.Hr(),              



 

	 
    # html.Div([
    #     html.H2("File Browser Upload"),
    #     dcc.Upload(
    #     id="uploadData",
    #     children = html.Div([
    #         html.H2(
    #             "Drag and drop or click to select a file to upload!", style={'text-align':'center'}
    #         ),
    #     ], id="uploadDataPlaceholder", className="twelve columns"), 
    #     multiple = True,      
    #     )

	# 	],   className='twelve columns', id = 'uploadFileTitle'),
	



        # content of each page
    dash.page_container,
    ]),

], className='twelve columns', id='pageWrapper')

if __name__=='__main__':
	app.run_server(debug=True, port=8988)
