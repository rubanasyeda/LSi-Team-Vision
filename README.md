# 🏠 Forecasting Shelter Demand for the Homeless in Saskatoon

## 📌 Introduction
Homelessness affects over **235,000 Canadians each year**, and Saskatoon has seen its homeless population **triple since 2022**. With increasing pressure on shelter systems from extreme weather and capacity limitations, proactive resource planning is urgently needed. Unfortunately, Saskatoon lacks open-access data on shelter occupancy, making direct forecasting difficult. This project addresses that gap by using data from Toronto and Calgary to train predictive models that can eventually be adapted to Saskatoon's needs.

## 🎯 Objective
The goal of this project was to **build a predictive model** to forecast shelter bed occupancy in Saskatoon, using comparable data from other Canadian cities. We aimed to assess the feasibility of **AI-driven forecasting** for homelessness resource planning in the absence of local data.

## 🔍 Approach & Methodology
We collected and analyzed the following:
- **Shelter occupancy data** (2021–2025) from Toronto and Calgary
- **Weather data**: max/min temperature, precipitation, snow on ground
- **Economic indicators**: inflation rate change, unemployment rate, and Consumer Price Index (CPI)

### Models Developed:
- **Random Forest**: for capturing nonlinear feature interactions
- **Prophet (by Meta)**: a time-series model with built-in seasonality analysis
- **LSTM (Long Short-Term Memory)**: for modeling sequential, multivariate time-series data

## 📊 Results
Among all models, **Multivariate LSTM** showed the best performance:
- **Mean Absolute Error (MAE):** ~0.83  
- **Mean Root Squared Error (MRSE):** ~1.0  

These results demonstrate that shelter demand can be forecasted with reasonable accuracy using historical and environmental trends, even when relying on proxy data.

## 🔮 Future Work & Conclusion
Our next steps include:
- **Integrating Saskatoon-specific shelter data**
- Adding features like **wind chill**, **event-based surges**, and **program usage**
- Partnering with local shelters for **domain feedback and validation**
- Enabling **early-warning systems** for shelter operators

This project highlights the potential of machine learning models to enhance data-driven planning for homelessness services, paving the way for smarter, more responsive systems in the future.

---

## 📂 Data Sources

The following datasets were used in this project:

### For Toronto:
1. [Daily Shelter Overnight Service Occupancy & Capacity](https://open.toronto.ca/dataset/daily-shelter-overnight-service-occupancy-capacity/)  
2. [Central Intake Calls](https://open.toronto.ca/dataset/central-intake-calls/)

### For Calgary:
1. [Shelter Utilization, Capacity and Usage](https://data.calgary.ca/Services-and-Amenities/Shelter-Utilization-Capacity-and-Usage-/p7ka-hqjn)  
2. [Calgary Emergency Shelters Daily Occupancy](https://data.calgary.ca/Services-and-Amenities/Calgary-Emergency-Shelters-Daily-Occupancy/7u2t-3wxf/about_data)  
3. [Calgary Community Profile](https://data.urbandatacentre.ca/dataset/calgary-community-profile)

---

## 🛠️ Tech Stack
- Python (Pandas, NumPy, Scikit-learn, TensorFlow/Keras, Prophet)
- Jupyter Notebooks
- Google Colab
- GitHub for version control

---

## 📁 Repository Structure






## Project Timeline & Deliverables (Now - May 4)

### **Week 1 (March 18 - March 24)**
- Identify Blockers and Key Components.
- Work on Data collection. 


### **Week 2 (March 25 - March 31)**
- Finalize data sources and define data pipelines.
- Research baseline models

### **Week 3 (April 1 - April 7)**
- Create Datasets
- Begin exploratory data analysis (EDA) on historical shelter data. (Identify key features)
- Further analyze data to understand trends.
- Implement baseline forecasting models for evaluation.


### **Week 4 (April 8 - April 14)**
- Conduct model testing.
- Meeting with AI RBC Researcher for Deep Learning Model Selection. 


### **Week 5 (April 15 - April 21)**
- Implement a Deep Learning Model.
- Begin designing the dashboard interface and visualization tools.
- Integrate the forecasting model with the dashboard.

### **Week 6 (April 22 - April 28)**
- Conduct testing and collect feedback.
- Prepare final documentation and user guides.
- Prepare for final presentation. 


### **Week 7 (April 29 - May 4)**
- Gather user feedback and refine the system.
- Present project outcomes.
- Meeting with the Marketing team - May 3


