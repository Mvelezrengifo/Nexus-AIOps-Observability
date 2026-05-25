import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Zap, Brain, HeartPulse, Settings } from 'lucide-react';

const navItems = [
  { path: '/dashboard', name: 'Dashboard', icon: LayoutDashboard },
  { path: '/events', name: 'Events', icon: Zap },
  { path: '/insights', name: 'Insights', icon: Brain },
  { path: '/health', name: 'Health', icon: HeartPulse },
];

export const Sidebar = () => {
  return (
    <aside className="w-64 bg-gray-900 border-r border-gray-800 h-screen fixed left-0 top-0 flex flex-col">
      <div className="p-6 border-b border-gray-800">
        <div className="flex items-center gap-2">
          <img src="/nexus-logo.svg" alt="Nexus Logo" className="h-8 w-auto" />
          <span className="text-white font-bold text-xl">NEXUS</span>
        </div>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-gray-800">
        <button className="flex items-center gap-3 text-gray-400 hover:text-white w-full px-4 py-2 rounded-lg hover:bg-gray-800">
          <Settings className="w-5 h-5" />
          <span>Settings</span>
        </button>
      </div>
    </aside>
  );
};