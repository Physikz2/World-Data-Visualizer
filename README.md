![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)


# 🌍 World Data Visualizer

An interactive, single-page data dashboard that visualizes global socio-economic metrics on a dynamic world map. Built with Python and Flask, this app renders interactive, color-coded choropleth maps in seconds by reading from a local pre-downloaded CSV file.

---

## 🌐 Live Demo

You can view and interact with the live app right now, hosted entirely on the web:

👉 **[https://world-data-visualizer.onrender.com](https://world-data-visualizer.onrender.com)**

*(Note: Site is hosted on Render's free tier, so it may take up to 30 seconds to wake up on the first visit. After the initial wake-up, everything runs instantly).*

---

## 📊 Features

- **Three Metrics:** Choose from Population, GDP per Capita, or Life Expectancy.
- **Dynamic Year Selection:** Select any year from 1960 to 2026.
- **Interactive Visualization:** Hover over any country to see its exact data value.
- **Custom Color Gradients:** Pick from a dropdown menu of 9 different color scales (Viridis, Plasma, Magma, Blues, etc.).
- **Live Console:** Built-in terminal-style log that streams country data in real-time.
- **Full-Stack Architecture:** Python/Flask backend with a responsive HTML/JS frontend.

---

## 🛠️ Tech Stack & How It's Used

| Technology | Badge | Role in the Project |
| :--- | :--- | :--- |
| **Python** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | Primary backend language. Handles data loading, filtering, caching, and routing logic for the entire application. |
| **Flask** | ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) | Lightweight web framework used to serve the dynamic HTML pages and handle HTTP requests from the browser. |
| **Plotly Express** | ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white) | Data visualization library used to generate the interactive choropleth world maps with custom color gradients. |
| **Pandas** | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) | Used to load and filter the local 2.3 MB CSV file. Fast filtering of 66 years of data across 3 metrics. |
| **HTML5** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) | Structure of the sidebar layout, control panels, and the live console interface. |
| **CSS3** | ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) | Responsive styling for the split-view layout, sidebar cards, and interactive console window. |
| **JavaScript** | ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) | Handles the frontend logic: sending fetch requests to Flask, updating the map iframe, and powering the live console stream. |
| **Render** | ![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black) | Cloud hosting platform used to deploy the live production app. Automatically builds from the GitHub repo and serves the global demo. |

---

## 🚀 How to Run Locally

1. Clone the repository: `git clone https://github.com/Physikz2/World-Data-Visualizer.git`
2. Install dependencies: `pip install flask plotly pandas cachetools gunicorn`
3. Run the app: `python app.py`
4. Open your browser to `http://127.0.0.1:5000`

---

## 💡 A Note on Performance

> **Why is it so much faster now?** 
> 
> Early versions of this app relied on the **live World Bank API**, which frequently caused 30–120 second timeouts and inconsistent hanging. 
> 
> To permanently solve this, I engineered a **local data pipeline**: all metrics (Population, GDP, Life Expectancy) for every country from 1960–2026 were pre-downloaded and stored as a compact 2.3 MB CSV file. 
> 
> Now, the Flask app reads **directly from the local file** instead of making external API calls. The result? **Map generation takes under 0.1 seconds**, while the raw JSON data is preserved in the `/archive` folder for transparency.