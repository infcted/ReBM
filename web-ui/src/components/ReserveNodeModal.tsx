import React, { useState } from 'react';
import Modal from './Modal';

interface ReserveNodeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (user: string, expiresAt: string) => void;
  nodeName: string;
  isLoading: boolean;
}

const ReserveNodeModal: React.FC<ReserveNodeModalProps> = ({ 
  isOpen, 
  onClose, 
  onSubmit, 
  nodeName, 
  isLoading 
}) => {
  const [user, setUser] = useState('');
  const [expiresAt, setExpiresAt] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (user.trim() && expiresAt) {
      onSubmit(user.trim(), expiresAt);
      setUser('');
      setExpiresAt('');
    }
  };

  // Get current time in datetime-local format
  const getCurrentTime = () => {
    const now = new Date();
    return now.toISOString().slice(0, 16);
  };

  // Set default expiration time to 1 hour from now
  const getDefaultExpiration = () => {
    const now = new Date();
    now.setHours(now.getHours() + 1);
    return now.toISOString().slice(0, 16);
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Reserve Node: ${nodeName}`}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="user" className="block text-sm font-medium text-gray-700 mb-1">
            User Name
          </label>
          <input
            type="text"
            id="user"
            value={user}
            onChange={(e) => setUser(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter your name"
            required
            disabled={isLoading}
          />
        </div>

        <div>
          <label htmlFor="expiresAt" className="block text-sm font-medium text-gray-700 mb-1">
            Expires At
          </label>
          <input
            type="datetime-local"
            id="expiresAt"
            value={expiresAt}
            onChange={(e) => setExpiresAt(e.target.value)}
            min={getCurrentTime()}
            defaultValue={getDefaultExpiration()}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
            disabled={isLoading}
          />
        </div>
        
        <div className="flex space-x-3 pt-4">
          <button
            type="button"
            onClick={onClose}
            className="flex-1 px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
            disabled={isLoading}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50"
            disabled={isLoading || !user.trim() || !expiresAt}
          >
            {isLoading ? 'Reserving...' : 'Reserve Node'}
          </button>
        </div>
      </form>
    </Modal>
  );
};

export default ReserveNodeModal; 