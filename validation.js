const validator = require('validator');

const validateEmail = (email) => {
    return validator.isEmail(email);
};

const validatePassword = (password) => {
    const minLength = 8;
    const hasNumber = /\d/.test(password);
    const hasLetter = /[a-zA-Z]/.test(password);
    
    return password.length >= minLength && hasNumber && hasLetter;
};

const validateName = (name) => {
    
    return name && name.trim().length >= 2 && name.trim().length <= 50 && /^[a-zA-Z\s]+$/.test(name.trim());
};


const validateRegistration = (req, res, next) => {
    const { name, email, password, confirmPassword } = req.body;
    const errors = [];

   
    req.body.name = name ? name.trim() : '';
    req.body.email = email ? email.trim().toLowerCase() : '';

    
    if (!validateName(req.body.name)) {
        errors.push('Name must be 2-50 characters long and contain only letters and spaces');
    }

   
    if (!validateEmail(req.body.email)) {
        errors.push('Please provide a valid email address');
    }

    
    if (!validatePassword(password)) {
        errors.push('Password must be at least 8 characters long and contain at least one number and one letter');
    }

    if (password !== confirmPassword) {
        errors.push('Passwords do not match');
    }

    if (errors.length > 0) {
        return res.status(400).json({ 
            error: 'Validation failed', 
            details: errors 
        });
    }

    next();
};

const validateLogin = (req, res, next) => {
    const { email, password } = req.body;
    const errors = [];

    
    req.body.email = email ? email.trim().toLowerCase() : '';

    if (!validateEmail(req.body.email)) {
        errors.push('Please provide a valid email address');
    }

   
    if (!password || password.trim().length === 0) {
        errors.push('Password is required');
    }

    if (errors.length > 0) {
        return res.status(400).json({ 
            error: 'Validation failed', 
            details: errors 
        });
    }

    next();
};

const sanitizeInput = (req, res, next) => {
    for (let key in req.body) {
        if (typeof req.body[key] === 'string') {
            req.body[key] = validator.escape(req.body[key]);
        }
    }
    next();
};

module.exports = {
    validateRegistration,
    validateLogin,
    sanitizeInput,
    validateEmail,
    validatePassword,
    validateName
};

