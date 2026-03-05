Uber Urban Mobility & Fare Dynamics Analysis

Strategic Business Intelligence

📋 Executive Summary

This project delivers an end-to-end Business Intelligence solution analyzing Uber's trip data to identify patterns in urban mobility, fare fluctuations, and driver utilization.
By leveraging Power BI and Advanced DAX, the dashboard transforms raw transactional data into strategic insights aimed at optimizing surge pricing strategies and improving fleet distribution across high-demand zones.

🎯 Business Objectives
Revenue Optimization: Analyze fare distribution to identify underpriced routes or high-value time windows.
Demand Forecasting: Visualize peak demand periods to assist in driver supply-side planning.
Geospatial Intelligence: Map trip density to identify "Hot Zones" for targeted marketing and driver incentives.
Operational Efficiency: Segment trips by passenger count and distance to evaluate vehicle type performance.

🛠️ Technical Methodology (ETL & Modeling)
A. Data Extraction & Transformation (Power Query):
Handled missing GPS coordinates and anomalous fare values (outliers).

B. Engineered features:
- Day of Week
- Hour
- Dynamic Measure of Total Transaction, Total Booking Values, Total Trip Distance
- Average Booking Values, Varate Trip Distance, and Averate Trip Time
- Most Frequent Pickup and Dropoff location

C. Data Modeling:
Implemented a Star Schema with a dedicated Calendar Dimension and Geography Dimension for optimized filtering performance.
Trip Details Table as Fact Table
Calendar Table and Location Table as Dimension

Analytical Calculations (DAX):
Developed complex measures including Total Transaction, Total Booking Values, Total Trip Distance, Average Booking Values, Varate Trip Distance, and Averate Trip Time and Peak Hour Frequency.

📊 Key Business Insights
Peak Demand Volatility: Analysis revealed a significant increase in demand during Saturday (13 AM - 18 PM), suggesting a need for dynamic surge adjustments.
Trip Time: Around 72.8% of the trip done on day time.
Geospatial Concentration: Most transaction takes pickup point at Penn Station/Madison Sq West and dropoff point at Upper East Side North.
Payment Method: Around 67.03% of transactions by Uber Pay and 32.23% by Cash.
Favorable Vehicle:  UberX is the most favorite car with 37.3% of bookings and also earn the most revenue.

🖥️ Dashboard Preview
[Optional: Link to Interactive Portfolio - e.g., NovyPro/PowerBI Service]

(Insert your high-resolution screenshot here)

📂 Repository Structure

├── Data/                   # Raw and cleaned datasets (CSV/Excel)
├── Documentation/          # Data Dictionary and project requirements
├── PowerBI/                # Main .pbix dashboard file
└── README.md               # Project documentation


🚀 How to Replicate

Clone the repository: git clone https://github.com/yourusername/uber-analysis.git

Ensure you have Power BI Desktop (latest version) installed.

Open Uber_Dashboard.pbix in the /PowerBI folder.

(Optional) Refer to the /Data folder to view the source transformation steps.

👤 Author

Oimolala Putrawan
Data Scientist & Business Intelligence Enthusiast

Education: Mechanical Engineering, Universitas Indonesia (UI)

LinkedIn: linkedin.com/in/yourprofile

Portfolio: [Link to your website/NovyPro]
