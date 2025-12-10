# Insurance Risk Analytics for AlphaCare

## 📋 Project Overview
This project conducts comprehensive risk analytics for **AlphaCare Insurance Solutions** (ACIS) to optimize marketing strategies, refine pricing models, and enhance overall profitability. The analysis uses a reproducible data pipeline ensuring auditability and regulatory compliance.

### Key Objectives
1. **Risk Segmentation**: Identify high-risk and low-risk customer segments across provinces
2. **Predictive Modeling**: Develop machine learning models to predict claim severity
3. **Pricing Optimization**: Create data-driven premium recommendations
4. **Strategic Insights**: Provide actionable marketing and underwriting strategies

##  Repository Structure
insurance-risk-analytics/
├── data/
│ ├── raw/ # Raw insurance data (DVC-tracked)
│ └── processed/ # Cleaned and processed data
├── notebooks/
│ ├── 01_eda.ipynb # Exploratory Data Analysis notebook
│ └── 02_analysis.ipynb # Statistical analysis notebook
├── src/
│ ├── data/ # Data processing scripts
│ ├── features/ # Feature engineering
│ ├── models/ # ML model training
│ └── visualization/ # Plotting functions
├── models/ # Trained models (DVC-tracked)
├── reports/
│ ├── figures/ # Generated visualizations
│ └── metrics/ # Performance metrics
├── tests/ # Test files
├── .gitignore # Git ignore rules
├── .dvcignore # DVC ignore rules
├── dvc.yaml # DVC pipeline definition
├── params.yaml # Configuration parameters
├── requirements.txt # Python dependencies
├── README.md # This file
└── INTERIM_SUBMISSION.md # Interim submission report

## 🚀 Quick Start Guide (Windows)

### Prerequisites
- Python 3.8 or higher
- Git for Windows
- DVC (Data Version Control)

### Step 1: Clone the Repository
```cmd
git clone https://github.com/yourusername/insurance-risk-analytics.git
cd insurance-risk-analytics