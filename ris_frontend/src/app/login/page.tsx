"use client"
import React, { useState, ChangeEvent } from 'react';
import { login, getCurrentUser } from '../services/auth';
import { Container, TextField, Button, Card, CardContent, Typography, Box, Alert } from '@mui/material';
import { useRouter } from 'next/navigation';

const Login: React.FC = () => {
    const router = useRouter();
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [user, setUser] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    const handleLogin = async () => {
        try {
        setError(null);
        await login(username, password);
        const userData = await getCurrentUser();
        setUser(userData);
        router.push('/home');
        } catch (error) {
        setError('Login failed. Please check your username and password.');
        }
    };

    return (
        <Container>
        <Box display="flex" justifyContent="center" mt={25}>
            <Card>
            <CardContent>
                <Typography variant="h5">Login</Typography>
                <Box mt={2}>
                {error && <Alert severity="error">{error}</Alert>}
                <TextField
                    label="Username"
                    value={username}
                    onChange={(e: ChangeEvent<HTMLInputElement>) => setUsername(e.target.value)}
                    fullWidth
                    margin="normal"
                />
                <TextField
                    label="Password"
                    type="password"
                    value={password}
                    onChange={(e: ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
                    fullWidth
                    margin="normal"
                />
                <Box mt={2}>
                    <Button variant="contained" color="primary" onClick={handleLogin}>
                    Login
                    </Button>
                </Box>
                </Box>
            </CardContent>
            </Card>
        </Box>
        </Container>
    );
};

export default Login;
