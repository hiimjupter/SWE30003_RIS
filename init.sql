CREATE SCHEMA ‘SWE30003_RIS’ ;

USE SWE30003_RIS;

-- Create table for roles
CREATE TABLE roles (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(255) NOT NULL UNIQUE,
    INDEX (role_id)
);

-- Create table for staff_accounts
CREATE TABLE staff_accounts (
    staff_id BINARY(16) PRIMARY KEY,
    role_id INT NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    gender ENUM('male', 'female', 'others') NOT NULL,
    dob DATE NOT NULL,
    created_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (role_id) REFERENCES roles(role_id),
    INDEX (username)
);

-- Create table for tables
CREATE TABLE tables (
    table_id INT PRIMARY KEY AUTO_INCREMENT,
    capacity INT NOT NULL,
    table_status ENUM('vacant', 'reserved', 'eating') NOT NULL DEFAULT 'vacant',
    INDEX (table_id)
);

-- Create table for orders
CREATE TABLE orders (
    order_id BINARY(16) PRIMARY KEY,
    table_id INT NOT NULL,
    staff_id BINARY(16) NOT NULL,
    is_served BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (table_id) REFERENCES tables(table_id),
    FOREIGN KEY (staff_id) REFERENCES staff_accounts(staff_id)
);

-- Create table for menu_sections
CREATE TABLE menu_sections (
    menu_section_id INT PRIMARY KEY AUTO_INCREMENT,
    section_name VARCHAR(255) NOT NULL,
    INDEX (menu_section_id)
);

-- Create table for menu_items
CREATE TABLE menu_items (
    menu_item_id BINARY(16) PRIMARY KEY,
    menu_section_id INT NOT NULL,
    item_name VARCHAR(255) NOT NULL UNIQUE,
    note VARCHAR(255),
    price FLOAT NOT NULL,
    FOREIGN KEY (menu_section_id) REFERENCES menu_sections(menu_section_id)
);

-- Create table for dishes
CREATE TABLE dishes (
    dish_id BINARY(16) PRIMARY KEY,
    order_id BINARY(16) NOT NULL,
    staff_id BINARY(16) NOT NULL,
    menu_item_id BINARY(16) NOT NULL,
    note VARCHAR(255),
    quantity INT NOT NULL,
    total FLOAT NOT NULL,
    dish_status ENUM('received', 'prepared', 'ready') NOT NULL DEFAULT 'received',
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (staff_id) REFERENCES staff_accounts(staff_id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id)
);

-- Insert data into roles
INSERT INTO roles (role_id, role_name) VALUES
(1, 'Waiter'),
(2, 'Chef'),
(3, 'Manager');

-- Insert data into staff_accounts
INSERT INTO staff_accounts (staff_id, role_id, username, password, full_name, gender, dob, created_at, is_active) VALUES
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440000'), 1, 'waiter', '$2b$12$l1W5CUtO/4U4Ofbz5x.X1.G4fVDKe7IfmTp.dGLZPGq1vsHQHldIO', 'Thanh Dat', 'male', '2003-05-02', '2024-07-30 00:00:00', TRUE),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440001'), 2, 'chef', '$2b$12$DTs5JYozpPO1XJr7NIdQ.O6MeoqgnJfayzFfR8TD/2CEnHvs7bw2i', 'Trung Hieu', 'female', '2003-07-11', '2024-07-30 00:00:00', TRUE),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440002'), 3, 'manager', '$2b$12$PN1D4m5M5JWoZvF3ZVfemuThMVHi36DUIunSEPmonvsQ.s6ywEqj2', 'Nghia Phat', 'others', '2003-05-10', '2024-07-30 00:00:00', TRUE);

-- Insert data into tables
INSERT INTO tables (table_id, capacity, table_status) VALUES
(1, 4, 'vacant'),
(2, 4, 'reserved'),
(3, 4, 'eating'),

-- Insert data into menu_sections
INSERT INTO menu_sections (menu_section_id, section_name) VALUES
(1, 'Main Courses'),
(2, 'Salads'),
(3, 'Desserts'),
(4, 'Drinks');

-- Insert data into menu-items
INSERT INTO menu_items (menu_item_id, menu_section_id, item_name, note, price) VALUES
-- Items into Main Courses
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440003'), 1, 'Beef Steak', 'Grilled to perfection', 15.0),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440004'), 1, 'Chicken Alfredo', 'Creamy Alfredo sauce', 13.5),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440005'), 1, 'Salmon Fillet', 'Served with lemon butter sauce', 17.0),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440006'), 1, 'Pasta Primavera', 'Fresh vegetables and pasta', 12.0),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440007'), 1, 'Pork Chop', 'Served with apple sauce', 14.0),
-- Items into Salads
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440008'), 2, 'Caesar Salad', 'Romaine lettuce, croutons, and Caesar dressing', 5.0),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440009'), 2, 'Greek Salad', 'Tomatoes, cucumbers, olives, and feta cheese', 6.0),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440010'), 2, 'Cobb Salad', 'Mixed greens, chicken, bacon, egg, and avocado', 6.5),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440011'), 2, 'Garden Salad', 'Mixed greens, tomatoes, cucumbers, and carrots', 7.2),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440012'), 2, 'Caprese Salad', 'Tomatoes, mozzarella, basil, and balsamic glaze', 4.99),
-- Items into Desserts
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440013'), 3, 'Chocolate Cake', 'Rich and moist chocolate cake', 4.99),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440014'), 3, 'Cheesecake', 'Creamy New York-style cheesecake', 5.99),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440015'), 3, 'Tiramisu', 'Classic Italian dessert with coffee and mascarpone', 6.49),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440016'), 3, 'Apple Pie', 'Traditional apple pie with a flaky crust', 4.49),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440017'), 3, 'Ice Cream Sundae', 'Vanilla ice cream with chocolate syrup and nuts', 3.99),
-- Items into Drinks
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440018'), 4, 'Coca-Cola', 'Refreshing classic cola', 1.25),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440019'), 4, 'Lemonade', 'Freshly squeezed lemonade', 1.50),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440020'), 4, 'Iced Tea', 'Chilled brewed tea with lemon', 1.75),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440021'), 4, 'Orange Juice', 'Freshly squeezed orange juice', 2.00),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440022'), 4, 'Mojito', 'Alcohol-free juice', 2.55),

-- Insert data into orders
INSERT INTO orders (order_id, table_id, staff_id, is_served, created_at) VALUES
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440023'), 3, UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440000'), FALSE, '2024-07-30 00:00:00'),

-- Insert data into dishes
INSERT INTO dishes (dish_id, order_id, staff_id, menu_item_id, note, quantity, total, dish_status) VALUES
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440024'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440023'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440000'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440003'), 'Less spicy', 2, 30.0, 'received'),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440025'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440023'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440000'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440004'), 'Extra cheese', 1, 13.5, 'prepared'),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440026'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440023'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440000'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440008'), 'No croutons', 3, 15.0, 'received'),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440027'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440023'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440000'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440016'), 'Warm', 2, 8.98, 'prepared'),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440028'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440023'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440000'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440018'), 'With ice', 1, 1.25, 'ready'),
(UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440029'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440023'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440000'), UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440019'), 'No ice', 1, 1.50, 'ready');
