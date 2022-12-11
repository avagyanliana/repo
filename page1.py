import pandas as pd
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
# import matplotlib.pyplot as plt
#from lifelines import CoxPHFitter
#from pandas_profiling import ProfileReport
import datetime as dt
#import plotly.figure_factory as ff
import plotly.express as px
# from lifetimes import BetaGeoFitter
# from lifetimes import GammaGammaFitter
# from lifetimes.plotting import *
# from lifetimes.utils import *
from lifetimes.utils import summary_data_from_transaction_data
# from lifetimes.plotting import plot_probability_alive_matrix
# from lifetimes.plotting import plot_frequency_recency_matrix
# from lifetimes.plotting import plot_period_transactions
# from lifetimes.utils import calibration_and_holdout_data
#from pyecharts.charts import Pie
#from pyecharts import options as opts
import squarify
#import sklearn

import dash

from dash import callback,Input, Output, State, dcc, html

data = pd.read_excel("Dataset.xlsx")
data['InvoiceDate'].agg(['min', 'max'])

fd = data.drop_duplicates()
fd = fd [['Customer ID','Description','InvoiceDate','Invoice','Quantity','Price', 'Country']]
fd = fd[(fd['Quantity']>0)]
fd['TotalPurchase'] = fd['Quantity'] * fd['Price']

Total_Purchase = fd['Quantity'].sum()
Total_Customers = len(fd['Customer ID'].unique())

df_plot_bar = fd.groupby('Description').agg({'TotalPurchase':'sum'}).sort_values(by = 'TotalPurchase', ascending=False).reset_index().head(5)
df_plot_bar['Percent'] = round((df_plot_bar['TotalPurchase'] / df_plot_bar['TotalPurchase'].sum()) * 100,2)
fir_plotbar = px.bar(df_plot_bar, y='Percent', x='Description', title='Top selling products', 
text='Percent', color='Percent')
fir_plotbar.update_traces(texttemplate='%{text:.2s}', textposition='inside')
fir_plotbar.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(1, 0, 0, 0)',
        'xaxis': {'title': 'x-label',
                'visible': False,
                'showticklabels': True},
})
fir_plotbar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',showlegend=False)                
 

fig_date = go.Figure([go.Scatter(x=fd['InvoiceDate'], y=fd['Quantity'])])
 
fig_date.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                    step="day",
                    stepmode="backward"),
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
    )
)


df_plot = fd.groupby(['Country','Description','Price','Quantity', 'InvoiceDate']).agg({'TotalPurchase': 'sum'},{'Quantity':'sum'}).reset_index()
fig_miricle = px.scatter(df_plot[:25000], x="Price", y="Quantity", color = 'Country', 
        size='TotalPurchase',  size_max=20, log_y= True, log_x= True, title= "PURCHASE TREND ACROSS COUNTRIES")
fig_miricle.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(1, 0, 0, 0)',
})


new = summary_data_from_transaction_data(fd, 'Customer ID', 'InvoiceDate', monetary_value_col='TotalPurchase', observation_period_end='2011-12-9')
new.head()

new['percent'] = round((new['frequency'] / new['frequency'].sum()) * 100,2)
fir_plot = px.bar(new, y=new['percent'], x=new['frequency'], title='Frequency BarChart', color='percent')


dash.register_page(
    __name__,
    path='/page1',
    title='Data Description',
    name='Data Description'
)

layout = html.Div([
    html.Div([dcc.Graph(figure=fig_miricle),],  id="data-description-container03"),
    html.Div([dcc.Graph(figure=fir_plotbar),],  id="data-description-container04"),
    html.Div([dcc.Graph(figure=fig_date),],  id="data-description-container05"),
    html.Div([dcc.Graph(figure=fir_plot),],  id="data-description-container06"),
    html.Div([ html.H1('Total Customers: 4315', id = 'data-description-text5'),
             ],  id="data-description-container07"),
    html.Div([html.H1('Total Purchases: 5992601', id = 'data-description-text6'),
             ],  id="data-description-container08"),
    html.Div([dcc.DatePickerRange(id='my-date-picker-range',)
             ],  id="data-description-container09"),

  ], className='twelve columns')


# @callback(
#     Output('output-container-date-picker-range', 'children'),
#     Input('my-date-picker-range', 'start_date'),
#     Input('my-date-picker-range', 'end_date'))

    
# def update_output(start_date, end_date):
#     fd = data.drop_duplicates()
#     fd['InvoiceDate'] = pd.to_datetime(fd['InvoiceDate'], format='%Y-%m-%d')
#     fd = fd.loc[fd["InvoiceDate"].between(*pd.to_datetime([start_date, end_date]))]
#     fd = fd [['Customer ID','Description','InvoiceDate','Invoice','Quantity','Price', 'Country']]
#     fd = fd[(fd['Quantity']>0)]
#     fd['TotalPurchase'] = fd['Quantity'] * fd['Price']
#     df_plot = fd.groupby(['Country','Description','Price','Quantity', 'InvoiceDate']).agg({'TotalPurchase': 'sum'},{'Quantity':'sum'}).reset_index()
#     fig_miricle = px.scatter(df_plot[:25000], x="Price", y="Quantity", color = 'Country', 
#         size='TotalPurchase',  size_max=20, log_y= True, log_x= True, title= "PURCHASE TREND ACROSS COUNTRIES")
#     fig_miricle.update_layout({
#     'plot_bgcolor': 'rgba(0, 0, 0, 0)',
#     'paper_bgcolor': 'rgba(1, 0, 0, 0)',
#     })
#     return fig_miricle