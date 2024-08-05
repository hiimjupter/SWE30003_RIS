'use client'

import React, { useState, useEffect } from 'react';
import {
  Box, Button, Typography, Modal, Fade, TextField, IconButton, List, ListItem, ListItemText,
  ListItemSecondaryAction, Paper
} from '@mui/material';
import { Add, Edit, Delete } from '@mui/icons-material';
import axios from 'axios';
import { addMenuItem, addSection, deleteMenuItem, deleteSection, editMenuItem, fetchMenu } from '@/app/services/manager';

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

const MenuComponent: React.FC = () => {
  const [menuSections, setMenuSections] = useState<MenuSection[]>([]);
  const [selectedSection, setSelectedSection] = useState<MenuSection | null>(null);
  const [selectedItem, setSelectedItem] = useState<MenuItem | null>(null);
  const [openSectionModal, setOpenSectionModal] = useState(false);
  const [openItemModal, setOpenItemModal] = useState(false);
  const [openEditItemModal, setOpenEditItemModal] = useState(false);
  const [openDeleteSectionModal, setOpenDeleteSectionModal] = useState(false);
  const [openDeleteItemModal, setOpenDeleteItemModal] = useState(false);
  const [sectionName, setSectionName] = useState('');
  const [itemName, setItemName] = useState('');
  const [itemNote, setItemNote] = useState('');
  const [itemPrice, setItemPrice] = useState<number | string>('');
  const [editItemId, setEditItemId] = useState<string | null>(null);
  const [currentSectionId, setCurrentSectionId] = useState<number | null>(null);


  useEffect(() => {
    const loadData = async () => {
      try {
        const response = await fetchMenu();
        setMenuSections(response);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
        console.error(errorMessage);
      }
    };
    loadData();
  }, []);

  const handleAddSection = async () => {
    if (sectionName) {
      try {
        await addSection(sectionName);
        const updatedSections = await fetchMenu();
        setMenuSections(updatedSections);
        setSectionName('');
        setOpenSectionModal(false);
      } catch (error) {
        console.error('Error adding menu section:', error);
      }
    }
  };

  const handleAddItem = async () => {
    if (selectedSection && itemName && itemPrice) {
      try {
        await addMenuItem(itemName, itemNote, Number(itemPrice), selectedSection.menu_section_id);
        setItemName('');
        setItemNote('');
        setItemPrice('');
        setOpenItemModal(false);
        const updatedSections = await fetchMenu();
        setMenuSections(updatedSections);
      } catch (error) {
        console.error('Error adding menu item:', error);
      }
    }
  };

  const handleDeleteSection = async () => {
    if (selectedSection) {
      try {
        await deleteSection(selectedSection.menu_section_id);
        setSelectedSection(null);
        setOpenDeleteSectionModal(false);
        const updatedSections = await fetchMenu();
        setMenuSections(updatedSections);
      } catch (error) {
        console.error('Error deleting menu section:', error);
      }
    }
  };

    const handleEditItem = async () => {
    if (editItemId && itemName && itemPrice && currentSectionId !== null) {
        try {
        await editMenuItem(editItemId, itemName, itemNote, Number(itemPrice), currentSectionId);
        setEditItemId(null);
        setItemName('');
        setItemNote('');
        setItemPrice('');
        setCurrentSectionId(null); // Clear section ID after update
        setOpenEditItemModal(false);
        const updatedSections = await fetchMenu();
        setMenuSections(updatedSections);
        } catch (error) {
        console.error('Error editing menu item:', error);
        }
    }
    };


  const handleDeleteItem = async () => {
    if (selectedItem) {
      try {
        await deleteMenuItem(selectedItem.menu_item_id);
        setSelectedItem(null);
        setOpenDeleteItemModal(false);
        const updatedSections = await fetchMenu();
        setMenuSections(updatedSections);
      } catch (error) {
        console.error('Error deleting menu item:', error);
      }
    }
  };

  return (
    <Box p={3}>
      <Box display="flex" justifyContent="space-between" mb={3}>
        <Typography variant="h4">Menu Manager</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Add />}
          onClick={() => setOpenSectionModal(true)}
        >
          Add Menu Section
        </Button>
      </Box>

      {menuSections.map(section => (
        <Box key={section.menu_section_id} mb={3}>
          <Paper sx={{ p: 2, position: 'relative' }}>
            <Typography variant="h6">{section.section_name}</Typography>
            <Button
              variant="contained"
              color="secondary"
              startIcon={<Add />}
              onClick={() => {
                setSelectedSection(section);
                setOpenItemModal(true);
              }}
              sx={{ mb: 2 }}
            >
              Add Menu Item
            </Button>
            <Button
              variant="contained"
              color="error"
              onClick={() => {
                setSelectedSection(section);
                setOpenDeleteSectionModal(true);
              }}
              sx={{ position: 'absolute', top: 10, right: 10 }}
            >
              Delete Section
            </Button>
            <List>
              {section.menu_items.map(item => (
                <ListItem key={item.menu_item_id}>
                  <ListItemText
                    primary={item.item_name}
                    secondary={`Note: ${item.note}, Price: $${item.price}`}
                  />
                  <ListItemSecondaryAction>
                    <IconButton onClick={() => {
                        setItemName(item.item_name);
                        setItemNote(item.note);
                        setItemPrice(item.price);
                        setEditItemId(item.menu_item_id);
                        setCurrentSectionId(section.menu_section_id); // Set the section ID here
                        setOpenEditItemModal(true);
                    }}>
                        <Edit />
                    </IconButton>
                    <IconButton onClick={() => {
                      setSelectedItem(item);
                      setOpenDeleteItemModal(true);
                    }}>
                      <Delete />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Box>
      ))}

      {/* Add Section Modal */}
      <Modal
        open={openSectionModal}
        onClose={() => setOpenSectionModal(false)}
      >
        <Fade in={openSectionModal}>
          <Box sx={{ bgcolor: 'background.paper', boxShadow: 24, p: 4, width: 400, margin: 'auto', mt: '10%' }}>
            <Typography variant="h6" component="h2">Add Menu Section</Typography>
            <TextField
              label="Section Name"
              variant="outlined"
              fullWidth
              value={sectionName}
              onChange={(e) => setSectionName(e.target.value)}
              sx={{ mt: 2 }}
            />
            <Button
              variant="contained"
              color="primary"
              onClick={handleAddSection}
              sx={{ mt: 2 }}
            >
              Add Section
            </Button>
            <Button
              onClick={() => setOpenSectionModal(false)}
              sx={{ mt: 2, ml: 2 }}
            >
              Cancel
            </Button>
          </Box>
        </Fade>
      </Modal>

      {/* Add Item Modal */}
      <Modal
        open={openItemModal}
        onClose={() => setOpenItemModal(false)}
      >
        <Fade in={openItemModal}>
          <Box sx={{ bgcolor: 'background.paper', boxShadow: 24, p: 4, width: 400, margin: 'auto', mt: '10%' }}>
            <Typography variant="h6" component="h2">Add Menu Item</Typography>
            <TextField
              label="Item Name"
              variant="outlined"
              fullWidth
              value={itemName}
              onChange={(e) => setItemName(e.target.value)}
              sx={{ mt: 2 }}
            />
            <TextField
              label="Note"
              variant="outlined"
              fullWidth
              value={itemNote}
              onChange={(e) => setItemNote(e.target.value)}
              sx={{ mt: 2 }}
            />
            <TextField
              label="Price"
              type="number"
              variant="outlined"
              fullWidth
              value={itemPrice}
              onChange={(e) => setItemPrice(e.target.value)}
              sx={{ mt: 2 }}
            />
            <Button
              variant="contained"
              color="primary"
              onClick={handleAddItem}
              sx={{ mt: 2 }}
            >
              Add Item
            </Button>
            <Button
              onClick={() => setOpenItemModal(false)}
              sx={{ mt: 2, ml: 2 }}
            >
              Cancel
            </Button>
          </Box>
        </Fade>
      </Modal>

      {/* Edit Item Modal */}
      <Modal
        open={openEditItemModal}
        onClose={() => setOpenEditItemModal(false)}
      >
        <Fade in={openEditItemModal}>
          <Box sx={{ bgcolor: 'background.paper', boxShadow: 24, p: 4, width: 400, margin: 'auto', mt: '10%' }}>
            <Typography variant="h6" component="h2">Edit Menu Item</Typography>
            <TextField
              label="Item Name"
              variant="outlined"
              fullWidth
              value={itemName}
              onChange={(e) => setItemName(e.target.value)}
              sx={{ mt: 2 }}
            />
            <TextField
              label="Note"
              variant="outlined"
              fullWidth
              value={itemNote}
              onChange={(e) => setItemNote(e.target.value)}
              sx={{ mt: 2 }}
            />
            <TextField
              label="Price"
              type="number"
              variant="outlined"
              fullWidth
              value={itemPrice}
              onChange={(e) => setItemPrice(e.target.value)}
              sx={{ mt: 2 }}
            />
            <Button
              variant="contained"
              color="primary"
              onClick={handleEditItem}
              sx={{ mt: 2 }}
            >
              Save Changes
            </Button>
            <Button
              onClick={() => setOpenEditItemModal(false)}
              sx={{ mt: 2, ml: 2 }}
            >
              Cancel
            </Button>
          </Box>
        </Fade>
      </Modal>

      {/* Delete Section Modal */}
      <Modal
        open={openDeleteSectionModal}
        onClose={() => setOpenDeleteSectionModal(false)}
      >
        <Fade in={openDeleteSectionModal}>
          <Box sx={{ bgcolor: 'background.paper', boxShadow: 24, p: 4, width: 400, margin: 'auto', mt: '10%' }}>
            <Typography variant="h6" component="h2">Confirm Deletion</Typography>
            <Typography variant="body1">Are you sure you want to delete this section?</Typography>
            <Button
              variant="contained"
              color="error"
              onClick={handleDeleteSection}
              sx={{ mt: 2 }}
            >
              Delete
            </Button>
            <Button
              onClick={() => setOpenDeleteSectionModal(false)}
              sx={{ mt: 2, ml: 2 }}
            >
              Cancel
            </Button>
          </Box>
        </Fade>
      </Modal>

      {/* Delete Item Modal */}
      <Modal
        open={openDeleteItemModal}
        onClose={() => setOpenDeleteItemModal(false)}
      >
        <Fade in={openDeleteItemModal}>
          <Box sx={{ bgcolor: 'background.paper', boxShadow: 24, p: 4, width: 400, margin: 'auto', mt: '10%' }}>
            <Typography variant="h6" component="h2">Confirm Deletion</Typography>
            <Typography variant="body1">Are you sure you want to delete this item?</Typography>
            <Button
              variant="contained"
              color="error"
              onClick={handleDeleteItem}
              sx={{ mt: 2 }}
            >
              Delete
            </Button>
            <Button
              onClick={() => setOpenDeleteItemModal(false)}
              sx={{ mt: 2, ml: 2 }}
            >
              Cancel
            </Button>
          </Box>
        </Fade>
      </Modal>
    </Box>
  );
};

export default MenuComponent;
