'use client'

import React, { useEffect } from 'react';
import MenuComponent from '@/components/Manager/menu';
import { useRedirectUser } from '@/utils/redirectUser';
import DishesComponent from '@/components/Chef/dishes';

const Waiter: React.FC = () => {
    const { redirectUser } = useRedirectUser();

    useEffect(() => {
        redirectUser();
    }, [redirectUser]);
  return (
    <div>
      <DishesComponent />
    </div>
  );
};

export default Waiter;
