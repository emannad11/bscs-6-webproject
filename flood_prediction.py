import numpy as np
import json
from datetime import datetime

class FloodPrediction:
    def __init__(self):
        self.risk_factors = {
            'rainfall_intensity': 0.35,
            'river_water_level': 0.25,
            'soil_saturation': 0.2,
            'drainage_capacity': 0.15,
            'topography': 0.05
        }
    
    def predict_flood(self, location, rainfall_intensity, river_water_level, 
                     soil_saturation, drainage_capacity, elevation_risk):
        """
        Simple AI-based flood prediction
        Returns risk level and probability
        """
        try:
            
            inputs = {
                'rainfall_intensity': min(max(rainfall_intensity, 0), 10),
                'river_water_level': min(max(river_water_level, 0), 10),
                'soil_saturation': min(max(soil_saturation, 0), 10),
                'drainage_capacity': 10 - min(max(drainage_capacity, 0), 10),  
                'topography': min(max(elevation_risk, 0), 10)
            }
            
    
            risk_score = 0
            for factor, weight in self.risk_factors.items():
                risk_score += inputs[factor] * weight
            
        
            probability = min(risk_score * 10, 100)
            
            if probability < 25:
                risk_level = "Low"
                alert_color = "green"
            elif probability < 50:
                risk_level = "Medium"
                alert_color = "yellow"
            elif probability < 75:
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
                'recommendations': self.get_recommendations(risk_level),
                'estimated_water_level': self.estimate_water_level(probability)
            }
            
            return result
            
        except Exception as e:
            return {'error': str(e)}
    
    def estimate_water_level(self, probability):
        """Estimate potential water level based on flood probability"""
        if probability < 25:
            return "0-0.5 feet"
        elif probability < 50:
            return "0.5-2 feet"
        elif probability < 75:
            return "2-5 feet"
        else:
            return "5+ feet"
    
    def get_recommendations(self, risk_level):
        recommendations = {
            'Low': [
                'Monitor weather updates',
                'Clear drainage systems',
                'Keep emergency contacts ready'
            ],
            'Medium': [
                'Prepare sandbags if available',
                'Move valuables to higher ground',
                'Check evacuation routes',
                'Monitor water levels closely'
            ],
            'High': [
                'Evacuate low-lying areas',
                'Avoid driving through water',
                'Keep emergency supplies ready',
                'Stay tuned to emergency broadcasts'
            ],
            'Critical': [
                'Immediate evacuation required',
                'Avoid all water-covered roads',
                'Seek higher ground immediately',
                'Follow emergency services instructions'
            ]
        }
        return recommendations.get(risk_level, [])

def test_prediction():
    predictor = FloodPrediction()
    

    result = predictor.predict_flood(
        location="Lahore, Pakistan",
        rainfall_intensity=8.5,
        river_water_level=7.8,
        soil_saturation=6.2,
        drainage_capacity=3.5,
        elevation_risk=7.0
    )
    
    print("Flood Prediction Test:")
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    test_prediction()

