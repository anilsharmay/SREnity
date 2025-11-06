import React from 'react';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <>
      <div className="sidebar-overlay" onClick={onClose} />
      <div className="sidebar">
        <div className="sidebar-header">
          <h2>Menu</h2>
          <button className="sidebar-close" onClick={onClose}>×</button>
        </div>
        <div className="sidebar-content">
          <div className="sidebar-item">Dashboard</div>
          <div className="sidebar-item">Services</div>
          <div className="sidebar-item">Alerts</div>
          <div className="sidebar-item">Analytics</div>
          <div className="sidebar-item">Settings</div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;

