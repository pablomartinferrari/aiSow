// src/pages/Login.tsx
import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
    Box,
    Card,
    CardContent,
    Typography,
    TextField,
    Button,
    Alert,
    FormControl,
    InputLabel,
    OutlinedInput,
    InputAdornment,
    IconButton,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Divider,
    Container,
    Paper
} from '@mui/material';
import { Visibility, VisibilityOff, CheckCircle, Cancel } from '@mui/icons-material';

const Login: React.FC = () => {
    const { register, loginLocal } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const [isRegistering, setIsRegistering] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirmPassword: ''
    });
    const [error, setError] = useState('');

    // Password validation rules
    const passwordRules = [
        { rule: 'At least 6 characters', test: (password: string) => password.length >= 6 },
        { rule: 'At least one uppercase letter', test: (password: string) => /[A-Z]/.test(password) },
        { rule: 'At least one lowercase letter', test: (password: string) => /[a-z]/.test(password) },
        { rule: 'At least one digit', test: (password: string) => /\d/.test(password) },
        { rule: 'At least one special character', test: (password: string) => /[^A-Za-z0-9]/.test(password) }
    ];

    const getPasswordValidation = (password: string) => {
        return passwordRules.map(rule => ({
            ...rule,
            isValid: rule.test(password)
        }));
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
        setError(''); // Clear error when user starts typing
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        if (isRegistering) {
            if (formData.password !== formData.confirmPassword) {
                setError('Passwords do not match');
                return;
            }

            // Check if password meets all requirements
            const validation = getPasswordValidation(formData.password);
            const failedRules = validation.filter(rule => !rule.isValid);

            if (failedRules.length > 0) {
                setError(`Password requirements not met: ${failedRules.map(rule => rule.rule).join(', ')}`);
                return;
            }
        }

        try {
            if (isRegistering) {
                await register(formData.email, formData.password);
            } else {
                await loginLocal(formData.email, formData.password);
            }

            // Navigate to dashboard or the intended destination
            const from = location.state?.from?.pathname || '/';
            navigate(from, { replace: true });
        } catch (err: any) {
            // Handle different types of errors
            if (err.message.includes('Email')) {
                setError('Please enter a valid email address');
            } else if (err.message.includes('Password')) {
                setError('Password does not meet requirements');
            } else if (err.message.includes('already taken')) {
                setError('An account with this email already exists');
            } else if (err.message.includes('Invalid login')) {
                setError('Invalid email or password');
            } else {
                setError(err.message || 'An error occurred');
            }
        }
    };

    const passwordValidation = getPasswordValidation(formData.password);
    const isPasswordValid = passwordValidation.every(rule => rule.isValid);
    const passwordsMatch = formData.password === formData.confirmPassword;

    return (
        <Container component="main" maxWidth="sm">
            <Box
                sx={{
                    minHeight: '100vh',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    py: 4
                }}
            >
                <Card sx={{ width: '100%', maxWidth: 400 }}>
                    <CardContent sx={{ p: 4 }}>
                        <Typography component="h1" variant="h4" align="center" gutterBottom>
                            {isRegistering ? 'Create Account' : 'Sign In'}
                        </Typography>

                        <Typography variant="body2" align="center" color="text.secondary" sx={{ mb: 3 }}>
                            {isRegistering ? 'Already have an account?' : "Don't have an account?"}{' '}
                            <Button
                                variant="text"
                                size="small"
                                onClick={() => {
                                    setIsRegistering(!isRegistering);
                                    setError('');
                                    setFormData({ email: '', password: '', confirmPassword: '' });
                                }}
                                sx={{ textTransform: 'none' }}
                            >
                                {isRegistering ? 'Sign in' : 'Sign up'}
                            </Button>
                        </Typography>

                        {error && (
                            <Alert severity="error" sx={{ mb: 3 }}>
                                {error}
                            </Alert>
                        )}

                        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="email"
                                label="Email Address"
                                name="email"
                                autoComplete="email"
                                autoFocus
                                value={formData.email}
                                onChange={handleInputChange}
                                sx={{ mb: 2 }}
                            />

                            <FormControl fullWidth margin="normal" variant="outlined">
                                <InputLabel htmlFor="password">Password</InputLabel>
                                <OutlinedInput
                                    id="password"
                                    name="password"
                                    type={showPassword ? 'text' : 'password'}
                                    value={formData.password}
                                    onChange={handleInputChange}
                                    endAdornment={
                                        <InputAdornment position="end">
                                            <IconButton
                                                aria-label="toggle password visibility"
                                                onClick={() => setShowPassword(!showPassword)}
                                                edge="end"
                                            >
                                                {showPassword ? <VisibilityOff /> : <Visibility />}
                                            </IconButton>
                                        </InputAdornment>
                                    }
                                    label="Password"
                                />
                            </FormControl>

                            {/* Password Requirements */}
                            {isRegistering && formData.password && (
                                <Paper variant="outlined" sx={{ p: 2, mt: 2, mb: 2 }}>
                                    <Typography variant="subtitle2" gutterBottom>
                                        Password requirements:
                                    </Typography>
                                    <List dense>
                                        {passwordValidation.map((rule, index) => (
                                            <ListItem key={index} sx={{ py: 0.5 }}>
                                                <ListItemIcon sx={{ minWidth: 32 }}>
                                                    {rule.isValid ? (
                                                        <CheckCircle color="success" fontSize="small" />
                                                    ) : (
                                                        <Cancel color="error" fontSize="small" />
                                                    )}
                                                </ListItemIcon>
                                                <ListItemText
                                                    primary={rule.rule}
                                                    primaryTypographyProps={{
                                                        variant: 'body2',
                                                        color: rule.isValid ? 'success.main' : 'error.main'
                                                    }}
                                                />
                                            </ListItem>
                                        ))}
                                    </List>
                                </Paper>
                            )}

                            {isRegistering && (
                                <FormControl fullWidth margin="normal" variant="outlined">
                                    <InputLabel htmlFor="confirmPassword">Confirm Password</InputLabel>
                                    <OutlinedInput
                                        id="confirmPassword"
                                        name="confirmPassword"
                                        type={showConfirmPassword ? 'text' : 'password'}
                                        value={formData.confirmPassword}
                                        onChange={handleInputChange}
                                        endAdornment={
                                            <InputAdornment position="end">
                                                <IconButton
                                                    aria-label="toggle confirm password visibility"
                                                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                                    edge="end"
                                                >
                                                    {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                                                </IconButton>
                                            </InputAdornment>
                                        }
                                        label="Confirm Password"
                                        error={formData.confirmPassword && !passwordsMatch}
                                    />
                                </FormControl>
                            )}

                            {isRegistering && formData.confirmPassword && !passwordsMatch && (
                                <Typography variant="caption" color="error" sx={{ mt: 1, display: 'block' }}>
                                    Passwords do not match
                                </Typography>
                            )}

                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                disabled={isRegistering && (!isPasswordValid || !passwordsMatch)}
                                sx={{ mt: 3, mb: 2, py: 1.5 }}
                            >
                                {isRegistering ? 'Create Account' : 'Sign In'}
                            </Button>
                        </Box>
                    </CardContent>
                </Card>
            </Box>
        </Container>
    );
};

export default Login;
