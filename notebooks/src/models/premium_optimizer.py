
def optimize_premium(policy_data, claim_model, current_premium):
    """
    Optimize insurance premium based on predicted risk.
    
    Parameters:
    -----------
    policy_data : dict or DataFrame
        Policyholder information
    claim_model : trained model
        Model to predict claim severity
    current_premium : float
        Current premium amount
    
    Returns:
    --------
    dict: Optimization results
    """
    
    # Predict claim severity
    predicted_severity = claim_model.predict(policy_data)[0]
    
    # Estimate claim probability (simplified)
    base_prob = 0.7  # Base claim probability
    
    # Risk adjustments
    risk_multiplier = 1.0
    
    # Province risk
    province = policy_data.get('Province', 'Unknown')
    if province == 'Gauteng':
        risk_multiplier *= 1.3
    elif province == 'Western Cape':
        risk_multiplier *= 0.9
    elif province == 'Free State':
        risk_multiplier *= 0.8
    
    # Vehicle type risk
    vehicle_type = policy_data.get('VehicleType', 'Unknown')
    if vehicle_type in ['SUV', 'Bakkie']:
        risk_multiplier *= 1.2
    elif vehicle_type == 'Sedan':
        risk_multiplier *= 0.9
    
    # Previous claims
    prev_claims = policy_data.get('PreviousClaims', 0)
    risk_multiplier *= (1 + prev_claims * 0.3)
    
    estimated_probability = min(base_prob * risk_multiplier, 0.95)
    
    # Calculate optimized premium
    risk_component = estimated_probability * predicted_severity
    expense_loading = 0.3  # 30% expenses
    profit_margin = 0.15   # 15% profit
    
    optimized_premium = risk_component * (1 + expense_loading + profit_margin)
    
    return {
        'current_premium': current_premium,
        'optimized_premium': optimized_premium,
        'predicted_severity': predicted_severity,
        'estimated_probability': estimated_probability,
        'recommendation': 'INCREASE' if optimized_premium > current_premium else 'DECREASE',
        'adjustment_percentage': ((optimized_premium - current_premium) / current_premium) * 100
    }
