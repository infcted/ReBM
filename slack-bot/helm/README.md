# ReBM Slack Bot Helm Chart

This Helm chart deploys the ReBM Slack Bot, a Slack integration for node management.

## Prerequisites

- EKS cluster
- Helm 3.x
- ReBM API server deployed and accessible
- Slack app configured with bot token, signing secret, and app token

## Installation

```bash
# Install the chart
helm install rebm-slack-bot ./helm

# Install with custom values
helm install rebm-slack-bot ./helm -f values.yaml
```

## Configuration

The following table lists the configurable parameters of the rebm-slack-bot chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of Slack bot replicas | `1` |
| `image.repository` | Container image repository | `rebm-slack-bot` |
| `image.tag` | Container image tag | `latest` |
| `image.pullPolicy` | Container image pull policy | `IfNotPresent` |
| `service.type` | Kubernetes service type | `ClusterIP` |
| `service.port` | Kubernetes service port | `3000` |
| `config.apiUrl` | URL of the ReBM API server | `http://rebm-api:8000` |
| `config.apiTimeout` | API request timeout in seconds | `30` |
| `config.botName` | Name of the Slack bot | `ReBM Bot` |
| `config.eventChannel` | Slack channel ID for events | `CXXXXXXXX` |
| `slack.botToken` | Slack bot token | `""` |
| `slack.signingSecret` | Slack signing secret | `""` |
| `slack.appToken` | Slack app token | `""` |

## Slack Configuration

The Slack bot requires several Slack app credentials. Configure them in your values file:

```yaml
slack:
  botToken: "xoxb-your-bot-token"
  signingSecret: "your-signing-secret"
  appToken: "xapp-your-app-token"

config:
  eventChannel: "CXXXXXXXX"  # Channel ID for event notifications
```

### Using Kubernetes Secrets (Recommended)

For production deployments, store Slack credentials in Kubernetes secrets:

```yaml
env:
  - name: SLACK_BOT_TOKEN
    valueFrom:
      secretKeyRef:
        name: slack-credentials
        key: bot-token
  - name: SLACK_SIGNING_SECRET
    valueFrom:
      secretKeyRef:
        name: slack-credentials
        key: signing-secret
  - name: SLACK_APP_TOKEN
    valueFrom:
      secretKeyRef:
        name: slack-credentials
        key: app-token
```

## API Configuration

The Slack bot needs to connect to the ReBM API server:

```yaml
config:
  apiUrl: "http://rebm-api:8000"  # Internal cluster URL
  apiTimeout: "30"  # Request timeout in seconds
```

## Ingress Configuration

To expose the Slack bot externally (for Slack events), enable and configure ingress:

```yaml
ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: slack-bot.rebm.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: slack-bot-tls
      hosts:
        - slack-bot.rebm.example.com
```

## Scaling

Enable horizontal pod autoscaling:

```yaml
autoscaling:
  enabled: true
  minReplicas: 1
  maxReplicas: 5
  targetCPUUtilizationPercentage: 80
```

## Health Checks

The Slack bot includes health check endpoints:

- **Liveness Probe**: `GET /health`
- **Readiness Probe**: `GET /health`

## Uninstallation

```bash
helm uninstall rebm-slack-bot
```

## Troubleshooting

1. **Check pod logs**:
   ```bash
   kubectl logs -l app.kubernetes.io/name=rebm-slack-bot
   ```

2. **Check service status**:
   ```bash
   kubectl get svc rebm-slack-bot
   ```

3. **Verify API connectivity**:
   ```bash
   kubectl exec -it deployment/rebm-slack-bot -- curl -I http://rebm-api:8000/health
   ```

4. **Check Slack configuration**:
   ```bash
   kubectl exec -it deployment/rebm-slack-bot -- env | grep SLACK
   ```

5. **Test Slack bot functionality**:
   ```bash
   # Check if bot is responding to Slack events
   kubectl logs -f deployment/rebm-slack-bot
   ``` 