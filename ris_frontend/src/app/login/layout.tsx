// components/layout.tsx
import React from 'react';
import { Container, AppBar, Toolbar, Typography } from '@mui/material';

interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <Container maxWidth="md">
            {children}
        </Container>
    );
};

export default Layout;
