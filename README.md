# SWE30003_Restaurant Information System

## I. Introduction

- **Institution**: Swinburne Vietnam - Computer Science
- **Team name**: The Software Architect (Group 1)
- **Course code**: SWE30003
- **Course name**: Software Architecture and Design
- **Lecturer**: Dr. Trung Luu
- **Project**: This repository contains the source code for a comprehensive Restaurant Information System (RIS) developed for Relaxing Koala, a restaurant located in Hawthorn. The primary objective of this system is to transform the restaurant's manual operations into an efficient, automated process that enhances communication between various departments.

## II. Instructions

### 1. Clone the Repository

Choose your desired driver, open a terminal and clone this repository using the
```bash
git clone https://github.com/hiimjupter/SWE30003_RIS.git
```

### 2. Set up Database
- Install MySQL Community Server:
    - Download and install from [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
    - Save your username and password.
- Go to `root` terminal of the code:
    ```
    mysql -u [username] -p --> Enter your password
    source init.sql
    ```
![Illustration](/static/init.png)
- Configure `.env` file:
    - Direct to *backend folder* using terminal: `cd ris_backend`
    - Swap the username and the password as your database configuration.
![Illustration](/static/set_con.png)

### 3. Install Dependencies
- Make sure you have Python and Pip package on device
- Open two terminals:
    - One for the backend
    - One for the frontend
- Backend setup:
    - Begin at the *root* terminal of the folder.
    - Navigate to the *backend* folder: `cd ris_backend`
![Illustration](/static/backend.png)
    - Install dependencies: `pip install -r requirements.txt`
- Frontend setup:
    - Begin at the *root* terminal of the folder.
    - Navigate to the *frontend* folder: `cd ris_frontend`
![Illustration](/static/frontend.png)
    - Install dependencies:
```bash
npm install @mui/material @emotion/react @emotion/styled
npm install @mui/material @mui/styled-engine-sc styled-components
npm i axios
```

## III. Run the App
### 1. Initiate Server:
- Use the *backend* terminal:
```bash
uvicorn app.main:app --reload
```
### 2. Initiate Client:
- Use the *frontend* terminal:
```bash
npm run dev
```
### 3. Access
- Go to *browser* and paste in:
```bash
localhost:3000
```
- For waiter interface, use:
```bash
username: waiter
password: Waiter@123
```
- For chef interface, use:
```bash
username: chef
password: Chef@123
```
- For manager interface, use:
```bash
username: manager
password: Manager@123
```

## IV. Run Test Cases
### 1. Go to *backend* folder:
```
cd ris_backend
```
### 2. Run test cases:
- For login testcase, run:
```bash
pytest test_case/test_auth.py
```
- For waiter testcase, run:
```bash
pytest test_case/test_waiter.py
```
- For chef testcase, run:
```bash
pytest test_case/test_chef.py
```
- For manager testcase, run:
```bash
pytest test_case/test_manager.py
```

## V. Main Authors:
1. Hilton Nguyen: 103488337@student.swin.edu.au
2. Dajit Ngo: 104169057@student.swin.edu.au
3. Fatfat Chau: 104055677@student.swin.edu.au
4. Min Truong: 103845039@student.swin.edu.au
