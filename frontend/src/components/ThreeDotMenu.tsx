import React, { useState, useRef, useEffect } from 'react';

interface MenuOption {
  label: string;
  action: string;
  isAnalyze?: boolean;
}

interface ThreeDotMenuProps {
  options: MenuOption[];
  onSelect: (action: string) => void;
}

const ThreeDotMenu: React.FC<ThreeDotMenuProps> = ({ options, onSelect }) => {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const handleOptionClick = (action: string) => {
    onSelect(action);
    setIsOpen(false);
  };

  return (
    <div className="three-dot-menu" ref={menuRef}>
      <button
        className="three-dot-button"
        onClick={(e) => {
          e.stopPropagation();
          setIsOpen(!isOpen);
        }}
        aria-label="Open menu"
      >
        ⋮
      </button>
      {isOpen && (
        <div className="menu-dropdown">
          {options.map((option, index) => (
            <button
              key={index}
              className={`menu-item ${option.isAnalyze ? 'analyze' : ''}`}
              onClick={(e) => {
                e.stopPropagation();
                handleOptionClick(option.action);
              }}
            >
              {option.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default ThreeDotMenu;

