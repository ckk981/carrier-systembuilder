import React, { useEffect, useRef } from 'react';
import { Html5QrcodeScanner } from 'html5-qrcode';

/**
 * Scanner Component
 * Wraps the html5-qrcode library to provide a React-friendly QR scanner.
 * 
 * @param {function} onScan - Callback function triggered when a QR code is successfully scanned.
 */
const Scanner = ({ onScan }) => {
    const scannerRef = useRef(null);

    useEffect(() => {
        // Initialize the scanner with configuration
        const scanner = new Html5QrcodeScanner(
            "reader",
            { fps: 10, qrbox: { width: 250, height: 250 } },
            /* verbose= */ false
        );

        // Render the scanner and define success/error callbacks
        scanner.render((decodedText) => {
            // Success: Pass data to parent and clear scanner to prevent duplicate reads immediately
            onScan(decodedText);
            scanner.clear();
        }, (error) => {
            // Error: Scanning failed (common while moving camera), usually ignored to prevent console spam
            // console.warn(error);
        });

        scannerRef.current = scanner;

        // Cleanup: Ensure scanner is stopped when component unmounts
        return () => {
            if (scannerRef.current) {
                scannerRef.current.clear().catch(error => {
                    console.error("Failed to clear html5-qrcode scanner. ", error);
                });
            }
        };
    }, [onScan]);

    return (
        <div className="w-full max-w-sm mx-auto">
            {/* Container for the camera view */}
            <div id="reader" className="overflow-hidden rounded-lg shadow-lg border-2 border-brand-500"></div>
            <p className="text-center text-sm text-gray-500 mt-2">Point camera at a QR code</p>
        </div>
    );
};

export default Scanner;
