import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os
# get current working directory
cwd = os.getcwd()

#get files in directory
files = os.listdir(cwd) 

print(files)
df = pd.read_csv('data3.csv')
df['Power (W)'] = df['Power (W)']*1e3
df.rename({'Power (W)': 'Power (mW)'}, axis=1, inplace=True)
df.rename({'Area (um2)': 'Area (um<sup>2</sup>)'}, axis=1, inplace=True)

df['AT (um2-ps)'] = df['Area (um<sup>2</sup>)']*df['Timing (ps)']
df['PDP (fJ)'] = df['Power (mW)']*df['Timing (ps)']
print(df)
df = df.drop(df[(df['Decoder Design Style'] == "4. Latched-Output Decoder") & (df['Decoder Design Style'] == "5. SIPO Decoder")].index)

import plotly.express as px
hover_text = df.apply(lambda row: f"{row['Decoder Design Style']} (Area: {row['Area (um<sup>2</sup>)']})", axis=1)

fig6 = px.line(df, x="Output Lines", y="PDP (fJ)", color='Decoder Design Style', text="Input", template="plotly_white",  
              markers=True, symbol="Decoder Design Style",
              hover_name="Decoder Design Style",
              hover_data={
                  "Decoder Design Style":False,
                  "Output Lines":False,
                  "Input Lines":True,
                  "Input": False})

fig6.update_traces(textposition='middle right')
fig6.update_layout(
    font= dict(
    size = 20, 
    family = 'Helvetica Neue, sans-serif',
    color="black"

), 
    width=750,
    height=550,
    template="plotly_white",
    xaxis=dict(
        title='WL-bit Output Decoder ',  # X-axis title
        showgrid=True,  # Show gridlines on the x-axis
        gridcolor='lightgray',  # Set gridline color
        showline=True,  # Show x-axis line
        linewidth=2,  # Set x-axis line width
        linecolor='black',  # Set x-axis line color
        tickmode = 'array',
        tickvals = [4,8,16,32,64,128,],
    ),
    yaxis=dict(
        title='PDP (<i>fJ</i>)',  # Y-axis title
        showgrid=True,  # Show gridlines on the y-axis
        gridcolor='lightgray',  # Set gridline color
        showline=True,  # Show y-axis line
        linewidth=2,  # Set y-axis line width
        linecolor='black',  # Set y-axis line color
    ),
     # Show the legend at the bottom of the graph
    legend=dict(
        orientation="h",
        yanchor='bottom',  # Anchor the legend to the bottom
        y=-0.7,
        xanchor="right",
        x=1,
         font=dict(
            family="Helvetica",
            size=20,
            color="black"
        ),

    ),
    legend_title_text='',
    legend_itemsizing='trace',

)


#fig6.write_image("pdp2.pdf")
time.sleep(2)
#fig6.write_image("pdp.pdf")
time.sleep(2)
df_spider = df[df["Output Lines"]==64]
df = df.drop(df[(df['Decoder Design Style'] == "1. Traditional Decoder") ].index)

df_spider = df_spider.drop('Input', axis=1)
df_spider = df_spider.drop('Output Lines', axis=1)
df_spider = df_spider.drop('Internal Power', axis=1)
df_spider = df_spider.drop('Switching Power', axis=1)
df_spider = df_spider.drop('Leakage Power', axis=1)
df_spider = df_spider.drop('PDP (fJ)', axis=1)
df_spider = df_spider.drop('AT (um2-ps)', axis=1)

df_spider['Area (um<sup>2</sup>)']=(df_spider['Area (um<sup>2</sup>)'])/(df_spider['Area (um<sup>2</sup>)'].max())
df_spider['Power (mW)']=(df_spider['Power (mW)'])/(df_spider['Power (mW)'].max())
df_spider['Timing (ps)']=(df_spider['Timing (ps)'])/(df_spider['Timing (ps)'].max())
df_spider['Input Lines']=(df_spider['Input Lines'])/(df_spider['Input Lines'].max())

df_spider2=df_spider.melt(id_vars=["Decoder Design Style"],
        var_name="param",
        value_name="value")

fig4 = px.line_polar(df_spider2, r = 'value', theta = 'param', line_close = True,
                    color = 'Decoder Design Style')
fig4.update_traces(fill = 'toself')

fig4.update_layout(
    font= dict(
    size = 14, 
    family = 'Helvetica Neue, sans-serif',
    color="black"

), 
    width=650,
    height=550,
   
     # Show the legend at the bottom of the graph
    legend=dict(
        orientation="h",
        yanchor='bottom',  # Anchor the legend to the bottom
        y=-0.27,
        xanchor="right",
        x=1,
        font=dict(
            family="Helvetica",
            size=16,
            color="black"
        ),
        title=dict(
            font=dict(
                family="Helvetica",
                size=16,
                color="black"
            )
        ),
        title_text='Decoder Design Style',

    )

)
#fig4.write_image("spider.pdf")


from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
# Add MathJax script to the HTML layout
app.layout = html.Div([
    html.Script(
        type="text/javascript",
        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML",
    ),
    #dcc.Markdown('# Decoder Design Analysis', style={'textAlign': 'center'}, className='mb-3'),
    dbc.Row([
   

        dbc.Col([
            dcc.Graph(figure=fig4, mathjax=True)
        ], width=6),
  
       
    ])
])
app.run_server(debug=True, use_reloader=False)
