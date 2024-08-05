'use client'

import React, { useEffect } from 'react';
import TableComponent from '../../../components/Waiter/tables';
import { useRedirectUser } from '@/utils/redirectUser';


const Waiter: React.FC = () => {
    const { redirectUser } = useRedirectUser();

    useEffect(() => {
        redirectUser();
    }, [redirectUser]);
  return (
    <div>
      <TableComponent />
    </div>
  );
};

export default Waiter;
