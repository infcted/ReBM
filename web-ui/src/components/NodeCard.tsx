import React from 'react';
import { Node } from '../types';
import { formatDistanceToNow } from 'date-fns';
import { Clock, User, Server, CheckCircle, XCircle } from 'lucide-react';

interface NodeCardProps {
  node: Node;
  onReserve: (nodeName: string) => void;
  onRelease: (nodeName: string) => void;
  onDelete: (nodeName: string) => void;
}

const NodeCard: React.FC<NodeCardProps> = ({ node, onReserve, onRelease, onDelete }) => {
  const isReserved = node.status === 'reserved';
  const isExpired = node.expires_at && new Date(node.expires_at) < new Date();

  const getStatusColor = () => {
    if (isExpired) return 'bg-red-100 text-red-800';
    if (isReserved) return 'bg-yellow-100 text-yellow-800';
    return 'bg-green-100 text-green-800';
  };

  const getStatusIcon = () => {
    if (isExpired) return <XCircle className="w-4 h-4" />;
    if (isReserved) return <Clock className="w-4 h-4" />;
    return <CheckCircle className="w-4 h-4" />;
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Server className="w-5 h-5 text-gray-600" />
          <h3 className="text-lg font-semibold text-gray-900">{node.node}</h3>
        </div>
        <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium ${getStatusColor()}`}>
          {getStatusIcon()}
          <span className="capitalize">{node.status}</span>
        </div>
      </div>

      <div className="space-y-2 mb-4">
        {isReserved && node.reserved_by && (
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <User className="w-4 h-4" />
            <span>Reserved by: {node.reserved_by}</span>
          </div>
        )}
        
        {node.expires_at && (
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Clock className="w-4 h-4" />
            <span>
              {isExpired ? 'Expired' : 'Expires'} {formatDistanceToNow(new Date(node.expires_at), { addSuffix: true })}
            </span>
          </div>
        )}

        <div className="text-xs text-gray-500">
          Updated {formatDistanceToNow(new Date(node.updated_at), { addSuffix: true })}
        </div>
      </div>

      <div className="flex space-x-2">
        {!isReserved ? (
          <button
            onClick={() => onReserve(node.node)}
            className="flex-1 bg-blue-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors"
          >
            Reserve
          </button>
        ) : (
          <button
            onClick={() => onRelease(node.node)}
            className="flex-1 bg-green-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-green-700 transition-colors"
          >
            Release
          </button>
        )}
        
        <button
          onClick={() => onDelete(node.node)}
          className="bg-red-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-red-700 transition-colors"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default NodeCard; 