import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
from pandas_datareader import wb
import requests
import time

# Initialize the Dash app
app = dash.Dash(__name__)

# Pre-populate the year dropdown from 1960 to 2026
years_list = [{'label': str(year), 'value': year} for year in range(1960, 2027)]

# --- Fetch a complete Country Code mapping from World Bank ---
print("📡 Loading country code mapping...")
url = "http://api.worldbank.org/v2/country?format=json&per_page=300"
resp = requests.get(url)
data = resp.json()
country_mapping = {}
for item in data[1]:
    if item['region']['value'] != 'Aggregates':
        country_mapping[item['name']] = item['id']

# --- LAYOUT ---
app.layout = html.Div([
    html.Div([
        # Left Sidebar
        html.Div([
            html.H2("🌍 Data Explorer", style={'textAlign': 'center'}),
            html.Hr(),
            
            html.Label("Select Metric:"),
            dcc.RadioItems(
                id='metric-radio',
                options=[
                    {'label': ' Population', 'value': 'population'},
                    {'label': ' GDP per Capita', 'value': 'gdp'},
                    {'label': ' Life Expectancy', 'value': 'life'}
                ],
                value='population',
                style={'marginBottom': '20px'}
            ),
            
            html.Label("Select Year:"),
            dcc.Dropdown(
                id='year-dropdown',
                options=years_list,
                placeholder="Select a year...",
                style={'marginBottom': '20px'}
            ),
            
            html.Button('Generate Map', id='generate-btn', n_clicks=0,
                        style={'width': '100%', 'padding': '10px', 
                               'backgroundColor': '#007bff', 'color': 'white',
                               'border': 'none', 'borderRadius': '5px',
                               'cursor': 'pointer', 'fontSize': '16px'}),
            
            html.Hr(),
            html.Div(id='status-msg', style={'fontSize': '14px', 'color': '#777'})
            
        ], style={'width': '25%', 'padding': '20px', 'backgroundColor': '#f8f9fa', 
                  'height': '100vh', 'boxSizing': 'border-box'}),

        # Right Side (Map)
        html.Div([
            dcc.Graph(id='world-map', 
                      figure=px.choropleth(title="Select a metric and year, then click Generate"),
                      style={'height': '90vh'})
        ], style={'width': '75%', 'padding': '20px', 'boxSizing': 'border-box'})
        
    ], style={'display': 'flex', 'flexDirection': 'row'})
])

# --- CALLBACK 1: (Kept for compatibility, returns pre-filled list) ---
@app.callback(
    Output('year-dropdown', 'options'),
    [Input('metric-radio', 'value')]
)
def update_year_options(metric):
    return years_list

# --- CALLBACK 2: Generate Map on button click with status updates ---
@app.callback(
    [Output('world-map', 'figure'),
     Output('status-msg', 'children')],
    [Input('generate-btn', 'n_clicks')],
    [State('metric-radio', 'value'),
     State('year-dropdown', 'value')]
)
def generate_map(n_clicks, metric, year):
    if not year:
        return px.choropleth(title="Please select a year"), "⚠️ Please select a year."
    
    if metric == 'population':
        indicator, scale, label = 'SP.POP.TOTL', 'Viridis', 'Population'
    elif metric == 'gdp':
        indicator, scale, label = 'NY.GDP.PCAP.CD', 'Plasma', 'GDP per Capita (USD)'
    else:
        indicator, scale, label = 'SP.DYN.LE00.IN', 'Turbo', 'Life Expectancy (Years)'
    
    try:
        # --- SHOW LOADING MESSAGE ---
        loading_fig = px.choropleth(title=f"⏳ Generating {label} for {year}... Please wait.")
        loading_fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        
        # Simulate a tiny delay so the UI updates
        time.sleep(0.1)
        
        # --- FETCH THE DATA ---
        df = wb.download(indicator=indicator, country='all', start=year, end=year)
        df = df.reset_index().dropna(subset=[indicator])
        df.rename(columns={indicator: 'value'}, inplace=True)
        
        # --- MAP COUNTRY NAMES TO ISO CODES ---
        df['iso_alpha'] = df['country'].map(country_mapping)
        df = df.dropna(subset=['iso_alpha'])
        
        # --- GENERATE FINAL MAP ---
        fig = px.choropleth(
            df,
            locations='iso_alpha',
            locationmode='ISO-3',
            color='value',
            hover_name='country',
            color_continuous_scale=scale,
            title=f"{label} ({year})"
        )
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        
        # --- RETURN SUCCESS STATUS ---
        return fig, f"✅ Map generated for {label} ({year})"
        
    except Exception as e:
        return px.choropleth(title="Error loading data"), f"❌ Error: {str(e)}"

# --- RUN THE APP ---
if __name__ == '__main__':
    app.run(debug=True, port=8050)