# 📊 Portfolio Manager

An interactive, cloud-native web application built with Python to analyze market assets, track global economic updates, simulate investment growth, and manage portfolio risk.

🚀 **Live Demo:** [[)](https://ecpuvtezmyzcfy5rwcgzxw.streamlit.app/)
💻 **Author & Developer:** [Marco Avellino](www.linkedin.com/in/marco-avellino-1a0918411)

---

## 🛠️ Tech Stack & Architecture
- **Frontend & Cloud Deployment:** Streamlit Cloud
- **Data Analytics & Statistics:** Pandas, NumPy
- **Financial Data Integration:** Yahoo Finance API
- **Interactive Visualizations:** Plotly (Candlestick, Linear, Pie, and Histogram charts)
- **Compliance & Structure:** Built with professional software engineering standards, including open-source licensing.

---

## 📁 Application Structure & Features

The platform is engineered into **6 specialized dashboards** accessible via the sidebar navigation menu:

### 1. 📊 Titoli e Grafici (Market Intelligence)
- Real-time stock, ETF, and cryptocurrency price tracking.
- **Smart Dynamic Currency Engine:** Automatically detects the asset's native listing market and formats all metrics into the correct currency symbol (**€**, **$**, or local currency).
- Highly responsive Candlestick charting powered by Plotly for professional technical analysis.

### 2. 📰 Notizie di Mercato (Resilient News Streaming)
- Live economic and business updates pulled from international aggregates.
- Built-in network **Fallback Logic** to guarantee 100% server uptime, providing highly structured backup institutional feeds if cloud network restrictions occur.

### 3. 💰 Simulatore Investimenti (Wealth Projection)
- Macroeconomic simulator utilizing compound interest models to project asset growth over custom time horizons.
- Evaluates the feasibility of dollar-cost averaging (PAC) strategies by matching total capital invested against compounding returns.

### 4. ⚖️ Bilanciamento Portafoglio (Asset Allocation Optimizer)
- Interactive asset allocation planner (Stocks, Bonds, Gold, Cash/Crypto) featuring dynamic side-by-side donut charts.
- **Automated Rebalancing Algorithm:** Calculates portfolio drifts in real time and automatically prints precise directional trading indicators (**BUY / SELL** amounts in €) to realign capital with target weights.

### 5. 🧮 Simulatore Fiscale (Italian Capital Gains Tax Simulator)
- Specialized tax module aligned with the **Italian Financial Regulatory Framework**.
- Features calculations based on asset types: **26%** standard tax rate (Equities, ETFs, Crypto) and **12.5%** privileged rate (Government Bonds / White List).
- Supports capital loss offset modeling (**Compensazione delle minusvalenze pregresse**), visualizing the net-of-tax capital distribution via clean visual aids.

### 6. 📉 Ottimizzazione & Rischio (Quantitative Risk Analysis)
- High-level quantitative risk assessment tool for corporate finance and asset management.
- Computes **Annualized Historical Return**, **Annualized Volatility** (Standard Deviation across a 252-day trading window), and the **Sharpe Ratio** to measure risk-adjusted return efficiency.
- Employs dynamic conditional statements to yield automated qualitative grading, paired with mathematical return distribution histograms.

---

## 📜 License
This project is licensed under the terms of the **MIT License**. Feel free to use, modify, and distribute it open-source.
