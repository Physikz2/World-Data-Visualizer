# 🌍 World Data Visualizer

An interactive, single-page data dashboard that visualizes global socio-economic metrics on a dynamic world map. Built with Python and Flask, this app fetches live data from the World Bank API and renders interactive, color-coded choropleth maps in seconds.

---

## 🌐 Live Demo

You can view and interact with the live app right now, hosted entirely on the web:

👉 **[https://world-data-visualizer.onrender.com](https://world-data-visualizer.onrender.com)**

*(Note: The free hosting service may take up to 30 seconds to wake up on the first visit).*

---

## 📊 Features

- **Live Data Integration:** Fetches real-time data from the World Bank API.
- **Three Metrics:** Choose from Population, GDP per Capita, or Life Expectancy.
- **Dynamic Year Selection:** Select any year from 1960 to 2026.
- **Interactive Visualization:** Hover over any country to see its exact data value.
- **Full-Stack Architecture:** Python/Flask backend with a responsive HTML/JS frontend.

---

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **Backend:** Flask
- **Data Visualization:** Plotly Express
- **Data Source:** World Bank API (via `pandas_datareader`)
- **Frontend:** HTML, CSS, JavaScript
- **Hosting:** Render (Cloud Server)

---

## 🚀 How to Run Locally


## 🚀 How to Run Locally
1. Clone the repository: `git clone https://github.com/Physikz2/World-Data-Visualizer.git`
2. Install dependencies: `pip install flask plotly pandas pandas_datareader gunicorn`
3. Run the app: `python app.py`
4. Open your browser to `http://127.0.0.1:5000`