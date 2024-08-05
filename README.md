# SWE30003_Restaurant Information System

## I. Introduction

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
- Install MySQL Workbench:
    - Download and install from [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)
- Login to Database:
    - Use the username and password configured during the `MySQL Community server` installation and login into `MySQL Workbench`
![Illustration](/static/login.png)
- Create Schema, Database, and Seed Data
    - Copy the SQL code from the `ini.sql` file in the repository and paste it into the MySQL Workbench
![Illustration](/static/ini.png)
- Configure `.env` file:
    - Direct to *backend folder* using terminal: `cd ris_backend`
    - Swap the username and the password as your database configuration.
![Illustration](/static/set_con.png)

### 3. Install Dependencies
- Open two terminals:
    - One for the backend
    - One for the frontend
- Backend setup:
    - Begin at the *root* terminal of the folder.
    - Navigate to the *backend* folder: `cd ris_backend`
    - Install dependencies: `pip install -r requirements.txt`
![Illustration](/static/backend.png)
- Frontend setup:
    - Begin at the *root* terminal of the folder.
    - Navigate to the *frontend* folder: `cd ris_frontend`
    - Install dependencies:
```bash
npm install @mui/material @emotion/react @emotion/styled
npm install @mui/material @mui/styled-engine-sc styled-components
npm i axios
```
![Illustration](/static/frontend.png)

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
