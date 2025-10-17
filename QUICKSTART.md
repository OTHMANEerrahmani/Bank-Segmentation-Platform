# Client-Segment Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Run the Application

bash
reflex run


Open your browser to: **http://localhost:3000**

---

### 2. Upload Sample Data

The app includes a pre-generated sample dataset at:

assets/bank_customers.csv


This file contains:
- **200 customer records**
- **6 features**: Monthly Income, Savings Amount, Credit Balance, Card Spending, Age, Bank Seniority
- **7 missing values** (to test cleaning pipeline)
- **2 outliers** (to test outlier detection)

---

### 3. Complete Analysis Workflow

#### Step 1: Upload CSV File
1. Go to **Home** page
2. Drag and drop `bank_customers.csv` or click to browse
3. Click **"Start Cleaning"**

#### Step 2: Review Data Cleaning Results
- View cleaning metrics: rows processed, missing values handled, outliers corrected
- Download cleaning log for audit trail
- Click **"Run PCA Analysis"**

#### Step 3: Analyze PCA Results
- View explained variance chart (how much information each component captures)
- Examine customer distribution scatter plot (PC1 vs PC2)
- Review component contributions table
- Click **"Go to Clustering"**

#### Step 4: Run Clustering
1. Click **"Compute Elbow Method"** to see optimal k recommendation
2. Review elbow plot and silhouette scores
3. Select number of clusters (recommended: k=3 for sample data)
4. Click **"Run K-Means with k=3"**
5. View colored scatter plot showing cluster assignments
6. Click **"View Customer Profiles"**

#### Step 5: Explore Customer Profiles
- Review detailed statistics for each segment
- Filter by specific clusters
- Download cluster summary CSV
- Click **"Generate Marketing Insights"**

#### Step 6: View Marketing Insights
- Review segment distribution pie chart
- Explore insight cards with:
  - Segment names (e.g., "Premium Savers", "Young Professionals")
  - Top 3 KPIs per segment
  - 3-5 marketing recommendations per segment
- Download full insights report

---

### 4. Expected Results (with sample data)

You should see **3 distinct customer segments**:

**Segment 1: Loyal Veterans / Diligent Savers**
- Higher savings amounts
- Older age range
- Longer bank seniority
- Recommendations: Loyalty rewards, retirement planning

**Segment 2: Young Professionals / Standard Customers**
- Moderate income and savings
- Younger age range
- Lower bank seniority
- Recommendations: Digital banking, starter products

**Segment 3: High-Income Earners / Active Spenders**
- Higher monthly income
- Higher card spending
- Mixed age range
- Recommendations: Premium cards, investment products

---

### 5. Troubleshooting

**Problem**: Upload fails
- **Solution**: Ensure CSV has the 6 required columns with exact names (including € symbol)

**Problem**: Cleaning takes too long
- **Solution**: Sample data should process in 1-2 seconds. Check file size (max 5MB)

**Problem**: Charts not displaying
- **Solution**: Ensure each step completes before moving to next (check "Stage" indicator in top-right)

**Problem**: Empty pages
- **Solution**: Follow the workflow in order: Upload → Clean → PCA → Cluster → Profiles → Insights

---

### 6. Custom Data Requirements

To use your own data, ensure your CSV has these **exact column names**:


Monthly Income (€),Savings Amount (€),Credit Balance (€),Monthly Card Spending (€),Age,Bank Seniority (years)


**Data Format**:
- Numeric values only (no currency symbols in cells)
- Age: whole numbers (22-70)
- Seniority: whole numbers (1-25)
- Missing values: OK (pipeline will handle)
- Outliers: OK (pipeline will cap at 3 std devs)

---

### 7. Key Features Demonstrated

✅ **Automated Data Cleaning**: Handles missing values, outliers, duplicates  
✅ **PCA Dimensionality Reduction**: 6D → 2D-3D for visualization  
✅ **Optimal Cluster Selection**: Elbow method + Silhouette analysis  
✅ **K-Means Clustering**: Unsupervised customer segmentation  
✅ **Customer Profiling**: Detailed statistics per segment  
✅ **Marketing Insights**: AI-generated recommendations  
✅ **Export Capabilities**: Download logs, summaries, reports  

---

### 8. Technology Stack

- **Backend**: Python + Reflex framework
- **ML Libraries**: scikit-learn (PCA, K-Means), pandas, numpy
- **Frontend**: Recharts (visualizations), Tailwind CSS
- **State Management**: Reflex reactive state system

---

### 9. Next Steps

After completing the demo with sample data:

1. **Try different cluster numbers** (k=2 to k=10)
2. **Upload your own bank customer data**
3. **Explore different segments** using filters
4. **Download reports** for presentation to stakeholders
5. **Customize insights** by modifying `app/utils/insights_utils.py`

---

### 10. Support

For questions or issues:
- Review the main **README.md** for detailed documentation
- Check the **plan.md** for project structure
- Examine the code in `app/` directory

---

**Enjoy analyzing your bank customer segments! 🎯📊💡**
