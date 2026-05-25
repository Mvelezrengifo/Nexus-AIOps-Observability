import React from 'react';
import { Bell, User, Search } from 'lucide-react';

export const TopBar = () => {
  const user = { name: 'Admin', role: 'Administrator' };
  const logout = () => console.log('logout');

  return (
    <header className="h-16 bg-gray-900 border-b border-gray-800 fixed top-0 right-0 left-64 z-10">
      <div className="h-full flex items-center justify-between px-6">
        {/* Logo pequeño solo para móvil o respaldo (opcional) */}
        <div className="flex items-center gap-2 lg:hidden">
          <img src="/nexus-logo.svg" alt="Nexus Logo" className="h-8 w-auto" />
        </div>
        <div className="relative w-96">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 w-4 h-4" />
          <input
            type="text"
            placeholder="Search events, insights..."
            className="w-full bg-gray-800 rounded-lg pl-10 pr-4 py-2 text-gray-300 placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>
        <div className="flex items-center gap-4">
          <button className="relative p-2 text-gray-400 hover:text-white transition-colors">
            <Bell className="w-5 h-5" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
          <div className="flex items-center gap-3 pl-4 border-l border-gray-700">
            <div className="text-right">
              <p className="text-sm text-white">{user?.name || 'Admin'}</p>
              <p className="text-xs text-gray-400">{user?.role || 'Administrator'}</p>
            </div>
            <button
              onClick={logout}
              className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center text-white hover:bg-gray-600"
            >
              <User className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};