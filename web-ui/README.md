# ReBM Web UI

A modern, responsive web interface for managing ReBM nodes. Built with React, TypeScript, and Tailwind CSS.

## Features

- 🖥️ **Node Management**: Create, view, reserve, release, and delete nodes
- 📊 **Real-time Status**: Live status indicators for node availability
- ⏰ **Expiration Tracking**: Automatic cleanup of expired reservations
- 🎨 **Modern UI**: Clean, responsive design with Tailwind CSS
- 🔄 **Auto-refresh**: Automatic status updates and health checks
- 📱 **Mobile Friendly**: Responsive design that works on all devices

## Prerequisites

- Node.js 16+ and npm
- ReBM API running on `http://localhost:8000` (or configure via environment variable)

## Installation

1. **Install dependencies**:
   ```bash
   cd web-ui
   npm install
   ```

2. **Configure API endpoint** (optional):
   Create a `.env` file in the web-ui directory:
   ```env
   REACT_APP_API_URL=http://localhost:8000
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

The application will open at `http://localhost:3000`.

## Usage

### Viewing Nodes
- The dashboard shows all nodes with their current status
- Available nodes are shown in green
- Reserved nodes are shown in yellow
- Expired reservations are automatically detected

### Creating Nodes
1. Click the "Add Node" button in the header
2. Enter a node name
3. Click "Create Node"

### Reserving Nodes
1. Click "Reserve" on an available node
2. Enter your name and expiration time
3. Click "Reserve Node"

### Releasing Nodes
- Click "Release" on a reserved node to make it available again

### Deleting Nodes
- Click "Delete" on any node (confirmation dialog will appear)

### Cleanup
- Click "Cleanup Expired" to manually trigger cleanup of expired reservations
- The API also runs automatic cleanup every 5 minutes

## API Endpoints

The web UI communicates with the following API endpoints:

- `GET /nodes/` - List all nodes
- `GET /nodes/{node}` - Get specific node
- `POST /nodes/` - Create new node
- `DELETE /nodes/{node}` - Delete node
- `POST /nodes/{node}/reserve` - Reserve node
- `POST /nodes/{node}/release` - Release node
- `POST /nodes/cleanup/expired` - Cleanup expired nodes
- `GET /health` - Health check

## Development

### Project Structure
```
web-ui/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── NodeCard.tsx
│   │   ├── Modal.tsx
│   │   ├── CreateNodeModal.tsx
│   │   └── ReserveNodeModal.tsx
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   ├── index.tsx
│   └── index.css
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── postcss.config.js
```

### Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

### Technologies Used

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **date-fns** - Date utilities
- **Lucide React** - Icons

## Troubleshooting

### API Connection Issues
- Ensure the ReBM API is running on the correct port
- Check the `REACT_APP_API_URL` environment variable
- Verify CORS settings on the API

### Build Issues
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version compatibility

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the ReBM system. 