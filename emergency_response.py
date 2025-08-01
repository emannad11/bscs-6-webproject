
import json
import sys
from datetime import datetime, timedelta
import uuid

class EmergencyResponseSystem:
    def __init__(self):
        self.active_emergencies = []
        self.response_teams = {
            'medical': [
                {'id': 'MED001', 'type': 'Ambulance', 'location': 'Karachi', 'status': 'available', 'capacity': 2},
                {'id': 'MED002', 'type': 'Medical Team', 'location': 'Lahore', 'status': 'available', 'capacity': 5},
                {'id': 'MED003', 'type': 'Emergency Doctor', 'location': 'Islamabad', 'status': 'available', 'capacity': 1}
            ],
            'fire': [
                {'id': 'FIRE001', 'type': 'Fire Truck', 'location': 'Karachi', 'status': 'available', 'capacity': 8},
                {'id': 'FIRE002', 'type': 'Fire Team', 'location': 'Lahore', 'status': 'available', 'capacity': 6}
            ],
            'rescue': [
                {'id': 'RES001', 'type': 'Rescue Team', 'location': 'Karachi', 'status': 'available', 'capacity': 10},
                {'id': 'RES002', 'type': 'Search & Rescue', 'location': 'Islamabad', 'status': 'available', 'capacity': 8},
                {'id': 'RES003', 'type': 'Heavy Equipment', 'location': 'Lahore', 'status': 'available', 'capacity': 3}
            ],
            'police': [
                {'id': 'POL001', 'type': 'Police Unit', 'location': 'Karachi', 'status': 'available', 'capacity': 4},
                {'id': 'POL002', 'type': 'Traffic Control', 'location': 'Lahore', 'status': 'available', 'capacity': 6}
            ]
        }
        
        self.emergency_protocols = {
            'earthquake': {
                'priority': 'critical',
                'required_teams': ['rescue', 'medical', 'fire'],
                'response_time': 15,  
                'evacuation_radius': 5, 
                'safety_measures': [
                    'Immediate evacuation of damaged buildings',
                    'Search and rescue operations',
                    'Medical triage setup',
                    'Traffic control and road clearance',
                    'Utility shutdown if necessary'
                ]
            },
            'flood': {
                'priority': 'high',
                'required_teams': ['rescue', 'medical'],
                'response_time': 20,
                'evacuation_radius': 3,
                'safety_measures': [
                    'Evacuation of low-lying areas',
                    'Water rescue operations',
                    'Emergency shelter setup',
                    'Medical aid stations',
                    'Road closure and traffic diversion'
                ]
            },
            'fire': {
                'priority': 'high',
                'required_teams': ['fire', 'medical', 'police'],
                'response_time': 10,
                'evacuation_radius': 2,
                'safety_measures': [
                    'Fire suppression operations',
                    'Evacuation of surrounding areas',
                    'Medical treatment for smoke inhalation',
                    'Traffic control',
                    'Utility isolation'
                ]
            },
            'medical': {
                'priority': 'critical',
                'required_teams': ['medical'],
                'response_time': 8,
                'evacuation_radius': 0.5,
                'safety_measures': [
                    'Immediate medical response',
                    'Patient stabilization',
                    'Hospital transport',
                    'Scene safety assessment'
                ]
            }
        }
    
    def declare_emergency(self, emergency_type, location, severity, description, coordinates=None):
        """Declare a new emergency and initiate response"""
        emergency_id = str(uuid.uuid4())[:8]
        
        emergency = {
            'id': emergency_id,
            'type': emergency_type,
            'location': location,
            'coordinates': coordinates or {'lat': 0, 'lng': 0},
            'severity': severity,  
            'description': description,
            'status': 'active',
            'declared_at': datetime.now().isoformat(),
            'estimated_resolution': None,
            'assigned_teams': [],
            'affected_population': self.estimate_affected_population(severity),
            'response_plan': self.generate_response_plan(emergency_type, severity)
        }
        
    
        assigned_teams = self.assign_response_teams(emergency_type, location, severity)
        emergency['assigned_teams'] = assigned_teams
        

        protocol = self.emergency_protocols.get(emergency_type, {})
        base_response_time = protocol.get('response_time', 30)
        estimated_duration = base_response_time + (severity * 10) 
        emergency['estimated_resolution'] = (datetime.now() + timedelta(minutes=estimated_duration)).isoformat()
        
        self.active_emergencies.append(emergency)
        
        return {
            'emergency_id': emergency_id,
            'status': 'declared',
            'response_initiated': True,
            'assigned_teams': len(assigned_teams),
            'estimated_response_time': f"{base_response_time} minutes",
            'emergency_details': emergency
        }
    
    def assign_response_teams(self, emergency_type, location, severity):
        """Assign appropriate response teams based on emergency type and severity"""
        protocol = self.emergency_protocols.get(emergency_type, {})
        required_team_types = protocol.get('required_teams', [])
        
        assigned_teams = []
        
        for team_type in required_team_types:
            available_teams = [team for team in self.response_teams.get(team_type, []) 
                             if team['status'] == 'available']
            
    
            local_teams = [team for team in available_teams if location.lower() in team['location'].lower()]
            other_teams = [team for team in available_teams if location.lower() not in team['location'].lower()]
            
            teams_to_assign = local_teams + other_teams
            
    
            teams_needed = min(severity // 3 + 1, len(teams_to_assign))
            
            for i in range(teams_needed):
                if i < len(teams_to_assign):
                    team = teams_to_assign[i]
                    team['status'] = 'deployed'
                    team['assigned_at'] = datetime.now().isoformat()
                    assigned_teams.append(team)
        
        return assigned_teams
    
    def estimate_affected_population(self, severity):
        """Estimate affected population based on severity"""
        base_population = {
            1: 10, 2: 25, 3: 50, 4: 100, 5: 250,
            6: 500, 7: 1000, 8: 2500, 9: 5000, 10: 10000
        }
        return base_population.get(severity, 100)
    
    def generate_response_plan(self, emergency_type, severity):
        """Generate a detailed response plan"""
        protocol = self.emergency_protocols.get(emergency_type, {})
        
        plan = {
            'priority_level': protocol.get('priority', 'medium'),
            'immediate_actions': protocol.get('safety_measures', []),
            'evacuation_required': severity >= 6,
            'evacuation_radius_km': protocol.get('evacuation_radius', 1),
            'medical_facilities_needed': severity >= 5,
            'shelter_capacity_needed': self.estimate_affected_population(severity) if severity >= 7 else 0,
            'estimated_duration_hours': severity * 2,
            'resource_requirements': self.calculate_resource_requirements(emergency_type, severity)
        }
        
        return plan
    
    def calculate_resource_requirements(self, emergency_type, severity):
        """Calculate required resources based on emergency type and severity"""
        base_requirements = {
            'earthquake': {
                'medical_supplies': severity * 10,
                'rescue_equipment': severity * 5,
                'emergency_shelters': severity * 2,
                'food_packages': severity * 20,
                'water_liters': severity * 100
            },
            'flood': {
                'boats': severity * 2,
                'life_jackets': severity * 15,
                'water_pumps': severity * 3,
                'sandbags': severity * 50,
                'emergency_shelters': severity * 3
            },
            'fire': {
                'fire_extinguishers': severity * 8,
                'breathing_apparatus': severity * 4,
                'medical_supplies': severity * 6,
                'evacuation_vehicles': severity * 2
            },
            'medical': {
                'ambulances': severity * 1,
                'medical_supplies': severity * 15,
                'hospital_beds': severity * 3,
                'medical_personnel': severity * 2
            }
        }
        
        return base_requirements.get(emergency_type, {})
    
    def update_emergency_status(self, emergency_id, new_status, update_notes=None):
        """Update the status of an active emergency"""
        for emergency in self.active_emergencies:
            if emergency['id'] == emergency_id:
                emergency['status'] = new_status
                emergency['last_updated'] = datetime.now().isoformat()
                
                if update_notes:
                    if 'updates' not in emergency:
                        emergency['updates'] = []
                    emergency['updates'].append({
                        'timestamp': datetime.now().isoformat(),
                        'notes': update_notes
                    })
                
                
                if new_status in ['resolved', 'closed']:
                    for team in emergency['assigned_teams']:
                        team['status'] = 'available'
                        team['assigned_at'] = None
                
                return {'success': True, 'emergency': emergency}
        
        return {'success': False, 'error': 'Emergency not found'}
    
    def get_active_emergencies(self):
        """Get all active emergencies"""
        return [e for e in self.active_emergencies if e['status'] == 'active']
    
    def get_emergency_by_id(self, emergency_id):
        """Get specific emergency by ID"""
        for emergency in self.active_emergencies:
            if emergency['id'] == emergency_id:
                return emergency
        return None
    
    def get_available_resources(self):
        """Get all available response teams and resources"""
        available_resources = {}
        for team_type, teams in self.response_teams.items():
            available_resources[team_type] = [team for team in teams if team['status'] == 'available']
        return available_resources
    
    def simulate_emergency_scenario(self, scenario_type):
        """Simulate different emergency scenarios for testing"""
        scenarios = {
            'major_earthquake': {
                'emergency_type': 'earthquake',
                'location': 'Karachi, Pakistan',
                'severity': 8,
                'description': 'Major earthquake detected, magnitude 7.2, multiple buildings damaged',
                'coordinates': {'lat': 24.8607, 'lng': 67.0011}
            },
            'flash_flood': {
                'emergency_type': 'flood',
                'location': 'Lahore, Pakistan',
                'severity': 7,
                'description': 'Flash flood due to heavy rainfall, water level rising rapidly',
                'coordinates': {'lat': 31.5204, 'lng': 74.3587}
            },
            'building_fire': {
                'emergency_type': 'fire',
                'location': 'Islamabad, Pakistan',
                'severity': 6,
                'description': 'Large building fire, multiple floors affected, people trapped',
                'coordinates': {'lat': 33.6844, 'lng': 73.0479}
            },
            'medical_emergency': {
                'emergency_type': 'medical',
                'location': 'Karachi, Pakistan',
                'severity': 5,
                'description': 'Mass casualty incident, multiple injuries reported',
                'coordinates': {'lat': 24.8607, 'lng': 67.0011}
            }
        }
        
        scenario = scenarios.get(scenario_type)
        if scenario:
            return self.declare_emergency(**scenario)
        else:
            return {'error': 'Unknown scenario type'}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'No command provided'}))
        return
    
    command = sys.argv[1]
    emergency_system = EmergencyResponseSystem()
    
    if command == 'declare':
    
        if len(sys.argv) < 6:
            print(json.dumps({'error': 'Insufficient parameters for declare command'}))
            return
        
        emergency_type = sys.argv[2]
        location = sys.argv[3]
        severity = int(sys.argv[4])
        description = sys.argv[5]
        
        result = emergency_system.declare_emergency(emergency_type, location, severity, description)
        print(json.dumps(result))
    
    elif command == 'simulate':
        scenario_type = sys.argv[2] if len(sys.argv) > 2 else 'major_earthquake'
        result = emergency_system.simulate_emergency_scenario(scenario_type)
        print(json.dumps(result))
    
    elif command == 'status':
        emergency_id = sys.argv[2] if len(sys.argv) > 2 else None
        if emergency_id:
            result = emergency_system.get_emergency_by_id(emergency_id)
        else:
            result = emergency_system.get_active_emergencies()
        print(json.dumps(result))
    
    elif command == 'resources':
        result = emergency_system.get_available_resources()
        print(json.dumps(result))
    
    elif command == 'update':
        if len(sys.argv) < 4:
            print(json.dumps({'error': 'Insufficient parameters for update command'}))
            return
        
        emergency_id = sys.argv[2]
        new_status = sys.argv[3]
        notes = sys.argv[4] if len(sys.argv) > 4 else None
        
        result = emergency_system.update_emergency_status(emergency_id, new_status, notes)
        print(json.dumps(result))
    
    else:
        print(json.dumps({'error': 'Unknown command'}))

if __name__ == "__main__":
    main()

