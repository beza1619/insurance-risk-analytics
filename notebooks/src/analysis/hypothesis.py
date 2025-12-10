# src/analysis/hypothesis.py
"""
Hypothesis testing for insurance risk analysis.
Tests the four business hypotheses.
"""

import pandas as pd
import numpy as np
from scipy import stats
import json

class HypothesisTester:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.results = {}
    
    def test_province_risk(self):
        """
        Hypothesis 1: No risk differences across provinces
        Test: One-way ANOVA
        """
        print("Testing: Province risk differences")
        
        provinces = self.df['Province'].unique()
        loss_ratios = []
        
        for province in provinces:
            province_data = self.df[self.df['Province'] == province]
            if len(province_data) > 10:
                loss_ratios.append(province_data['LossRatio'].values)
        
        # ANOVA test
        f_stat, p_value = stats.f_oneway(*loss_ratios)
        
        result = {
            'test': 'ANOVA',
            'f_statistic': float(f_stat),
            'p_value': float(p_value),
            'reject_null': p_value < 0.05,
            'conclusion': 'REJECT' if p_value < 0.05 else 'FAIL TO REJECT'
        }
        
        self.results['province_risk'] = result
        return result
    
    def run_all_tests(self):
        """Run all hypothesis tests"""
        print("Running hypothesis tests...")
        
        # Test 1: Province risk
        test1 = self.test_province_risk()
        print(f"Province risk: p={test1['p_value']:.4f}, {test1['conclusion']}")
        
        # Save results
        with open('reports/hypothesis_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return self.results

# Example usage
if __name__ == "__main__":
    tester = HypothesisTester('data/processed/cleaned_data.csv')
    results = tester.run_all_tests()
