# LSi-Team-Vision
Use AI to forecast when shelters will experience high demand, allowing for better resource allocation, with a focus on predicting the number of beds required.

## Project Scope and Requirements

This project aims to develop an advanced forecasting model to predict shelter demand based on various influencing factors. The key objectives include:

- **Forecasting shelter demand** using historical data, weather patterns, and socio-economic indicators.
- **Providing early warnings** for demand surges to help shelters allocate resources effectively.
- **Creating a user-friendly dashboard** for shelters to monitor forecasts, trends, and provide inputs to the model.

  ###  Key Components

- **Data Collection & Preprocessing**
- **Forecasting Model Development**
- **Early Warning System**
- **Dashboard & Visualization**



## Data Sources

The following datasets were used in this project:

### For Toronto:
1. [Daily Shelter Overnight Service Occupancy & Capacity](https://open.toronto.ca/dataset/daily-shelter-overnight-service-occupancy-capacity/)  
2. [Central Intake Calls](https://open.toronto.ca/dataset/central-intake-calls/)

### For Calgary:
1. [Shelter Utilization, Capacity and Usage](https://data.calgary.ca/Services-and-Amenities/Shelter-Utilization-Capacity-and-Usage-/p7ka-hqjn)  
2. [Calgary Emergency Shelters Daily Occupancy](https://data.calgary.ca/Services-and-Amenities/Calgary-Emergency-Shelters-Daily-Occupancy/7u2t-3wxf/about_data)  
3. [Calgary Community Profile](https://data.urbandatacentre.ca/dataset/calgary-community-profile)


  

## Testing/ Model Validation 

To ensure the reliability of the forecasting model, the following testing and validation approaches will be used:

- **Accuracy Measurement**: Compare predicted shelter demand with actual demand to evaluate the model's accuracy.
- **Scenario Testing**: Assess model performance under different conditions, such as extreme weather or seasonal variations.
- **Scalability Analysis**: Test whether the system can be applied to different cities or regions with varying homelessness challenges.
- **Interpretability & Usability**: Ensure stakeholders can easily understand and interpret model predictions and insights.
- **False Prediction Analysis**: Track false positives and negatives (e.g., predicting high demand when it doesn’t occur or missing peak demand).
- **User Feedback & Adoption**: Conduct surveys or interviews with shelter staff and decision-makers to gauge satisfaction with the system’s usability and impact.

## Development Methodology

Agile approach with iterative development and continuous testing



## Project Timeline & Deliverables (Now - May 4)

### **Week 1 (March 18 - March 24)**
- Finalize data sources and define data pipelines.
- Set up data collection mechanisms and integrations.
- Begin exploratory data analysis (EDA) on historical shelter data. (Identify key features)
- Map the date 

### **Week 2 (March 25 - March 31)**
- Implement baseline forecasting models (ARIMA, LSTM, Prophet, etc.) for evaluation.

### **Week 3 (April 1 - April 7)**
- Compare forecasting models and optimize for accuracy.
- Implement additional feature engineering techniques.
- Start developing the early warning system.

### **Week 4 (April 8 - April 14)**
- Train the model further.
- Conduct initial model testing and refinement.

### **Week 5 (April 15 - April 21)**
- Develop API integrations and cloud-based storage for real-time data (if possible).
- Begin designing the dashboard interface and visualization tools.
- Integrate the forecasting model with the dashboard.

### **Week 6 (April 22 - April 28)**
- Develop and test alert mechanisms in the early warning system.
- Conduct initial internal testing and collect feedback.
- Implement final improvements based on testing feedback.
- Finalize dashboard and ensure user-friendliness.

### **Week 7 (April 29 - May 4)**
- Gather user feedback and refine the system.
- Prepare final documentation and user guides.
- Present project outcomes.
