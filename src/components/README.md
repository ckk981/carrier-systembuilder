# Components Documentation

This directory contains the reusable React components used in the QR Inventory application.

## `Scanner.jsx`

A wrapper around the `html5-qrcode` library to provide a React-friendly QR code scanner.

*   **Props**:
    *   `onScan` (function): Callback triggered when a QR code is successfully decoded. Receives the `decodedText` as an argument.
*   **Usage**:
    ```jsx
    <Scanner onScan={(data) => handleScan(data)} />
    ```
*   **Notes**:
    *   Handles camera permissions automatically.
    *   Cleans up the scanner instance on component unmount to prevent memory leaks.

## `InventoryList.jsx`

A presentation component that displays the inventory in a searchable list format.

*   **Props**:
    *   `inventory` (Array): An array of inventory objects. Each object should have:
        *   `id` (string): Unique identifier (QR code content).
        *   `name` (string): Display name of the item.
        *   `quantity` (number): Current stock level.
*   **Usage**:
    ```jsx
    <InventoryList inventory={currentInventoryState} />
    ```
*   **Features**:
    *   **Search**: Includes a search input that filters items by Name or ID.
    *   **Empty State**: Displays a friendly message if no items match the search or if the inventory is empty.
