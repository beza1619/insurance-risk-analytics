# src/analysis/hypothesis_complete.py
"""
Complete hypothesis testing for all 4 business hypotheses.
Version: 1.0
"""

import pandas as pd
import numpy as np
from scipy import stats
import json
from pathlib import Path

class CompleteHypothesisTester:
    """Test all four business hypotheses from the report"""
    
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.results = {}
        self.alpha = 0.05  # Significance level
    
    def test_1_province_risk(self):
        """
        Hypothesis 1: "There are no risk differences across provinces."
        Test: One-way ANOVA on Loss Ratio
        """
        print("\nHYPOTHESIS 1: Province Risk Differences")
        print("-" * 40)
        
        # Get loss ratios for each province
        provinces = self.df['Province'].unique()
        loss_ratios_by_province = []
        
        for province in provinces:
            province_data = self.df[self.df['Province'] == province]
            if len(province_data) >= 10:  # Ensure sufficient data
                loss_ratios = province_data['LossRatio'].dropna().values
                if len(loss_ratios) > 0:
                    loss_ratios_by_province.append(loss_ratios)
        
        # Perform ANOVA
        if len(loss_ratios_by_province) >= 2:
            f_stat, p_value = stats.f_oneway(*loss_ratios_by_province)
            
            result = {
                'test': 'One-way ANOVA',
                'null_hypothesis': 'Loss ratios are equal across all provinces',
                'f_statistic': float(f_stat),
                'p_value': float(p_value),
                'alpha': self.alpha,
                'reject_null': p_value < self.alpha,
                'conclusion': 'REJECT' if p_value < self.alpha else 'FAIL TO REJECT',
                'business_implication': 'Geographic-based pricing is justified'
            }
            
            print(f"F-statistic: {f_stat:.4f}")
            print(f"P-value: {p_value:.4f}")
            print(f"Conclusion: {result['conclusion']}")
            
            self.results['hypothesis_1'] = result
            return result
        
        return None
    
    def test_2_3_zipcode_density(self):
        """
        Hypotheses 2 & 3: No risk or margin differences between zip codes
        Simplified test using postal code frequency as density proxy
        """
        print("\nHYPOTHESES 2 & 3: Zip Code Density Effects")
        print("-" * 40)
        
        if 'PostalCode' not in self.df.columns:
            print("PostalCode column not found - skipping test")
            return None
        
        # Use frequency as density proxy
        zipcode_counts = self.df['PostalCode'].value_counts()
        median_count = zipcode_counts.median()
        
        high_density_zips = zipcode_counts[zipcode_counts > median_count].index
        low_density_zips = zipcode_counts[zipcode_counts <= median_count].index
        
        self.df['HighDensity'] = self.df['PostalCode'].isin(high_density_zips)
        
        # Test for risk difference (Loss Ratio)
        high_density_lr = self.df[self.df['HighDensity']]['LossRatio'].dropna()
        low_density_lr = self.df[~self.df['HighDensity']]['LossRatio'].dropna()
        
        if len(high_density_lr) > 0 and len(low_density_lr) > 0:
            t_stat, p_value = stats.ttest_ind(high_density_lr, low_density_lr, equal_var=False)
            
            result = {
                'test': "Welch's t-test",
                'null_hypothesis': 'No risk difference between high/low density zip codes',
                't_statistic': float(t_stat),
                'p_value': float(p_value),
                'alpha': self.alpha,
                'reject_null': p_value < self.alpha,
                'conclusion': 'REJECT' if p_value < self.alpha else 'FAIL TO REJECT',
                'business_implication': 'Zip-code level analysis can reveal profit pockets'
            }
            
            print(f"T-statistic: {t_stat:.4f}")
            print(f"P-value: {p_value:.4f}")
            print(f"Conclusion: {result['conclusion']}")
            
            self.results['hypothesis_2_3'] = result
            return result
        
        return None
    
    def test_4_gender_difference(self):
        """
        Hypothesis 4: "There is no risk difference between women and men."
        Test: Chi-square test for claim frequency
        """
        print("\nHYPOTHESIS 4: Gender Risk Difference")
        print("-" * 40)
        
        if 'Gender' not in self.df.columns or 'HasClaim' not in self.df.columns:
            print("Required columns not found - skipping test")
            return None
        
        # Create contingency table
        contingency = pd.crosstab(self.df['Gender'], self.df['HasClaim'])
        
        # Perform chi-square test
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
        
        result = {
            'test': 'Chi-square test',
            'null_hypothesis': 'No association between gender and claim frequency',
            'chi2_statistic': float(chi2),
            'p_value': float(p_value),
            'degrees_freedom': int(dof),
            'alpha': self.alpha,
            'reject_null': p_value < self.alpha,
            'conclusion': 'REJECT' if p_value < self.alpha else 'FAIL TO REJECT',
            'business_interpretation': 'Statistical difference exists but pricing must use multidimensional assessment'
        }
        
        print(f"Chi-square: {chi2:.4f}")
        print(f"P-value: {p_value:.4f}")
        print(f"Conclusion: {result['conclusion']}")
        
        # Calculate the ~4% difference mentioned in report
        if 'Male' in contingency.index and 'Female' in contingency.index:
            male_claim_rate = contingency.loc['Male', 1] / contingency.loc['Male'].sum()
            female_claim_rate = contingency.loc['Female', 1] / contingency.loc['Female'].sum()
            percentage_diff = ((male_claim_rate - female_claim_rate) / female_claim_rate) * 100
            
            result['male_claim_rate'] = float(male_claim_rate)
            result['female_claim_rate'] = float(female_claim_rate)
            result['percentage_difference'] = float(percentage_diff)
            
            print(f"Male claim rate: {male_claim_rate:.3f}")
            print(f"Female claim rate: {female_claim_rate:.3f}")
            print(f"Difference: {percentage_diff:.1f}%")
        
        self.results['hypothesis_4'] = result
        return result
    
    def run_all_tests(self):
        """Run all four hypothesis tests"""
        print("=" * 60)
        print("RUNNING ALL HYPOTHESIS TESTS")
        print("=" * 60)
        
        test1 = self.test_1_province_risk()
        test2_3 = self.test_2_3_zipcode_density()
        test4 = self.test_4_gender_difference()
        
        # Save results
        Path('reports').mkdir(exist_ok=True)
        with open('reports/hypothesis_results_complete.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED")
        print("=" * 60)
        
        return self.results

# Example usage
if __name__ == "__main__":
    # Load data
    data_path = 'data/processed/cleaned_data.csv'
    
    print(f"Loading data from {data_path}")
    try:
        tester = CompleteHypothesisTester(data_path)
        results = tester.run_all_tests()
        print("\nResults saved to: reports/hypothesis_results_complete.json")
    except FileNotFoundError:
        print("Data file not found. Please run preprocessing first.")
