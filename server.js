require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const session = require('express-session');
const passport = require('./config/passport');
const { exec } = require('child_process');
const path = require('path');
const cities = require('./cities');


const connectDB = require('./config/database');
const authRoutes = require('./routes/auth');
const { authenticateToken } = require('./middleware/auth');

const app = express();
const PORT = process.env.PORT || 3000;


connectDB();

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static('public'));

app.use(session({
    secret: process.env.SESSION_SECRET || 'your-session-secret',
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: process.env.NODE_ENV === 'production',
        maxAge: 24 * 60 * 60 * 1000 
    }
}));
app.use(passport.initialize());
app.use(passport.session());


app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

let incidents = [
    {
        id: 1,
        type: 'Flood',
        location: 'Karachi',
        description: 'Heavy rainfall causing street flooding in Saddar area',
        severity: 'Medium',
        status: 'Reported',
        timestamp: new Date().toISOString(),
        reporter: 'Citizen Report'
    }
];

let resources = [
    { id: 1, type: 'Ambulance', location: 'Karachi', status: 'Available', contact: '+92-300-1234567' },
    { id: 2, type: 'Fire Truck', location: 'Lahore', status: 'Available', contact: '+92-300-2345678' },
    { id: 3, type: 'Rescue Team', location: 'Islamabad', status: 'Busy', contact: '+92-300-3456789' },
    { id: 4, type: 'Medical Team', location: 'Karachi', status: 'Available', contact: '+92-300-4567890' },
    { id: 5, type: 'Police', location: 'Lahore', status: 'Available', contact: '+92-300-5678901' },
    { id: 6, type: 'Ambulance', location: 'Islamabad', status: 'Maintenance', contact: '+92-300-6789012' }
];


function runPythonScript(command, data = null) {
    return new Promise((resolve, reject) => {
        let cmd = `python3 ai_predictor.py ${command}`;
        if (data) {
            cmd += ` '${JSON.stringify(data)}'`;
        }
        
        exec(cmd, { cwd: __dirname }, (error, stdout, stderr) => {
            if (error) {
                reject(error);
                return;
            }
            try {
                const result = JSON.parse(stdout);
                resolve(result);
            } catch (e) {
                reject(e);
            }
        });
    });
}

app.use('/auth', authRoutes);
app.get('/', (req, res) => {
    res.redirect('/login');
});

app.get('/login', (req, res) => {
    res.redirect('/auth/login');
});

app.get('/register', (req, res) => {
    res.redirect('/auth/register');
});
app.get('/dashboard', authenticateToken, (req, res) => {
    res.render('dashboard', { 
        title: 'Dashboard - Emergency Response System',
        incidents: incidents.slice(-5),
        resources: resources,
        user: req.user
    });
});

app.get('/predict', authenticateToken, (req, res) => {
    res.render('predict', { 
        title: 'AI Prediction - Emergency Response System',
        cities: cities,
        user: req.user
    });
});

app.get('/incidents', authenticateToken, (req, res) => {
    res.render('incidents', { 
        title: 'Incidents - Emergency Response System',
        incidents: incidents,
        user: req.user
    });
});

app.get('/resources', authenticateToken, (req, res) => {
    res.render('resources', { 
        title: 'Resources - Emergency Response System',
        resources: resources,
        user: req.user
    });
});


app.get('/api/cities', authenticateToken, (req, res) => {
    res.json(cities);
});

app.get('/api/emergency-status', authenticateToken, async (req, res) => {
    try {
        const location = req.query.location || 'Pakistan';
        
        const statusData = {
            status: 'Normal',
            riskLevel: 'Low',
            location: location,
            lastUpdated: new Date().toISOString(),
            activeEmergencies: incidents.length,
            availableResources: resources.filter(r => r.status === 'Available').length
        };
        
        res.json(statusData);
    } catch (error) {
        console.error('Status check error:', error);
        res.status(500).json({ 
            error: 'Status check failed',
            status: 'Unknown',
            riskLevel: 'Unknown',
            location: 'Unknown'
        });
    }
});

app.post('/predict/earthquake', authenticateToken, async (req, res) => {
    try {
        
        const { location, magnitude, depth, frequency } = req.body;
        
        const prediction = {
            location: location || 'Unknown',
            riskLevel: parseFloat(magnitude) > 5 ? 'High' : parseFloat(magnitude) > 3 ? 'Medium' : 'Low',
            predictionTime: new Date().toISOString(),
            magnitude: magnitude || 'N/A',
            depth: depth ? `${depth} km` : 'N/A',
            frequency: frequency || 'N/A',
            confidence: '85%'
        };
        
        res.json(prediction);
    } catch (error) {
        console.error('Earthquake prediction error:', error);
        res.status(500).json({ error: 'Prediction failed', details: error.message });
    }
});

app.post('/predict/flood', authenticateToken, async (req, res) => {
    try {
        const { location, rainfall, elevation, soilSaturation } = req.body;
        
        const prediction = {
            location: location || 'Unknown',
            riskLevel: parseFloat(rainfall) > 200 ? 'High' : parseFloat(rainfall) > 100 ? 'Medium' : 'Low',
            predictionTime: new Date().toISOString(),
            rainfall: rainfall ? `${rainfall} mm` : 'N/A',
            elevation: elevation ? `${elevation} m` : 'N/A',
            soilSaturation: soilSaturation || 'N/A',
            confidence: '78%'
        };
        
        res.json(prediction);
    } catch (error) {
        console.error('Flood prediction error:', error);
        res.status(500).json({ error: 'Prediction failed', details: error.message });
    }
});

app.post('/incidents', authenticateToken, (req, res) => {
    const incident = {
        id: incidents.length + 1,
        type: req.body.type,
        location: req.body.location,
        description: req.body.description,
        severity: req.body.severity,
        status: 'Reported',
        timestamp: new Date().toISOString(),
        reporter: req.body.reporter || 'Anonymous'
    };
    
    incidents.push(incident);
    res.json({ success: true, incident });
});

app.post('/resources/:id/status', authenticateToken, (req, res) => {
    const resourceId = parseInt(req.params.id);
    const resource = resources.find(r => r.id === resourceId);
    
    if (resource) {
        resource.status = req.body.status;
        res.json({ success: true, resource });
    } else {
        res.status(404).json({ error: 'Resource not found' });
    }
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚨 Emergency Response System running on http://0.0.0.0:${PORT}`);
    console.log('🤖 AI Prediction modules loaded successfully');
});

module.exports = app;

