'use client'

import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableRow, Button, Paper, Box, Typography, Modal, Backdrop, Fade, IconButton } from '@mui/material';
import { Add, Remove } from '@mui/icons-material';

interface TableData {
    table_id: number;
    capacity: number;
    table_status: 'vacant' | 'reserved' | 'eating';
}

interface OrderData {
    order_id: number;
    table_id: number;
    items: string[];
    status: string;
}

interface MenuItem {
    menu_item_id: string;
    menu_section_id: number;
    item_name: string;
    note: string;
    price: number;
}

const TablesComponent: React.FC = () => {
    const [data, setData] = useState<TableData[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [orderData, setOrderData] = useState<OrderData | null>(null);
    const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
    const [open, setOpen] = useState(false);
    const [selectedTableId, setSelectedTableId] = useState<number | null>(null);
    const [orderItems, setOrderItems] = useState<{ [key: string]: number }>({});

    useEffect(() => {
        const fetchTableData = async () => {
            try {
                const response = await axios.get<TableData[]>('http://localhost:9000/api/table/thanhdat');
                setData(response.data);
                setError(null); // Clear previous errors if successful
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
                setError(errorMessage);
                console.error('Error fetching table data:', errorMessage);
            }
        };

        fetchTableData();
    }, []);

    useEffect(() => {
        const fetchMenuItems = async () => {
            try {
                const response = await axios.get('http://localhost:9000/api/menu/thanhdat');
                console.log('Full response:', response);
                // Check if data is an array or needs to be accessed differently
                const menuData = Array.isArray(response.data) ? response.data : response.data.menuItems || [];
                console.log('Menu items from response:', menuData);
                setMenuItems(menuData);
            } catch (error) {
                console.error('Error fetching menu items:', error);
            }
        };

        fetchMenuItems();
    }, []);

    const getButtonLabel = (status: string) => {
        switch (status) {
            case 'vacant':
                return 'Check-in';
            case 'reserved':
                return 'Make Order';
            case 'eating':
                return 'View Order';
            default:
                return '';
        }
    };

    const handleCheckIn = async (tableId: number) => {
        try {
            await axios.put(`http://localhost:9000/api/tables/checkin/${tableId}`);
            const response = await axios.get<TableData[]>('http://localhost:9000/api/table/thanhdat');
            setData(response.data);
        } catch (error) {
            console.error('Error checking in:', error);
        }
    };

    const handleMakeOrder = (tableId: number) => {
        setSelectedTableId(tableId);
        setOrderItems({});
        setOpen(true);
    };

    const handleViewOrder = async (tableId: number) => {
        try {
            const response = await axios.get<OrderData>(`http://localhost:9000/api/orders/${tableId}`);
            setOrderData(response.data);
            setOpen(true);
        } catch (error) {
            console.error('Error fetching order data:', error);
        }
    };

    const handleClose = () => {
        setOpen(false);
        setOrderData(null);
        setSelectedTableId(null);
    };

    const handleIncrement = (itemId: string) => {
        setOrderItems((prevOrderItems) => ({
            ...prevOrderItems,
            [itemId]: (prevOrderItems[itemId] || 0) + 1,
        }));
        console.log('Order Items:', orderItems);

    };

    const handleDecrement = (itemId: string) => {
        setOrderItems((prevOrderItems) => ({
            ...prevOrderItems,
            [itemId]: Math.max((prevOrderItems[itemId] || 0) - 1, 0),
        }));
    };

    const handleSubmitOrder = async () => {
        if (selectedTableId !== null) {
            try {
                await axios.post(`http://localhost:9000/api/order`, {
                    table_id: selectedTableId,
                    dishes: Object.entries(orderItems).map(([id, quantity]) => ({
                        menu_item_id: id,
                        quantity,
                    })),
                }, {
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                setOpen(false);
            } catch (error) {
                console.error('Error submitting order:', error);
            }
        }
    };

    return (
        <Box mt={20} display="flex" justifyContent="center" sx={{ width: '100%' }}>
            <TableContainer component={Paper}>
                <Table>
                    <TableBody>
                        {data.reduce((rows, row, index) => {
                            if (index % 5 === 0) rows.push([]);
                            rows[rows.length - 1].push(row);
                            return rows;
                        }, [] as TableData[][]).map((rowGroup, rowIndex) => (
                            <TableRow key={rowIndex} sx={{ height: '150px' }}>
                                {rowGroup.map((item) => (
                                    <TableCell key={item.table_id} align="center">
                                        <Typography sx={{ paddingBottom: '10px', fontWeight: '600' }}>{`Table ${item.table_id}`}</Typography>
                                        <Button
                                            variant="contained"
                                            color="primary"
                                            sx={{ width: '150px', height: '70px' }}
                                            onClick={() => {
                                                if (item.table_status === 'vacant') handleCheckIn(item.table_id);
                                                if (item.table_status === 'reserved') handleMakeOrder(item.table_id);
                                                if (item.table_status === 'eating') handleViewOrder(item.table_id);
                                            }}
                                        >
                                            {getButtonLabel(item.table_status)}
                                        </Button>
                                    </TableCell>
                                ))}
                                {Array(5 - rowGroup.length).fill(null).map((_, emptyIndex) => (
                                    <TableCell key={emptyIndex} />
                                ))}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            <Modal
                open={open}
                onClose={handleClose}
            >
                <Fade in={open}>
                    <Box sx={{ bgcolor: 'background.paper', boxShadow: 24, p: 4, width: 400, margin: 'auto', mt: '10%' }}>
                        <Typography variant="h6" component="h2">
                            {orderData ? 'View Order' : 'Make Order'}
                        </Typography>
                        <Box sx={{ mt: 2 }}>
                            {orderData ? (
                                <ul>
                                    {orderData.items.map((item) => (
                                        <li key={item}>{item}</li>
                                    ))}
                                </ul>
                            ) : (
                                <Box>
                                    {Array.isArray(menuItems) && menuItems.length > 0 ? (
                                        <Box sx={{ maxHeight: 300, overflowY: 'auto' }}>
                                            {menuItems.map((item) => (
                                                <Box key={item.menu_item_id} display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                                                    <Typography sx={{ color: 'black' }}>{item.item_name}</Typography>
                                                    <Box display="flex" alignItems="center">
                                                        <IconButton onClick={() => handleDecrement(item.menu_item_id)}><Remove /></IconButton>
                                                        <Typography sx={{ color: 'black' }}>{orderItems[item.menu_item_id] || 0}</Typography>
                                                        <IconButton onClick={() => handleIncrement(item.menu_item_id)}><Add /></IconButton>
                                                    </Box>
                                                </Box>
                                            ))}
                                        </Box>
                                    ) : (
                                        <Typography>No menu items available</Typography>
                                    )}
                                    <Button variant="contained" onClick={handleSubmitOrder} sx={{ mt: 2 }}>Submit Order</Button>
                                </Box>
                            )}
                        </Box>
                        <Button onClick={handleClose} sx={{ mt: 2 }}>Close</Button>
                    </Box>
                </Fade>
            </Modal>
        </Box>
    );
};

export default TablesComponent;
