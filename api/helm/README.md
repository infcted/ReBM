# ReBM API Helm Chart

This Helm chart deploys the ReBM API Server, a FastAPI backend with DynamoDB storage for managing node reservations.

## Prerequisites

- EKS cluster
- Helm 3.x
- AWS credentials configured (for DynamoDB access)
- DynamoDB table created

## Installation

```bash
# Install the chart
helm install rebm-api ./helm

# Install with custom values
helm install rebm-api ./helm -f values.yaml
```

## Configuration

The following table lists the configurable parameters of the rebm-api chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of API server replicas | `1` |
| `image.repository` | Container image repository | `rebm-api` |
| `image.tag` | Container image tag | `latest` |
| `image.pullPolicy` | Container image pull policy | `IfNotPresent` |
| `service.type` | Kubernetes service type | `ClusterIP` |
| `service.port` | Kubernetes service port | `8000` |
| `config.nodeStoreBackend` | Storage backend type | `dynamodb` |
| `config.nodeStoreTableName` | DynamoDB table name | `ReBM-dev` |
| `aws.region` | AWS region for DynamoDB | `us-west-2` |

## AWS Configuration (EKS)

For EKS deployments, the API server uses the default service account and inherits AWS credentials from the node's IAM role. Ensure your EKS nodes have the appropriate IAM permissions for DynamoDB access.

### Required IAM Permissions

Your EKS node role should include the following DynamoDB permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      "Resource": "arn:aws:dynamodb:*:*:table/ReBM-*"
    }
  ]
}
```

## Health Checks

The API server includes health check endpoints:

- **Liveness Probe**: `GET /health`
- **Readiness Probe**: `GET /health`

## Scaling

Enable horizontal pod autoscaling:

```yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

## Uninstallation

```bash
helm uninstall rebm-api
```

## Troubleshooting

1. **Check pod logs**:
   ```bash
   kubectl logs -l app.kubernetes.io/name=rebm-api
   ```

2. **Check service status**:
   ```bash
   kubectl get svc rebm-api
   ```

3. **Verify DynamoDB connectivity**:
   ```bash
   kubectl exec -it deployment/rebm-api -- curl localhost:8000/health
   ```

4. **Check AWS credentials**:
   ```bash
   kubectl exec -it deployment/rebm-api -- env | grep AWS
   ``` 