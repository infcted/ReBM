import React, { useState, useEffect } from 'react';
import { nodeService } from './services/api';
import { Node } from './types';

function App() {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showReserveModal, setShowReserveModal] = useState(false);
  const [selectedNode, setSelectedNode] = useState<string>('');
  const [actionLoading, setActionLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState<'online' | 'offline' | 'checking'>('checking');

  // Form states
  const [newNodeName, setNewNodeName] = useState('');
  const [reserveUser, setReserveUser] = useState('');
  const [reserveExpiresAt, setReserveExpiresAt] = useState('');

  // Load nodes on component mount
  useEffect(() => {
    loadNodes();
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      await nodeService.healthCheck();
      setApiStatus('online');
    } catch (error) {
      setApiStatus('offline');
    }
  };

  const loadNodes = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await nodeService.listNodes();
      setNodes(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load nodes');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNode = async () => {
    if (!newNodeName.trim()) return;
    
    try {
      setActionLoading(true);
      await nodeService.createNode({ node_name: newNodeName.trim() });
      setShowCreateModal(false);
      setNewNodeName('');
      await loadNodes();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create node');
    } finally {
      setActionLoading(false);
    }
  };

  const handleReserveNode = async () => {
    if (!reserveUser.trim() || !reserveExpiresAt) return;
    
    try {
      setActionLoading(true);
      // Convert local datetime to ISO string with timezone
      const localDateTime = new Date(reserveExpiresAt);
      const isoString = localDateTime.toISOString();
      
      await nodeService.reserveNode(selectedNode, { 
        user: reserveUser.trim(), 
        expires_at: isoString
      });
      setShowReserveModal(false);
      setReserveUser('');
      setReserveExpiresAt('');
      await loadNodes();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to reserve node');
    } finally {
      setActionLoading(false);
    }
  };

  const handleReleaseNode = async (nodeName: string) => {
    try {
      setActionLoading(true);
      await nodeService.releaseNode(nodeName);
      await loadNodes();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to release node');
    } finally {
      setActionLoading(false);
    }
  };

  const handleDeleteNode = async (nodeName: string) => {
    if (!window.confirm(`Are you sure you want to delete node "${nodeName}"?`)) {
      return;
    }

    try {
      setActionLoading(true);
      await nodeService.deleteNode(nodeName);
      await loadNodes();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete node');
    } finally {
      setActionLoading(false);
    }
  };

  const handleCleanup = async () => {
    try {
      setActionLoading(true);
      const result = await nodeService.cleanupExpiredNodes();
      await loadNodes();
      alert(result.message);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to cleanup expired nodes');
    } finally {
      setActionLoading(false);
    }
  };

  const openReserveModal = (nodeName: string) => {
    setSelectedNode(nodeName);
    setShowReserveModal(true);
    // Set default expiration to 1 hour from now
    const now = new Date();
    now.setHours(now.getHours() + 1);
    setReserveExpiresAt(now.toISOString().slice(0, 16));
  };

  const getStatusColor = (status: string) => {
    if (status === 'available') return 'text-green-600';
    if (status === 'reserved') return 'text-yellow-600';
    return 'text-gray-600';
  };

  const formatDateTime = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleString();
    } catch {
      return dateString;
    }
  };

  const isExpired = (expiresAt: string | null | undefined) => {
    if (!expiresAt) return false;
    try {
      return new Date(expiresAt) < new Date();
    } catch {
      return false;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <h1 className="text-2xl font-bold text-gray-900">ReBM Node Manager</h1>
              <div className="flex items-center space-x-1">
                <span className={`w-3 h-3 rounded-full ${apiStatus === 'online' ? 'bg-green-500' : apiStatus === 'offline' ? 'bg-red-500' : 'bg-yellow-500'}`}></span>
                <span className="text-sm text-gray-600 capitalize">{apiStatus}</span>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={handleCleanup}
                disabled={actionLoading}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors disabled:opacity-50"
              >
                Cleanup Expired
              </button>
              <button
                onClick={loadNodes}
                disabled={loading}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors disabled:opacity-50"
              >
                Refresh
              </button>
              <button
                onClick={() => setShowCreateModal(true)}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors"
              >
                Add Node
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Display */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="mt-2 text-sm text-red-700">{error}</div>
              </div>
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
            <span className="ml-2 text-gray-600">Loading nodes...</span>
          </div>
        ) : (
          <>
            {/* Stats */}
            <div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="text-2xl font-bold text-gray-900">{nodes.length}</div>
                <div className="text-sm text-gray-600">Total Nodes</div>
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <div className="text-2xl font-bold text-green-600">
                  {nodes.filter(n => n.status === 'available').length}
                </div>
                <div className="text-sm text-gray-600">Available</div>
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <div className="text-2xl font-bold text-yellow-600">
                  {nodes.filter(n => n.status === 'reserved').length}
                </div>
                <div className="text-sm text-gray-600">Reserved</div>
              </div>
            </div>

            {/* Nodes List */}
            {nodes.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-gray-400 mb-4">No nodes found</div>
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors"
                >
                  Create your first node
                </button>
              </div>
            ) : (
              <div className="bg-white shadow overflow-hidden sm:rounded-md">
                <ul className="divide-y divide-gray-200">
                  {nodes.map((node) => (
                    <li key={node.node} className="px-6 py-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center flex-1">
                          <div className="flex-shrink-0">
                            <div className="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                              <span className="text-sm font-medium text-gray-700">{node.node.charAt(0).toUpperCase()}</span>
                            </div>
                          </div>
                          <div className="ml-4 flex-1">
                            <div className="text-sm font-medium text-gray-900">{node.node}</div>
                            <div className="text-sm text-gray-500 space-y-1">
                              <div>
                                Status: <span className={getStatusColor(node.status)}>{node.status}</span>
                                {isExpired(node.expires_at) && <span className="text-red-600 ml-2">(EXPIRED)</span>}
                              </div>
                              {node.reserved_by && (
                                <div>Reserved by: <span className="font-medium">{node.reserved_by}</span></div>
                              )}
                              {node.expires_at && (
                                <div>
                                  Expires: <span className="font-medium">{formatDateTime(node.expires_at)}</span>
                                </div>
                              )}
                              <div>Updated: {formatDateTime(node.updated_at)}</div>
                            </div>
                          </div>
                        </div>
                        <div className="flex space-x-2 ml-4">
                          {node.status === 'available' ? (
                            <button
                              onClick={() => openReserveModal(node.node)}
                              className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
                            >
                              Reserve
                            </button>
                          ) : (
                            <button
                              onClick={() => handleReleaseNode(node.node)}
                              className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700"
                            >
                              Release
                            </button>
                          )}
                          <button
                            onClick={() => handleDeleteNode(node.node)}
                            className="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700"
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
      </main>

      {/* Create Node Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">Create New Node</h2>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
            <div className="p-6">
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Node Name
                </label>
                <input
                  type="text"
                  value={newNodeName}
                  onChange={(e) => setNewNodeName(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter node name"
                  disabled={actionLoading}
                />
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
                  disabled={actionLoading}
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreateNode}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                  disabled={actionLoading || !newNodeName.trim()}
                >
                  {actionLoading ? 'Creating...' : 'Create Node'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Reserve Node Modal */}
      {showReserveModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">Reserve Node: {selectedNode}</h2>
              <button
                onClick={() => setShowReserveModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
            <div className="p-6">
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  User Name
                </label>
                <input
                  type="text"
                  value={reserveUser}
                  onChange={(e) => setReserveUser(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter your name"
                  disabled={actionLoading}
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Expires At
                </label>
                <input
                  type="datetime-local"
                  value={reserveExpiresAt}
                  onChange={(e) => setReserveExpiresAt(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={actionLoading}
                />
                <p className="text-xs text-gray-500 mt-1">
                  You can select today's date and any time from now onwards
                </p>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={() => setShowReserveModal(false)}
                  className="flex-1 px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
                  disabled={actionLoading}
                >
                  Cancel
                </button>
                <button
                  onClick={handleReserveNode}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                  disabled={actionLoading || !reserveUser.trim() || !reserveExpiresAt}
                >
                  {actionLoading ? 'Reserving...' : 'Reserve Node'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App; 