import React, { useState } from 'react';
import { Search } from 'lucide-react';

/**
 * InventoryList Component
 * Displays a searchable list of all inventory items.
 * 
 * @param {Array} inventory - List of inventory items {id, name, quantity}
 */
const InventoryList = ({ inventory }) => {
    const [search, setSearch] = useState('');

    // Filter inventory based on search term (matches name or ID)
    const filtered = inventory.filter(item =>
        item.name.toLowerCase().includes(search.toLowerCase()) ||
        item.id.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="bg-white rounded-xl shadow-lg p-4 flex flex-col h-full overflow-hidden">
            {/* Search Bar */}
            <div className="relative mb-4">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                    type="text"
                    placeholder="Search items..."
                    className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-brand-500 outline-none"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                />
            </div>

            {/* Scrollable List */}
            <div className="flex-1 overflow-y-auto space-y-2">
                {filtered.length === 0 ? (
                    <p className="text-center text-gray-500 py-8">No items found.</p>
                ) : (
                    filtered.map((item, idx) => (
                        <div key={idx} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg border border-gray-100">
                            <div>
                                <h3 className="font-bold text-gray-800">{item.name}</h3>
                                <p className="text-xs text-gray-500 font-mono">{item.id}</p>
                            </div>
                            <div className="bg-brand-100 text-brand-900 px-3 py-1 rounded-full font-bold text-sm">
                                {item.quantity}
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default InventoryList;
