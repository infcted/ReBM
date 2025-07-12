export interface Node {
  node: string;
  status: 'available' | 'reserved';
  reserved_by?: string | null;
  expires_at?: string | null;
  updated_at: string;
  [key: string]: any; // For additional node properties
}

export interface CreateNodeRequest {
  node_name: string;
  [key: string]: any; // For additional properties
}

export interface ReserveNodeRequest {
  user: string;
  expires_at: string; // ISO format timestamp
}

export interface ApiResponse<T = any> {
  message?: string;
  status?: string;
  data?: T;
}

export interface ErrorResponse {
  detail: string;
} 