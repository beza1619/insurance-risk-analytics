# Insurance Risk Analytics Project 
 
## ?? Project Description 
This project analyzes car insurance data for AlphaCare Insurance Solutions (ACIS). 
The goal is to identify low-risk customers and optimize insurance premiums. 
 
## ?? Business Objectives 
1. Find "low-risk" customer segments for targeted marketing 
2. Test if location, gender, or vehicle type affects insurance risk 
3. Build predictive models for claim amounts 
4. Suggest optimal premium pricing 
 
## ?? Data Overview 
- **Period**: February 2014 to August 2015 
- **Location**: South Africa 
- **Contains**: Customer info, vehicle details, policy info, claims data 
 
## ??? How to Get Started 
 
### 1. Install Python 
Download Python 3.9+ from https://www.python.org/downloads/ 
**IMPORTANT**: Check "Add Python to PATH" during installation! 
 
### 2. Install Required Packages 
Open Command Prompt and type: 
``` 
pip install pandas numpy matplotlib seaborn jupyter scikit-learn xgboost dvc 
``` 
 
### 3. Clone and Setup Project 
``` 
git clone [your-repository-url] 
cd insurance-risk-analytics 
``` 
 
### 4. Run Jupyter Notebook 
``` 
jupyter notebook 
``` 
Then open the notebooks in this order: 
1. `01_eda.ipynb` - Exploratory Data Analysis 
2. `02_hypothesis_testing.ipynb` - Statistical Tests 
3. `03_modeling.ipynb` - Machine Learning Models 
 
## ?? Project Structure 
 
``` 
insurance-risk-analytics/ 
ÃÄÄ data/                    # All data files 
³   ÃÄÄ raw/                # Original data 
³   ÃÄÄ processed/          # Cleaned data 
³   ÀÄÄ interim/            # Intermediate files 
ÃÄÄ notebooks/              # Jupyter notebooks 
ÃÄÄ src/                    # Python source code 
ÃÄÄ models/                 # Saved ML models 
ÃÄÄ reports/                # Analysis reports 
ÃÄÄ requirements.txt        # Python dependencies 
ÀÄÄ README.md               # This file 
``` 
 
## ?? Project Timeline 
 
 
## ?? What I'm Learning 
- Data analysis with Python and Pandas 
- Statistical hypothesis testing 
- Machine learning for insurance 
- Data version control with DVC 
- Git and GitHub for collaboration 
