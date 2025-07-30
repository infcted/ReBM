# ReBM Helm Charts

This directory contains Helm charts for deploying the ReBM (Reserved By Me) system on Kubernetes.

## System Overview

ReBM consists of four main components:

1. **API Server** (`api/helm/`) - FastAPI backend with DynamoDB storage
2. **Web UI** (`web-ui/helm/`) - React/TypeScript frontend
3. **Slack Bot** (`slack-bot/helm/`) - Slack integration for node management
4. **ReBM Linux** (`rebm-linux/`) - Systemd service for node monitoring (installed directly on nodes)

## Prerequisites

- EKS cluster (1.19+)
- Helm 3.x
- AWS credentials configured (for DynamoDB access)
- DynamoDB table created
- Container registry with ReBM images
- Linux nodes with systemd (for ReBM Linux service)
- Slack app configured (for Slack bot)

## Quick Start

### 1. Deploy the API Server

```bash
# Navigate to the API directory
cd api

# Install the API chart
helm install rebm-api ./helm

# Or with custom values
helm install rebm-api ./helm -f values.yaml
```

### 2. Deploy the Web UI

```bash
# Navigate to the Web UI directory
cd web-ui

# Install the Web UI chart
helm install rebm-web-ui ./helm

# Or with custom values
helm install rebm-web-ui ./helm -f values.yaml
```

### 3. Deploy the Slack Bot

```bash
# Navigate to the Slack Bot directory
cd slack-bot

# Install the Slack Bot chart
helm install rebm-slack-bot ./helm

# Or with custom values
helm install rebm-slack-bot ./helm -f values.yaml
```

### 4. Install ReBM Linux on Nodes

The ReBM Linux component is installed directly on each node as a systemd service:

```bash
# Navigate to the ReBM Linux directory
cd rebm-linux

# Install on each node you want to monitor
sudo chmod +x install.sh
sudo ./install.sh
```

## Complete Deployment Example

Create a `values.yaml` file for each component with your specific configuration:

### API Server (`api/helm/values.yaml`)

```yaml
image:
  repository: your-registry/rebm-api
  tag: "v1.0.0"

config:
  nodeStoreTableName: "ReBM-prod"

aws:
  region: "us-west-2"
```

### Web UI (`web-ui/helm/values.yaml`)

```yaml
image:
  repository: your-registry/rebm-web-ui
  tag: "v1.0.0"

config:
  apiUrl: "http://rebm-api:8000"

ingress:
  enabled: true
  hosts:
    - host: rebm.example.com
      paths:
        - path: /
          pathType: Prefix
```

### Slack Bot (`slack-bot/helm/values.yaml`)

```yaml
image:
  repository: your-registry/rebm-slack-bot
  tag: "v1.0.0"

config:
  apiUrl: "http://rebm-api:8000"
  eventChannel: "CXXXXXXXX"

slack:
  botToken: "xoxb-your-bot-token"
  signingSecret: "your-signing-secret"
  appToken: "xapp-your-app-token"

ingress:
  enabled: true
  hosts:
    - host: slack-bot.rebm.example.com
      paths:
        - path: /
          pathType: Prefix
```

### ReBM Linux Configuration

Configure the ReBM Linux service by setting environment variables on each node:

```bash
# Set API URL
export REBM_API_URL="http://your-api-server:8000"

# Set node name (optional, defaults to hostname)
export NODE_NAME="my-node"

# Set check interval (optional, defaults to 300 seconds)
export CHECK_INTERVAL_SECONDS=300
```

## Deployment Order

1. **API Server** (required first)
2. **Web UI** (depends on API)
3. **Slack Bot** (depends on API)
4. **ReBM Linux** (install on each node after API is available)

## Verification

### Check API Server

```bash
# Check API deployment
kubectl get deployment rebm-api

# Test API health
kubectl port-forward svc/rebm-api 8000:8000
curl http://localhost:8000/health
```

### Check Web UI

```bash
# Check Web UI deployment
kubectl get deployment rebm-web-ui

# Access Web UI (if ingress is configured)
kubectl get ingress rebm-web-ui
```

### Check Slack Bot

```bash
# Check Slack Bot deployment
kubectl get deployment rebm-slack-bot

# Check Slack Bot logs
kubectl logs -f deployment/rebm-slack-bot
```

### Check Node Monitoring

```bash
# Check systemd service status on nodes
sudo systemctl status rebm-linux.service

# Check service logs
sudo journalctl -u rebm-linux.service -f

# Check MOTD updates
cat /etc/motd
```

## Scaling

### API Server Scaling

```bash
# Scale API server
kubectl scale deployment rebm-api --replicas=3

# Or enable HPA
helm upgrade rebm-api ./helm --set autoscaling.enabled=true
```

### Web UI Scaling

```bash
# Scale Web UI
kubectl scale deployment rebm-web-ui --replicas=2

# Or enable HPA
helm upgrade rebm-web-ui ./helm --set autoscaling.enabled=true
```

### Slack Bot Scaling

```bash
# Scale Slack Bot
kubectl scale deployment rebm-slack-bot --replicas=2

# Or enable HPA
helm upgrade rebm-slack-bot ./helm --set autoscaling.enabled=true
```

## Monitoring and Logs

### API Server Logs

```bash
kubectl logs -l app.kubernetes.io/name=rebm-api -f
```

### Web UI Logs

```bash
kubectl logs -l app.kubernetes.io/name=rebm-web-ui -f
```

### Slack Bot Logs

```bash
kubectl logs -l app.kubernetes.io/name=rebm-slack-bot -f
```

### Node Monitoring Logs

```bash
# On each node
sudo journalctl -u rebm-linux.service -f
```

## Uninstallation

### Remove Kubernetes Components

```bash
# Remove Helm charts
helm uninstall rebm-slack-bot
helm uninstall rebm-web-ui
helm uninstall rebm-api
```

### Remove Node Monitoring

```bash
# On each node
sudo systemctl stop rebm-linux.service
sudo systemctl disable rebm-linux.service
sudo rm /etc/systemd/system/rebm-linux.service
sudo systemctl daemon-reload
```

## Troubleshooting

### Common Issues

1. **API Connection Issues**: Verify the API server is running and accessible
2. **DynamoDB Access**: Check AWS credentials and IAM permissions
3. **Slack Bot Issues**: Verify Slack credentials and webhook configuration
4. **Node Monitoring**: Ensure ReBM Linux service is installed and running
5. **Image Pull Issues**: Verify container images exist in your registry

### Debug Commands

```bash
# Check all ReBM resources
kubectl get all -l app.kubernetes.io/part-of=rebm

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Check pod status
kubectl describe pod <pod-name>

# Check node monitoring service
sudo systemctl status rebm-linux.service
sudo journalctl -u rebm-linux.service --no-pager
```

## Customization

Each chart can be customized by:

1. **Modifying values.yaml**: Edit the default values
2. **Using --set**: Override specific values during installation
3. **Creating custom values files**: Create environment-specific configurations

## Security Considerations

1. **API Server**: Use IAM roles for AWS access, enable TLS
2. **Web UI**: Configure ingress with TLS, use proper authentication
3. **Slack Bot**: Store Slack credentials in Kubernetes secrets
4. **Node Monitoring**: The systemd service runs with appropriate permissions

## Support

For issues and questions:

1. Check the individual chart READMEs
2. Review Kubernetes events and logs
3. Check systemd service logs on nodes
4. Verify configuration and prerequisites 