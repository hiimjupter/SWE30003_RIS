"use client"
import React, { useState, ChangeEvent, useEffect } from 'react';
import { useRedirectUser } from '@/utils/redirectUser';

const Home: React.FC = () => {
    const { redirectUser } = useRedirectUser();

    useEffect(() => {
        redirectUser();
    }, [redirectUser]);
    return (
        <></>
    );
};

export default Home;
