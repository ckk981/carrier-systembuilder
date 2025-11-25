# QRinventorymanager

A lightweight, serverless inventory management application built with React, Vite, and Tailwind CSS. It leverages QR codes for quick stock adjustments and uses LocalStorage for data persistence.

## Features

*   **QR Code Scanning**: Integrated `html5-qrcode` scanner for fast item interaction.
*   **Role-Based Access Control**:
    *   **Admin**: Full access to Add, Remove, and View stock.
    *   **Staff**: Restricted access (Remove and View only).
*   **Inventory Management**:
    *   **Add Stock**: Scan a QR code. If new, register it; if existing, increment stock.
    *   **Remove Stock**: Scan an item and specify quantity to remove.
    *   **View Inventory**: Searchable list of all items and current stock levels.
*   **Responsive Design**: Optimized for mobile devices to facilitate on-the-go scanning.
*   **Offline Persistence**: Data is saved to the browser's `localStorage`.

## Tech Stack

*   **Framework**: [React](https://react.dev/) + [Vite](https://vitejs.dev/)
*   **Styling**: [Tailwind CSS](https://tailwindcss.com/) (v4)
*   **QR Scanning**: [html5-qrcode](https://github.com/mebjas/html5-qrcode)
*   **Icons**: [Lucide React](https://lucide.dev/)

## Setup & Installation

This project requires Node.js. If you are running this in an environment where Node.js is not globally installed, you can use the local setup provided in `./local_node`.

### 1. Install Dependencies

```bash
export PATH=$PWD/local_node/bin:$PATH
npm install
```

### 2. Run Development Server

To start the app locally:

```bash
npm run dev
```

To make the app accessible to other devices on your network (e.g., for mobile testing):

```bash
npm run dev:host
```

### 3. Build for Production

```bash
npm run build
```

The output will be in the `dist/` directory.

## Project Structure

```
QRinventorymanager/
├── src/
│   ├── components/      # Reusable UI components (Scanner, InventoryList)
│   ├── styles/          # Global styles and Tailwind config
│   ├── App.jsx          # Main application logic and state
│   └── main.jsx         # Entry point
├── public/              # Static assets
├── index.html           # HTML entry point
├── package.json         # Dependencies and scripts
└── vite.config.js       # Vite configuration
```

## Usage Guide

1.  **Select Role**: On launch, choose **Admin** or **Staff**.
2.  **Add Item (Admin only)**:
    *   Go to "Add Stock".
    *   Scan a QR code.
    *   Enter a name if it's a new item.
3.  **Remove Item**:
    *   Go to "Remove Stock".
    *   Scan the item's QR code.
    *   Enter the quantity to remove.
4.  **View Inventory**:
    *   Go to "View Inventory" to see a list of all items.
    *   Use the search bar to filter by name or ID.
