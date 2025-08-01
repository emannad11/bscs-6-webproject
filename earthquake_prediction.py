import numpy as np
import json
from datetime import datetime

class EarthquakePrediction:
    def __init__(self):
        self.risk_factors = {
            'seismic_activity': 0.3,
            'geological_stress': 0.25,
            'historical_data': 0.2,
            'tectonic_movement': 0.15,
            'ground_water_level': 0.1
        }
    
    def predict_earthquake(self, location, seismic_activity, geological_stress, 
                          historical_frequency, tectonic_movement, ground_water_change):
        """
        Simple AI-based earthquake prediction
        Returns risk level and probability
        """
        try:

            inputs = {
                'seismic_activity': min(max(seismic_activity, 0), 10),
                'geological_stress': min(max(geological_stress, 0), 10),
                'historical_data': min(max(historical_frequency, 0), 10),
                'tectonic_movement': min(max(tectonic_movement, 0), 10),
                'ground_water_level': min(max(ground_water_change, 0), 10)
            }
            
            risk_score = 0
            for factor, weight in self.risk_factors.items():
                risk_score += inputs[factor] * weight
            
        
            probability = min(risk_score * 10, 100)
            
            if probability < 30:
                risk_level = "Low"
                alert_color = "green"
            elif probability < 60:
                risk_level = "Medium"
                alert_color = "yellow"
            elif probability < 80:
                risk_level = "High"
                alert_color = "orange"
            else:
                risk_level = "Critical"
                alert_color = "red"
            
            result = {
                'location': location,
                'prediction_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'probability': round(probability, 2),
                'risk_level': risk_level,
                'alert_color': alert_color,
                'factors': inputs,
                'recommendations': self.get_recommendations(risk_level)
            }
            
            return result
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_recommendations(self, risk_level):
        recommendations = {
            'Low': [
                'Continue normal activities',
                'Keep emergency kit updated',
                'Stay informed about local alerts'
            ],
            'Medium': [
                'Review emergency plans',
                'Check building safety',
                'Prepare emergency supplies',
                'Stay alert for updates'
            ],
            'High': [
                'Avoid tall buildings if possible',
                'Keep emergency kit ready',
                'Plan evacuation routes',
                'Monitor official alerts closely'
            ],
            'Critical': [
                'Consider temporary relocation',
                'Avoid unnecessary travel',
                'Keep emergency supplies accessible',
                'Follow official evacuation orders'
            ]
        }
        return recommendations.get(risk_level, [])

def test_prediction():
    predictor = EarthquakePrediction()

    result = predictor.predict_earthquake(
        location="Karachi, Pakistan",
        seismic_activity=6.5,
        geological_stress=7.2,
        historical_frequency=4.8,
        tectonic_movement=5.5,
        ground_water_change=3.2
    )
    
    print("Earthquake Prediction Test:")
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    test_prediction()

