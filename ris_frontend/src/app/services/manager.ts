
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';


interface MenuItem {
  menu_item_id: string;
  item_name: string;
  note: string;
  price: number;
}

interface MenuSection {
  section_name: string;
  menu_section_id: number;
  menu_items: MenuItem[];
}

export async function fetchMenu(): Promise<MenuSection[]> {
    const token = localStorage.getItem('access_token');
    const response = await axios.get<MenuSection[]>(`${API_URL}/users/manager/menu-sections`, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    return response.data;
}

export async function addSection(sectionName: string) {
    try {
        const token = localStorage.getItem('access_token');
        await axios.post(`${API_URL}/users/manager/menu-sections`, 
            { section_name: sectionName },
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        );
    } catch (error) {
        console.error('Error adding menu section:', error);
    }
}

export async function addMenuItem(itemName: string, itemNote: string, itemPrice: number, menu_section_id: number) {
    try {
        const token = localStorage.getItem('access_token');
        await axios.post(`${API_URL}/users/manager/menu-items`, 
            {
                item_name: itemName,
                note: itemNote,
                price: itemPrice,
                menu_section_id: menu_section_id
            },
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        );
    } catch (error) {
        console.error('Error adding menu section:', error);
    }
}


export async function deleteSection(menu_section_id: number) {
    try {
        const token = localStorage.getItem('access_token');
        await axios.delete(`${API_URL}/users/manager/menu-sections/${menu_section_id}/delete`, 
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        );
    } catch (error) {
        console.error('Error adding menu section:', error);
    }
}

export async function deleteMenuItem(menu_item_id: string) {
    try {
        const token = localStorage.getItem('access_token');
        await axios.delete(`${API_URL}/users/manager/menu-items/${menu_item_id}/delete`, 
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        );
    } catch (error) {
        console.error('Error adding menu section:', error);
    }
}

export async function editMenuItem(menu_item_id: string, itemName: string, itemNote: string, itemPrice: number, menu_section_id: number) {
    try {
        const token = localStorage.getItem('access_token');
        await axios.put(`${API_URL}/users/manager/menu-items/${menu_item_id}`, 
            {
                item_name: itemName,
                note: itemNote,
                price: itemPrice,
                menu_section_id: menu_section_id
            },
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        );
    } catch (error) {
        console.error('Error adding menu section:', error);
    }
}


