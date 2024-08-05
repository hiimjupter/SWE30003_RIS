'use client'

import React, { useEffect, useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Button, Paper, Box, Typography } from '@mui/material';
import axios from 'axios';
import { fetchDishes, updateDishStatus } from '@/app/services/chef';
import { updateTableStatus } from '@/app/services/waiter';

interface Dish {
    dish_id: string;
    order_id: string;
    table_id: number;
    item_name: string;
    quantity: number;
    dish_status: 'received' | 'prepared' | 'ready';
}

const DishesComponent: React.FC = () => {
    const [dishes, setDishes] = useState<Dish[]>([]);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadData = async () => {
            try {
                const response = await fetchDishes();
                setDishes(response);
                setError(null);
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
                setError(errorMessage);
                console.error('Error fetching dishes:', errorMessage);
            }
        };

        loadData();
    }, []);


    const handleUpdateDishStatus = async (dishId: string) => {
        try {
            const newStatus = await updateDishStatus(dishId);
            setDishes(prevDishes =>
                prevDishes.map(dish =>
                    dish.dish_id === dishId
                        ? { ...dish, dish_status: newStatus }
                        : dish
                ).filter(dish => newStatus !== 'ready' || dish.dish_id !== dishId) // Remove dish if newStatus is 'ready'
            );
        } catch (error) {
            console.error('Error updating dish status:', error);
        }
    };

    return (
        <Box mt={10} display="flex" justifyContent="center" sx={{ width: '100%' }}>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Dish ID</TableCell>
                            <TableCell>Order ID</TableCell>
                            <TableCell>Table ID</TableCell>
                            <TableCell>Item Name</TableCell>
                            <TableCell>Quantity</TableCell>
                            <TableCell>Status</TableCell>
                            <TableCell>Action</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {dishes.map(dish => (
                            <TableRow key={dish.dish_id}>
                                <TableCell>{dish.dish_id}</TableCell>
                                <TableCell>{dish.order_id}</TableCell>
                                <TableCell>{dish.table_id}</TableCell>
                                <TableCell>{dish.item_name}</TableCell>
                                <TableCell>{dish.quantity}</TableCell>
                                <TableCell>{dish.dish_status}</TableCell>
                                <TableCell>
                                    {dish.dish_status === 'received' && (
                                        <Button
                                            variant="contained"
                                            color="primary"
                                            onClick={() => handleUpdateDishStatus (dish.dish_id)}
                                        >
                                            Prepare
                                        </Button>
                                    )}
                                    {dish.dish_status === 'prepared' && (
                                        <Button
                                            variant="contained"
                                            color="primary"
                                            onClick={() => handleUpdateDishStatus (dish.dish_id)}
                                        >
                                            Ready
                                        </Button>
                                    )}
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            {error && <Typography color="error">{error}</Typography>}
        </Box>
    );
};

export default DishesComponent;
