# ReBM Web UI Helm Chart

This Helm chart deploys the ReBM Web UI, a React/TypeScript frontend for node management.

## Prerequisites

- EKS cluster
- Helm 3.x
- ReBM API server deployed and accessible

## Installation

```bash
# Install the chart
helm install rebm-web-ui ./helm

# Install with custom values
helm install rebm-web-ui ./helm -f values.yaml
```

## Configuration

The following table lists the configurable parameters of the rebm-web-ui chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of web UI replicas | `1` |
| `image.repository` | Container image repository | `rebm-web-ui` |
| `image.tag` | Container image tag | `latest` |
| `image.pullPolicy` | Container image pull policy | `IfNotPresent` |
| `service.type` | Kubernetes service type | `ClusterIP` |
| `service.port` | Kubernetes service port | `80` |
| `config.apiUrl` | URL of the ReBM API server | `http://rebm-api:8000` |

## API Configuration

The web UI needs to connect to the ReBM API server. Configure the API URL:

```yaml
config:
  apiUrl: "http://rebm-api:8000"  # Internal cluster URL
  # or
  apiUrl: "https://api.rebm.example.com"  # External URL
```

## Ingress Configuration

To expose the web UI externally, enable and configure ingress:

```yaml
ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: rebm.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: rebm-tls
      hosts:
        - rebm.example.com
```

## Scaling

Enable horizontal pod autoscaling:

```yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

## Health Checks

The web UI includes health check endpoints:

- **Liveness Probe**: `GET /`
- **Readiness Probe**: `GET /`

## Uninstallation

```bash
helm uninstall rebm-web-ui
```

## Troubleshooting

1. **Check pod logs**:
   ```bash
   kubectl logs -l app.kubernetes.io/name=rebm-web-ui
   ```

2. **Check service status**:
   ```bash
   kubectl get svc rebm-web-ui
   ```

3. **Verify API connectivity**:
   ```bash
   kubectl exec -it deployment/rebm-web-ui -- curl -I http://rebm-api:8000/health
   ```

4. **Check ingress status**:
   ```bash
   kubectl get ingress rebm-web-ui
   ``` 