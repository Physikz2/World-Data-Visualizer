![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)


# 🌍 World Data Visualizer

An interactive, single-page data dashboard that visualizes global socio-economic metrics on a dynamic world map. Built with Python and Flask, this app fetches live data from the World Bank API and renders interactive, color-coded choropleth maps in seconds.

---

## 🌐 Live Demo

You can view and interact with the live app right now, hosted entirely on the web:

👉 **[https://world-data-visualizer.onrender.com](https://world-data-visualizer.onrender.com)**

*(Note: Site may be slow as it is on a free hosting service and may take up to 30 seconds to wake up on the first visit). 
*(Note: World Bank API has experienced slowdown issues as well - speed improves if cloning repository and running locally).

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
1. Clone the repository: `git clone https://github.com/Physikz2/World-Data-Visualizer.git`
2. Install dependencies: `pip install flask plotly pandas pandas_datareader gunicorn`
3. Run the app: `python app.py`
4. Open your browser to `http://127.0.0.1:5000`