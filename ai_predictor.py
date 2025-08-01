#!/usr/bin/env python3
import sys
import json
from earthquake_prediction import EarthquakePrediction
from flood_prediction import FloodPrediction
from emergency_response import EmergencyResponseSystem

class EmergencyAI:
    def __init__(self):
        self.earthquake_predictor = EarthquakePrediction()
        self.flood_predictor = FloodPrediction()
        self.emergency_system = EmergencyResponseSystem()
    
    def predict_earthquake(self, data):
        """Predict earthquake risk and trigger emergency response if needed"""
        try:
            # Ensure all required fields have default values
            location = data.get('location', 'Unknown Location')
            seismic_activity = float(data.get('seismic_activity', 0))
            geological_stress = float(data.get('geological_stress', 0))
            historical_frequency = float(data.get('historical_frequency', 0))
            tectonic_movement = float(data.get('tectonic_movement', 0))
            ground_water_change = float(data.get('ground_water_change', 0))
            
            result = self.earthquake_predictor.predict_earthquake(
                location=location,
                seismic_activity=seismic_activity,
                geological_stress=geological_stress,
                historical_frequency=historical_frequency,
                tectonic_movement=tectonic_movement,
                ground_water_change=ground_water_change
            )
            
            # Ensure result has all required fields
            if not result:
                result = {}
            
            result['location'] = location
            result['probability'] = result.get('probability', 0)
            result['risk_level'] = result.get('risk_level', 'Low')
            result['prediction_time'] = result.get('prediction_time', 'Unknown')
            
            # Auto-trigger emergency response for high-risk predictions
            if result.get('probability', 0) >= 75:
                emergency_response = self.emergency_system.declare_emergency(
                    emergency_type='earthquake',
                    location=location,
                    severity=min(int(result.get('probability', 0) / 10), 10),
                    description=f"High earthquake risk detected: {result.get('probability', 0)}% probability"
                )
                result['emergency_response'] = emergency_response
            
            return result
        except Exception as e:
            return {
                'location': data.get('location', 'Unknown Location'),
                'probability': 0,
                'risk_level': 'Error',
                'prediction_time': 'Unknown',
                'error': str(e)
            }
    
    def predict_flood(self, data):
        """Predict flood risk and trigger emergency response if needed"""
        try:
            # Ensure all required fields have default values
            location = data.get('location', 'Unknown Location')
            rainfall_intensity = float(data.get('rainfall_intensity', 0))
            river_water_level = float(data.get('river_water_level', 0))
            soil_saturation = float(data.get('soil_saturation', 0))
            drainage_capacity = float(data.get('drainage_capacity', 0))
            elevation_risk = float(data.get('elevation_risk', 0))
            
            result = self.flood_predictor.predict_flood(
                location=location,
                rainfall_intensity=rainfall_intensity,
                river_water_level=river_water_level,
                soil_saturation=soil_saturation,
                drainage_capacity=drainage_capacity,
                elevation_risk=elevation_risk
            )
            
            if not result:
                result = {}
            
            result['location'] = location
            result['probability'] = result.get('probability', 0)
            result['risk_level'] = result.get('risk_level', 'Low')
            result['prediction_time'] = result.get('prediction_time', 'Unknown')
            
            if result.get('probability', 0) >= 70:
                emergency_response = self.emergency_system.declare_emergency(
                    emergency_type='flood',
                    location=location,
                    severity=min(int(result.get('probability', 0) / 10), 10),
                    description=f"High flood risk detected: {result.get('probability', 0)}% probability"
                )
                result['emergency_response'] = emergency_response
            
            return result
        except Exception as e:
            return {
                'location': data.get('location', 'Unknown Location'),
                'probability': 0,
                'risk_level': 'Error',
                'prediction_time': 'Unknown',
                'error': str(e)
            }

    
    def get_emergency_status(self, location):
        """Get overall emergency status for a location"""

        earthquake_data = {
            'location': location,
            'seismic_activity': 5.0,
            'geological_stress': 4.5,
            'historical_frequency': 3.8,
            'tectonic_movement': 4.2,
            'ground_water_change': 2.5
        }
        
        flood_data = {
            'location': location,
            'rainfall_intensity': 6.5,
            'river_water_level': 5.8,
            'soil_saturation': 4.2,
            'drainage_capacity': 6.0,
            'elevation_risk': 3.5
        }
        
        earthquake_result = self.predict_earthquake(earthquake_data)
        flood_result = self.predict_flood(flood_data)
        
        eq_prob = earthquake_result.get('probability', 0)
        flood_prob = flood_result.get('probability', 0)
        
        overall_risk = max(eq_prob, flood_prob)
        
        if overall_risk < 30:
            overall_status = "Safe"
            status_color = "green"
        elif overall_risk < 60:
            overall_status = "Caution"
            status_color = "yellow"
        elif overall_risk < 80:
            overall_status = "Warning"
            status_color = "orange"
        else:
            overall_status = "Emergency"
            status_color = "red"
        
        active_emergencies = self.emergency_system.get_active_emergencies()
        
        return {
            'location': location,
            'overall_status': overall_status,
            'status_color': status_color,
            'overall_risk': round(overall_risk, 2),
            'earthquake': earthquake_result,
            'flood': flood_result,
            'active_emergencies': len(active_emergencies),
            'emergency_details': active_emergencies[:3] 
        }
    
    def handle_emergency_command(self, command, *args):
        """Handle emergency-related commands"""
        if command == 'simulate':
            scenario_type = args[0] if args else 'major_earthquake'
            return self.emergency_system.simulate_emergency_scenario(scenario_type)
        elif command == 'declare':
            if len(args) < 4:
                return {'error': 'Insufficient parameters for declare command'}
            return self.emergency_system.declare_emergency(args[0], args[1], int(args[2]), args[3])
        elif command == 'active':
            return self.emergency_system.get_active_emergencies()
        elif command == 'resources':
            return self.emergency_system.get_available_resources()
        elif command == 'update':
            if len(args) < 2:
                return {'error': 'Insufficient parameters for update command'}
            notes = args[2] if len(args) > 2 else None
            return self.emergency_system.update_emergency_status(args[0], args[1], notes)
        else:
            return {'error': 'Unknown emergency command'}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'No command provided'}))
        return
    
    command = sys.argv[1]
    ai = EmergencyAI()
    
    if command == 'earthquake':
        if len(sys.argv) < 3:
            print(json.dumps({'error': 'No data provided'}))
            return
        data = json.loads(sys.argv[2])
        result = ai.predict_earthquake(data)
        print(json.dumps(result))
    
    elif command == 'flood':
        if len(sys.argv) < 3:
            print(json.dumps({'error': 'No data provided'}))
            return
        data = json.loads(sys.argv[2])
        result = ai.predict_flood(data)
        print(json.dumps(result))
    
    elif command == 'status':
        location = sys.argv[2] if len(sys.argv) > 2 else 'Unknown Location'
        result = ai.get_emergency_status(location)
        print(json.dumps(result))
    
    elif command == 'emergency':
        if len(sys.argv) < 3:
            print(json.dumps({'error': 'No emergency command provided'}))
            return
        emergency_command = sys.argv[2]
        args = sys.argv[3:] if len(sys.argv) > 3 else []
        result = ai.handle_emergency_command(emergency_command, *args)
        print(json.dumps(result))
    
    else:
        print(json.dumps({'error': 'Unknown command'}))

if __name__ == "__main__":
    main()

