# Client-Segment: Bank Customer Segmentation Platform

A professional full-stack web application for bank customer segmentation and analysis using unsupervised machine learning (PCA + K-Means Clustering).

## 🎯 Overview

Client-Segment is a complete data analysis platform that helps banks identify, visualize, and profile customer segments to generate actionable marketing recommendations. Built with **Reflex** (Python full-stack framework), it provides an intuitive interface for the entire segmentation workflow.

## ✨ Features

### 📊 Complete Data Pipeline
- **CSV Upload**: Drag-and-drop interface for bank customer data
- **Data Cleaning**: 4-step iterative process (Control → Diagnose → Treat → Report)
- **PCA Analysis**: Dimensionality reduction with explained variance visualization
- **K-Means Clustering**: Optimal cluster selection using Elbow & Silhouette methods
- **Customer Profiling**: Detailed statistics per customer segment
- **Marketing Insights**: AI-generated recommendations per segment

### 🎨 Modern UI/UX
- Clean, professional SaaS-style interface
- Responsive design (desktop, tablet, mobile)
- Interactive charts and visualizations (Recharts)
- Smooth transitions and hover effects
- Color-coded cluster identification

### 📈 Advanced Analytics
- Principal Component Analysis (PCA) with variance decomposition
- Elbow Method for optimal cluster selection
- Silhouette Score analysis
- Multi-dimensional customer profiling
- Segment comparison visualizations (Radar charts, Bar charts, Pie charts)

### 💾 Export Capabilities
- Download cleaning logs (TXT)
- Export cluster summaries (CSV)
- Generate full marketing insights reports (CSV)

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (or download the code)
   bash
   cd client-segment
   

2. **Install dependencies**
   bash
   pip install -r requirements.txt
   

3. **Initialize Reflex**
   bash
   reflex init
   

4. **Run the application**
   bash
   reflex run
   

5. **Open your browser**
   Navigate to: `http://localhost:3000`

## 📁 Dataset Format

Your CSV file should contain the following columns:

csv
Monthly Income (€),Savings Amount (€),Credit Balance (€),Monthly Card Spending (€),Age,Bank Seniority (years)
3500.00,15000.00,5000.00,800.00,35,5
4200.00,25000.00,3000.00,1200.00,42,10
...


### Required Columns:
- `Monthly Income (€)` - Customer's monthly income in euros
- `Savings Amount (€)` - Total savings amount
- `Credit Balance (€)` - Outstanding credit balance
- `Monthly Card Spending (€)` - Average monthly card spending
- `Age` - Customer age
- `Bank Seniority (years)` - Years as a bank customer

### Sample Data
A sample dataset (`bank_customers.csv`) is included in the `assets/` folder with 200 customer records for testing.

## 🔄 Usage Workflow

### Step 1: Upload Data
1. Navigate to the **Home** page
2. Drag and drop your CSV file or click to browse
3. Wait for file validation and preview

### Step 2: Data Cleaning
1. Click **"Start Cleaning"** on the upload confirmation
2. Review cleaning summary metrics:
   - Total rows processed
   - Missing values handled
   - Outliers corrected
   - Duplicates removed
3. Download cleaning log for audit trail
4. Proceed to **"Run PCA Analysis"**

### Step 3: PCA Analysis
1. View explained variance per component
2. Examine cumulative variance chart
3. Analyze component contributions table
4. Visualize customer distribution (PC1 vs PC2)
5. Proceed to **"Go to Clustering"**

### Step 4: Clustering
1. Click **"Compute Elbow Method"** to see optimal k
2. Review Elbow plot (Inertia) and Silhouette scores
3. Select number of clusters (k = 2-10)
4. Click **"Run K-Means with k=X"**
5. View color-coded cluster scatter plot
6. Proceed to **"View Customer Profiles"**

### Step 5: Customer Profiles
1. Review detailed statistics per cluster:
   - Average income, savings, credit
   - Average spending, age, seniority
2. Filter by specific clusters
3. Download cluster summary (CSV)
4. Click **"Generate Marketing Insights"**

### Step 6: Marketing Insights
1. View segment distribution pie chart
2. Review KPI dashboard:
   - Total customers analyzed
   - Number of segments identified
   - Average segment size
