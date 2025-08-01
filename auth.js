const express = require('express');
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const { validateRegistration, validateLogin, sanitizeInput } = require('../middleware/validation');
const { redirectIfAuthenticated } = require('../middleware/auth');

const router = express.Router();

const generateToken = (userId) => {
    return jwt.sign({ userId }, process.env.JWT_SECRET, { expiresIn: '7d' });
};

const setTokenCookie = (res, token) => {
    res.cookie('token', token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60 * 1000
    });
};

router.get('/login', redirectIfAuthenticated, (req, res) => {
    res.render('auth/login', { 
        title: 'Login - Emergency Response System',
        error: null,
        email: ''
    });
});

router.get('/register', redirectIfAuthenticated, (req, res) => {
    res.render('auth/register', { 
        title: 'Register - Emergency Response System',
        error: null,
        formData: {}
    });
});

router.post('/register', sanitizeInput, validateRegistration, async (req, res) => {
    try {
        const { name, email, password } = req.body;
        const existingUser = await User.findOne({ email });
        if (existingUser) {
            return res.status(400).json({ 
                error: 'User already exists with this email address' 
            });
        }

        const user = new User({
            name,
            email,
            password,
            isVerified: true  
        });

        await user.save();
        const token = generateToken(user._id);
        setTokenCookie(res, token);

        user.lastLogin = new Date();
        await user.save();

        res.status(201).json({ 
            success: true, 
            message: 'Registration successful',
            user: user.toJSON(),
            redirectTo: '/dashboard'
        });

    } catch (error) {
        console.error('Registration error:', error);
        
        if (error.code === 11000) {
            return res.status(400).json({ 
                error: 'Email address is already registered' 
            });
        }
        
        res.status(500).json({ 
            error: 'Registration failed. Please try again.' 
        });
    }
});

router.post('/login', sanitizeInput, validateLogin, async (req, res) => {
    try {
        const { email, password } = req.body;

        const user = await User.findOne({ email });
        if (!user) {
            return res.status(401).json({ 
                error: 'Invalid email or password' 
            });
        }
        const isPasswordValid = await user.comparePassword(password);
        if (!isPasswordValid) {
            return res.status(401).json({ 
                error: 'Invalid email or password' 
            });
        }

        const token = generateToken(user._id);
        setTokenCookie(res, token);

        user.lastLogin = new Date();
        await user.save();

        res.json({ 
            success: true, 
            message: 'Login successful',
            user: user.toJSON(),
            redirectTo: '/dashboard'
        });

    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ 
            error: 'Login failed. Please try again.' 
        });
    }
});
router.post('/logout', (req, res) => {
    res.clearCookie('token');
    res.json({ 
        success: true, 
        message: 'Logout successful',
        redirectTo: '/login'
    });
});

router.get('/profile', require('../middleware/auth').authenticateToken, (req, res) => {
    res.json({ 
        success: true, 
        user: req.user 
    });
});

module.exports = router;
router.get('/google', 
    require('passport').authenticate('google', { 
        scope: ['profile', 'email'],
        prompt: 'select_account'
    })
);

router.get('/google/callback', 
    require('passport').authenticate('google', { 
        failureRedirect: '/auth/login?error=oauth_failed' 
    }),
    async (req, res) => {
        try {
            console.log('Google OAuth callback - User:', req.user);
            
            if (!req.user) {
                console.error('No user found in Google OAuth callback');
                return res.redirect('/auth/login?error=oauth_callback_failed');
            }
            
            const token = generateToken(req.user._id);
            setTokenCookie(res, token);
            
            console.log('Token generated and cookie set, redirecting to dashboard');
            
            // Direct redirect to dashboard without any middleware interference
            return res.redirect('/dashboard');
            
        } catch (error) {
            console.error('Google OAuth callback error:', error);
            return res.redirect('/auth/login?error=oauth_callback_failed');
        }
    }
);




