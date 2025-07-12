import axios, { AxiosResponse } from 'axios';
import { Node, CreateNodeRequest, ReserveNodeRequest, ApiResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const nodeService = {
  // Get all nodes
  async listNodes(): Promise<Node[]> {
    const response: AxiosResponse<Node[]> = await api.get('/nodes/');
    return response.data;
  },

  // Get a specific node
  async getNode(nodeName: string): Promise<Node> {
    const response: AxiosResponse<Node> = await api.get(`/nodes/${nodeName}`);
    return response.data;
  },

  // Create a new node
  async createNode(nodeData: CreateNodeRequest): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await api.post('/nodes/', nodeData);
    return response.data;
  },

  // Delete a node
  async deleteNode(nodeName: string): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await api.delete(`/nodes/${nodeName}`);
    return response.data;
  },

  // Reserve a node
  async reserveNode(nodeName: string, reserveData: ReserveNodeRequest): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await api.post(`/nodes/${nodeName}/reserve`, reserveData);
    return response.data;
  },

  // Release a node
  async releaseNode(nodeName: string): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await api.post(`/nodes/${nodeName}/release`);
    return response.data;
  },

  // Cleanup expired nodes
  async cleanupExpiredNodes(): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await api.post('/nodes/cleanup/expired');
    return response.data;
  },

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response: AxiosResponse<{ status: string }> = await api.get('/health');
    return response.data;
  },
};

export default api; 