import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';



interface TableData {
    table_id: number;
    capacity: number;
    table_status: 'vacant' | 'reserved' | 'eating';
}

interface OrderItem {
    item_name: string;
    quantity: number;
    price: number;
}

interface OrderData {
    order_id: string;
    items: OrderItem[];
    created_at: string;
    is_served: boolean;
}


interface MenuItem {
    menu_item_id: string;
    menu_section_id: number;
    item_name: string;
    note: string;
    price: number;
}


export async function fetchTableData(): Promise<TableData[]> {
    const token = localStorage.getItem('access_token');
    const response = await axios.get<TableData[]>(`${API_URL}/users/waiter/tables`, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    return response.data;
}

export async function fetchMenuItems(): Promise<MenuItem[]> {
    const token = localStorage.getItem('access_token');
    const response = await axios.get(`${API_URL}/users/waiter/tables/menu-items`, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    const menuData = Array.isArray(response.data) ? response.data : response.data.menuItems || [];
    return menuData;
}

export async function updateTableStatus(table_id: number): Promise<void> {
    const token = localStorage.getItem('access_token');
        await axios.put(`${API_URL}/users/waiter/tables/reserve`, 
            { table_id },
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        );
}

export async function createOrder(selectedTableId: number, orderItems: Record<string, number>): Promise<void> {
    const token = localStorage.getItem('access_token');
    await axios.post(
        `${API_URL}/users/waiter/create-order`,
        {
            table_id: selectedTableId,
            dishes: Object.entries(orderItems).map(([id, quantity]) => ({
                menu_item_id: id,
                quantity,
            })),
        },
        {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
        }
    );
}

export async function viewOrder(selectedTableId: number): Promise<OrderData> {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await axios.get<OrderData>(`${API_URL}/users/waiter/tables/${selectedTableId}/order`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
        });
        
        // Check if response.data matches the expected OrderData structure
        const orderData: OrderData = response.data;
        
        // Validate the order data format if needed
        if (!orderData.items || !Array.isArray(orderData.items)) {
            throw new Error('Invalid order items format');
        }
        
        return orderData;
    } catch (error) {
        console.error('Error fetching order data:', error);
        throw error; // Re-throw the error to handle it in the calling function
    }
}

export async function makePayment(table_id: number): Promise<void> {
    const token = localStorage.getItem('access_token');
        await axios.put(`${API_URL}/users/waiter/orders/${table_id}/serve`,
            {},
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
            }
        );
}