3. Explore detailed insight cards per segment:
   - Descriptive segment name
   - Top 3 KPIs
   - 3-5 marketing recommendations
4. Download full insights report (CSV)

## 🏗️ Architecture

### Project Structure

app/
├── app.py                  # Main app with routing and layout
├── state.py                # Global state management
├── components/
│   ├── navbar.py          # Top navigation bar
│   ├── card.py            # Metric and insight cards
│   ├── charts.py          # Recharts visualizations
│   └── datatable.py       # Data table component
├── pages/
│   ├── home.py            # Upload page
│   ├── data_cleaning.py   # Cleaning results
│   ├── pca_analysis.py    # PCA visualizations
│   ├── clustering.py      # Clustering analysis
│   ├── customer_profiles.py  # Segment profiles
│   └── insights.py        # Marketing insights
└── utils/
    ├── cleaning_pipeline.py  # Data cleaning logic
    ├── pca_utils.py          # PCA computation
    ├── clustering_utils.py   # K-Means clustering
    └── insights_utils.py     # Insights generation


### Technology Stack
- **Framework**: Reflex (Python full-stack)
- **Data Processing**: pandas, numpy
- **Machine Learning**: scikit-learn, scipy
- **Visualization**: Recharts (via Reflex)
- **Styling**: Tailwind CSS
- **Font**: Lora (Google Fonts)

## 📊 Customer Segment Types

The application automatically identifies and names segments based on characteristics:

1. **Premium Savers** - High income + High savings
   - Wealth management services
   - Investment products
   - Exclusive rewards

2. **Active Spenders** - High spending + Low savings
   - Savings automation
   - Cashback credit cards
   - Financial planning

3. **Young Professionals** - Young age + Low seniority
   - Digital banking features
   - Starter accounts
   - Credit building products

4. **Loyal Veterans** - High age + High seniority
   - Loyalty rewards
   - Retirement planning
   - Premium customer service

5. **Credit Dependent** - Low income + High credit
   - Debt consolidation
   - Financial literacy programs
   - Budget management tools

## 🎨 Design System

### Colors
- **Primary**: Indigo (#6366F1)
- **Secondary**: Gray (#71717A)
- **Success**: Green (#10B981)
- **Warning**: Orange (#F59E0B)
- **Error**: Red (#EF4444)

### Cluster Colors (9 distinct colors)
- Indigo, Emerald, Rose, Amber, Purple, Cyan, Pink, Lime, Sky

### Typography
- **Font Family**: Lora
- **Display**: 48-72px, tight tracking
- **Headline**: 24-32px
- **Body**: 14-16px, 1.5-1.6 line height

## 🔧 Configuration

### Tailwind CSS Plugin
The app uses `TailwindV3Plugin` configured in `rxconfig.py`:

config = rx.Config(app_name="app", plugins=[rx.plugins.TailwindV3Plugin()])


### Font Integration
Google Fonts (Lora) is loaded via head components in `app.py`.

## 📝 Data Cleaning Pipeline

### 4-Step Process:

1. **Control**: Detect missing values, duplicates, data types
2. **Diagnose**: Identify outliers using Z-score (threshold=3)
3. **Treat**: 
   - Fill missing values with median
   - Cap outliers at 3 standard deviations
   - Remove duplicate rows
4. **Report**: Generate comprehensive cleaning log

## 🧪 Testing

Test the application with the included sample dataset:
bash
# The sample file is located at:
assets/bank_customers.csv


This file contains:
- 200 customer records
- 7 missing values (intentional)
- 2 outliers (intentional)
- All 6 required columns

## 🚀 Deployment

To deploy the application:

1. **Build for production**
   bash
   reflex export
   

2. **Deploy to your preferred platform**
   - Reflex Hosting
   - Docker container
   - Cloud platforms (AWS, GCP, Azure)

## 📄 License

This project is provided as-is for educational and commercial use.

## 🤝 Support

For issues, questions, or contributions:
- Review the code documentation
- Check the Reflex documentation: https://reflex.dev
- Test with the provided sample dataset first

## 🎓 Credits

Built with:
- **Reflex** - Python full-stack framework
- **scikit-learn** - Machine learning library
- **pandas** - Data manipulation
- **Recharts** - Charting library

---

**Client-Segment** - Professional Bank Customer Segmentation Platform
