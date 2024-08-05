import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';


interface Dish {
    dish_id: string;
    order_id: string;
    table_id: number;
    item_name: string;
    quantity: number;
    dish_status: 'received' | 'prepared' | 'ready';
}

interface MenuItem {
    menu_item_id: string;
    menu_section_id: number;
    item_name: string;
    note: string;
    price: number;
}


export async function fetchDishes(): Promise<Dish[]> {
    const token = localStorage.getItem('access_token');
    const response = await axios.get<Dish[]>(`${API_URL}/users/chef/dishes`, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    return  response.data.filter(dish => dish.dish_status !== 'ready');
}


export async function updateDishStatus(dishId: string): Promise<'prepared' | 'ready'> {
    try {
        const token = localStorage.getItem('access_token');
        const response = await axios.put(`${API_URL}/users/chef/dishes/status-update`, {
            dish_id: dishId} , {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        // Return the new dish_status from the response data
        const { dish_status } = response.data;
        return dish_status;
    } catch (error) {
        console.error('Error updating dish status:', error);
        throw error; // Ensure the error is propagated
    }
}


