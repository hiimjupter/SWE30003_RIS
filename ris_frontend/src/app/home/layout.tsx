'use client'

// src/app/home/layout.tsx
import React from 'react';
import { Container, AppBar, Toolbar, Typography, Button } from '@mui/material';
import { useRouter } from 'next/navigation'; // Use `next/navigation` instead of `next/router`

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const router = useRouter();

  const handleLogout = () => {
    // Clear the token and redirect to login
    localStorage.removeItem('access_token');
    router.push('/login');
  };

  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Relaxing Koala Restaurant
          </Typography>
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      <Container sx={{ mt: 2 }}>
        {children}
      </Container>
    </div>
  );
};

export default Layout;
