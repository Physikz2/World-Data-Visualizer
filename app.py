from flask import Flask, render_template_string, request
import pandas as pd
from pandas_datareader import wb
import plotly.express as px
import json
import warnings  # <--- NEW LINE 1: Import warnings

# Initialize the Flask application
app = Flask(__name__)

# Generate the list of years from 1960 to 2026 for the dropdown
years = [str(y) for y in range(1960, 2027)]

# --- LOAD MASTER TABLE FROM JSON FILE ---
# This file contains the 2-letter country codes, 3-letter ISO codes, and full names.
with open('country_codes.json', 'r') as f:
    MASTER_TABLE = json.load(f)

# --- HTML TEMPLATE WITH LIVE CONSOLE ---
# This template contains the sidebar controls, the map iframe, and the console window.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>World Data Explorer</title>
    <script src="https://cdn.plot.ly/plotly-2.27.1.min.js"></script>
    <style>
        body { font-family: system-ui, sans-serif; margin: 0; display: flex; height: 100vh; }
        .sidebar { width: 18%; padding: 20px; background: #f8f9fa; border-right: 1px solid #ddd; }
        .map-container { width: 82%; padding: 20px; }
        .btn { background: #007bff; color: white; padding: 10px; border: none; border-radius: 5px; cursor: pointer; width: 100%; }
        .btn:hover { background: #0056b3; }
        #status { margin-top: 15px; font-weight: bold; }
        #map-div { width: 100%; height: 85vh; border: none; }
        .loader { display: none; text-align: center; margin-top: 20px; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #007bff; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 10px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        /* --- CONSOLE STYLING --- */
        #console-container {
            width: 100%;
            height: 120px;
            overflow-y: scroll;
            background: #1e1e1e;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #333;
            margin-top: 15px;
            display: none;
            white-space: pre-wrap;
            box-sizing: border-box;
        }
        #console-output { margin: 0; }
        .console-line { margin: 2px 0; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>🌍 Data Explorer</h2>
        <hr>
        <label>Select Metric:</label><br>
        <input type="radio" name="metric" value="population" checked> Population<br>
        <input type="radio" name="metric" value="gdp"> GDP per Capita<br>
        <input type="radio" name="metric" value="life"> Life Expectancy<br><br>
        
        <label>Select Year:</label><br>
        <select name="year" style="width:100%; padding:8px; margin-top:5px;">
            {% for year in years %}
                <option value="{{ year }}">{{ year }}</option>
            {% endfor %}
        </select><br><br>
        
        <button class="btn" onclick="generateMap()">Generate Map</button>
        <div id="status"></div>
        <div id="loader" class="loader">
            <div class="spinner"></div>
            Fetching data from World Bank API...
        </div>

        <!-- LIVE CONSOLE WINDOW -->
        <div id="console-container">
            <div id="console-output"></div>
        </div>
    </div>
    
    <div class="map-container">
        <iframe id="map-div" srcdoc="<h3 style='color:#777; text-align:center;'>Select a metric and year, then click Generate</h3>"></iframe>
    </div>

    <script>
        // 1. Render blank map on load
        document.addEventListener('DOMContentLoaded', function() {
            const emptyMap = {
                layout: {
                    title: 'Select a metric and year, then click Generate',
                    geo: { 
                        projection: { type: 'natural earth' }, 
                        showland: true, 
                        landcolor: '#f2f2f2', 
                        showcountries: true, 
                        countrycolor: '#d3d3d3' 
                    },
                    margin: { r: 0, t: 40, l: 0, b: 0 }
                },
                data: [{ type: 'choropleth', locations: [], z: [], text: [] }]
            };
            const mapDiv = document.getElementById('map-div');
            const emptyHtml = `
                <html>
                    <head><script src="https://cdn.plot.ly/plotly-2.27.1.min.js"><\/script></head>
                    <body style="margin:0;">
                        <div id="plot" style="width:100%; height:100%;"></div>
                        <script>
                            Plotly.newPlot('plot', ${JSON.stringify(emptyMap.data)}, ${JSON.stringify(emptyMap.layout)}, {responsive: true});
                        <\/script>
                    </body>
                </html>
            `;
            mapDiv.srcdoc = emptyHtml;
        });

        // 2. Console Logging Helper
        function logToConsole(msg) {
            const consoleContainer = document.getElementById('console-container');
            const consoleOutput = document.getElementById('console-output');
            
            // Show console on first log
            if (consoleContainer.style.display === 'none') {
                consoleContainer.style.display = 'block';
            }
            
            const line = document.createElement('div');
            line.className = 'console-line';
            line.textContent = `> ${msg}`;
            consoleOutput.appendChild(line);
            
            // Auto-scroll to bottom
            consoleContainer.scrollTop = consoleContainer.scrollHeight;
        }

        // 3. Generate Map function
        async function generateMap() {
            const metric = document.querySelector('input[name="metric"]:checked').value;
            const year = document.querySelector('select[name="year"]').value;
            const status = document.getElementById('status');
            const loader = document.getElementById('loader');
            const mapDiv = document.getElementById('map-div');
            const consoleOutput = document.getElementById('console-output');
            
            // Reset UI
            status.innerHTML = "";
            consoleOutput.innerHTML = ""; // Clear previous logs
            document.getElementById('console-container').style.display = 'none';
            loader.style.display = "block";
            mapDiv.srcdoc = "<div class='spinner'></div><br>Loading...";
            
            logToConsole("🚀 Starting data pipeline...");
            logToConsole(`📡 Requesting ${metric} data for year ${year}...`);
            
            const response = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ metric: metric, year: year })
            });
            
            const data = await response.json();
            loader.style.display = "none";
            
            if (data.success) {
                // Stream the country data line by line
                if (data.stream && data.stream.length > 0) {
                    logToConsole(`✅ Received ${data.stream.length} countries. Streaming data:`);
                    for (const item of data.stream) {
                        logToConsole(`   ${item.country} → ${item.value}`);
                    }
                }
                
                logToConsole("🗺️ Rendering interactive map...");
                mapDiv.srcdoc = data.html;
                status.innerHTML = `✅ ${data.label}`;
                logToConsole("✅ Done! Map ready.");
            } else {
                logToConsole(`❌ Error: ${data.error}`);
                status.innerHTML = `❌ ${data.error}`;
                mapDiv.srcdoc = `<h3 style="color:red; text-align:center;">${data.error}</h3>`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, years=years)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    metric = data['metric']
    year = data['year']
    
    if metric == 'population':
        indicator = 'SP.POP.TOTL'
    elif metric == 'gdp':
        indicator = 'NY.GDP.PCAP.CD'
    else:
        indicator = 'SP.DYN.LE00.IN'
    
    try:
        # --- FETCH DATA ---
        # <--- NEW LINE 2: Convert pandas_datareader warnings to exceptions
        warnings.filterwarnings("error", category=UserWarning, module="pandas_datareader")

        try:
            raw = wb.download(indicator=indicator, country='all', start=year, end=year)
        except UserWarning:
            return {
                "success": False, 
                "error": "World Bank API does not have data for that year. Please select a different year."
            }
        
        df = raw.reset_index().dropna(subset=[indicator])
        df.rename(columns={indicator: 'value'}, inplace=True)
        
        # --- MATCH NAMES TO MASTER TABLE ---
        matched_rows = []
        stream_data = []
        for _, row in df.iterrows():
            name = row['country']
            if name in MASTER_TABLE:
                MASTER_TABLE[name]['value'] = row['value']
                matched_rows.append({
                    'iso': MASTER_TABLE[name]['iso'],
                    'name': MASTER_TABLE[name]['name'],
                    'val': row['value']
                })
                # Collect data for the console stream
                stream_data.append({
                    'country': MASTER_TABLE[name]['name'],
                    'value': row['value']
                })
        
        # --- CHECK IF DATA WAS FOUND ---
        if not matched_rows:
            return {
                "success": False, 
                "error": "World Bank API does not have data for that year. Please select a different year."
            }
        
        # --- PLOTLY MAP ---
        fig = px.choropleth(
            pd.DataFrame(matched_rows),
            locations='iso',
            locationmode='ISO-3',
            color='val',
            hover_name='name',
            color_continuous_scale='Viridis',
            title=f"{metric.capitalize()} ({year})"
        )
        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            geo=dict(projection_type='natural earth')
        )
        
        # Return both the HTML map AND the stream data for the console
        return {
            "success": True, 
            "html": fig.to_html(), 
            "label": f"{metric.capitalize()} ({year})",
            "stream": stream_data
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == '__main__':
    app.run(debug=True, port=5000)