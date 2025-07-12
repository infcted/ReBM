import React, { useState } from 'react';
import Modal from './Modal';

interface CreateNodeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (nodeName: string) => void;
  isLoading: boolean;
}

const CreateNodeModal: React.FC<CreateNodeModalProps> = ({ isOpen, onClose, onSubmit, isLoading }) => {
  const [nodeName, setNodeName] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (nodeName.trim()) {
      onSubmit(nodeName.trim());
      setNodeName('');
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Create New Node">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="nodeName" className="block text-sm font-medium text-gray-700 mb-1">
            Node Name
          </label>
          <input
            type="text"
            id="nodeName"
            value={nodeName}
            onChange={(e) => setNodeName(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter node name"
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
            disabled={isLoading || !nodeName.trim()}
          >
            {isLoading ? 'Creating...' : 'Create Node'}
          </button>
        </div>
      </form>
    </Modal>
  );
};

export default CreateNodeModal; 