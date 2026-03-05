🚖 Uber Urban Mobility & Fare Dynamics Analysis

This project delivers an end-to-end Data Solution—from descriptive analytics to predictive modeling—analyzing Uber's trip data (2009–2015) to identify patterns in urban mobility, fare fluctuations, and driver utilization.

📋 Executive Summary

By leveraging Power BI for historical insights and Machine Learning (XGBoost/LightGBM) for future price prediction, this project transforms raw transactional data into strategic intelligence. The final solution includes an interactive dashboard and a Streamlit web application for real-time fare estimation.

🎯 Business Objectives

Revenue Optimization: Identify underpriced routes and high-value time windows.

Demand Forecasting: Visualize peak periods to assist in driver supply-side planning.

Geospatial Intelligence: Map "Hot Zones" for targeted marketing and driver incentives.

Fare Accuracy: Provide precise fare estimates to improve customer trust and operational transparency.

🛠️ Technical Methodology

1. Business Intelligence (Power BI & DAX)

ETL: Handled missing GPS coordinates and removed outliers (negative fares, zero coordinates) using Power Query.

Modeling: Implemented a Star Schema with dedicated Calendar and Location dimensions.

Analytics: Developed advanced DAX measures for Peak Hour Frequency, Total Booking Value, and Average Trip Velocity.

2. Data Science Pipeline (Python & Jupyter)

Exploratory Data Analysis (EDA): Discovered high correlations between distance and fare, and identified seasonal trends in trip volume.

Feature Engineering:

Geospatial: Calculated Haversine distance and Manhattan Distance from pickup/dropoff coordinates.

Clustering area: Extracting borough of pickup and dropoff trip from pickup/dropoff coordinates

Airport Trip: Identify airport trip from dataset to determine fix fare to airport.

Temporal: Extracted Hour, Day, Month, Year, Day of Week, and Rush Hour Period.

Modeling: Evaluated 5 algorithms. The XGBoost and LightGBM models emerged as winners, further optimized through hyperparameter tuning.

3. Model Deployment (Streamlit)

Integrated the trained LightGBM and XGBoost model into a user-friendly interface.

Allows users to input trip details and receive an instant fare estimate.


📊 Key Business Insights

1. Peak Demand: Demand spikes significantly on Saturdays (1 PM - 6 PM), suggesting a need for dynamic surge pricing.

2. Daytime Dominance: ~72.8% of trips occur during daylight hours.

3. Top Corridor: The most frequent route is from Penn Station/Madison Sq West to the Upper East Side North.

4. Preferred Service: UberX accounts for 37.3% of bookings and is the primary revenue driver.

5. Payment Trends: 67.03% of transactions are via Uber Pay, indicating high digital adoption.

6. Market Demand Growth:
Transaction volume remained remarkably consistent for five years, hovering around the 28,000–30,000 range. This suggests a loyal but stagnant user base during this period. The CAGR of -0.41% confirms that, despite the early peaks, the overall trend in volume was slightly downward

7. Revenue Growth
While transaction growth was flat, revenue grew steadily from 2010 to 2013. The CAGR of 4.67% shows that Uber successfully increased its "Average Revenue Per User" (ARPU) or adjusted its pricing models during this window.

8. Average Fare per Trip Growth
The Average Fare per Trip grew at a Compound Annual Growth Rate (CAGR) of 5.1% over the six-year period. Unlike transaction volume and total revenue, which plummeted in 2015, the average fare per trip actually remained stable and reached its highest point ($12.67) in 2015.


[For detailed analysis can be seen here: https://bit.ly/4bpzB9K]

🚀 How to Replicate

Power BI Dashboard

Clone the repository:

git clone https://github.com/oimolala/uber-fare-prediction-apps/PowerBI


Open PowerBI/Uber_Dashboard.pbix using Power BI Desktop.

Machine Learning & App

Navigate to the directory: cd uber-fare-prediction-apps

Install dependencies:

pip install -r requirements.txt


Run the Streamlit App:

streamlit run app.py


📂 Repository Structure

├── Data/                   # Raw and cleaned datasets (CSV/Excel)
├── Notebooks/              # Jupyter Notebook (EDA, Clustering, XGBoost/LightGBM)
├── PowerBI/                # Main .pbix dashboard file
├── App/                    # Streamlit deployment files
└── README.md               # Project documentation


👤 Author

Oimolala Putrawan
Data Scientist & Business Intelligence Enthusiast

Background: Mechanical Engineering, Universitas Indonesia (UI)

Experience: Ex-Assistant Project and Program Manager at Unilever Indonesia

Connect: https://www.linkedin.com/in/oimolala-putrawan-a00438149/ | https://github.com/oimolala/uber-fare-prediction-apps

Disclaimer: This project uses the Uber Fares Dataset from Kaggle for educational purposes.
