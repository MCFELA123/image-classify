# Cloud Deployment Guide

## Overview

This guide covers deploying the Fruit Classification System to various cloud platforms for production use. The system is designed for scalability, security, and multi-user access.

## Deployment Options

### 1. Docker Deployment (Recommended)

#### Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:create_app()"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MONGODB_URI=${MONGODB_URI}
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./data:/app/data
      - ./trained_models:/app/trained_models
    depends_on:
      - mongodb
    restart: unless-stopped

  mongodb:
    image: mongo:6.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - app
    restart: unless-stopped

volumes:
  mongodb_data:
```

---

### 2. AWS Deployment

#### Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS Cloud                                 │
│                                                                  │
│  ┌──────────┐     ┌─────────────┐     ┌──────────────────────┐  │
│  │ Route 53 │────▶│ CloudFront  │────▶│ Application Load     │  │
│  │   DNS    │     │    CDN      │     │     Balancer         │  │
│  └──────────┘     └─────────────┘     └──────────┬───────────┘  │
│                                                   │              │
│                     ┌─────────────────────────────┼─────────┐    │
│                     │         ECS Cluster         │         │    │
│                     │  ┌─────────┐  ┌─────────┐  │         │    │
│                     │  │Container│  │Container│  │         │    │
│                     │  │  Task   │  │  Task   │  │         │    │
│                     │  └────┬────┘  └────┬────┘  │         │    │
│                     └───────┼────────────┼───────┘         │    │
│                             │            │                  │    │
│  ┌──────────────────────────┴────────────┴──────────────┐  │    │
│  │                    DocumentDB / MongoDB Atlas         │  │    │
│  └───────────────────────────────────────────────────────┘  │    │
│                                                              │    │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────────┐ │    │
│  │    S3      │  │ CloudWatch │  │     Secrets Manager    │ │    │
│  │  Storage   │  │   Logs     │  │      (API Keys)        │ │    │
│  └────────────┘  └────────────┘  └────────────────────────┘ │    │
└─────────────────────────────────────────────────────────────────┘
```

#### AWS ECS Task Definition
```json
{
  "family": "fruit-classifier",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "fruit-classifier",
      "image": "your-registry/fruit-classifier:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "FLASK_ENV", "value": "production"}
      ],
      "secrets": [
        {
          "name": "OPENAI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:fruit-classifier/openai"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/fruit-classifier",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

---

### 3. Google Cloud Platform (GCP)

#### Cloud Run Deployment
```bash
# Build and push container
gcloud builds submit --tag gcr.io/PROJECT_ID/fruit-classifier

# Deploy to Cloud Run
gcloud run deploy fruit-classifier \
  --image gcr.io/PROJECT_ID/fruit-classifier \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLASK_ENV=production \
  --set-secrets OPENAI_API_KEY=openai-key:latest \
  --memory 2Gi \
  --cpu 2 \
  --concurrency 80 \
  --max-instances 10
```

#### GCP Architecture
```
                    ┌─────────────────┐
                    │  Cloud DNS      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Cloud Load     │
                    │  Balancer       │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼────┐  ┌──────▼──────┐ ┌─────▼─────┐
     │  Cloud Run  │  │  Cloud Run  │ │ Cloud Run │
     │  Instance   │  │  Instance   │ │ Instance  │
     └──────┬──────┘  └──────┬──────┘ └─────┬─────┘
            │                │              │
            └────────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │   Firestore /   │
                    │   Cloud SQL     │
                    └─────────────────┘
```

---

### 4. Azure Deployment

#### Azure Container Apps
```bash
# Create Container App
az containerapp create \
  --name fruit-classifier \
  --resource-group fruit-classifier-rg \
  --environment fruit-classifier-env \
  --image your-registry.azurecr.io/fruit-classifier:latest \
  --target-port 5000 \
  --ingress external \
  --cpu 1.0 \
  --memory 2Gi \
  --min-replicas 1 \
  --max-replicas 10 \
  --secrets openai-key=<OPENAI_API_KEY> \
  --env-vars OPENAI_API_KEY=secretref:openai-key FLASK_ENV=production
```

---

### 5. Firebase Deployment

#### Firebase Configuration (firebase.json)
```json
{
  "hosting": {
    "public": "frontend",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      {
        "source": "/api/**",
        "function": "api"
      },
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  },
  "functions": {
    "source": "functions",
    "runtime": "python310"
  },
  "firestore": {
    "rules": "firestore.rules",
    "indexes": "firestore.indexes.json"
  }
}
```

---

## Environment Variables

Required environment variables for production:

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 Vision | Yes |
| `MONGODB_URI` | MongoDB connection string | Yes |
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `FLASK_ENV` | Environment (production/development) | Yes |
| `ALLOWED_ORIGINS` | CORS allowed origins | Recommended |
| `MAX_UPLOAD_SIZE` | Max upload size in bytes | Optional |
| `RATE_LIMIT` | API rate limit per minute | Optional |

---

## Scaling Considerations

### Horizontal Scaling
- Use container orchestration (Kubernetes, ECS, Cloud Run)
- Configure auto-scaling based on CPU/memory/request count
- Implement load balancing

### Database Scaling
- Use MongoDB Atlas or managed database services
- Configure read replicas for read-heavy workloads
- Implement connection pooling

### CDN Setup
- Serve static files through CDN (CloudFront, Cloud CDN)
- Cache API responses where appropriate
- Configure proper cache headers

---

## Security Checklist

- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Use secrets manager for API keys
- [ ] Enable rate limiting
- [ ] Configure WAF (Web Application Firewall)
- [ ] Enable logging and monitoring
- [ ] Set up alerts for anomalies
- [ ] Regular security audits
- [ ] Implement proper authentication
- [ ] Configure backup and recovery

---

## Monitoring & Logging

### Recommended Tools
- **AWS**: CloudWatch, X-Ray
- **GCP**: Cloud Monitoring, Cloud Logging
- **Azure**: Application Insights, Azure Monitor
- **Self-hosted**: Prometheus, Grafana, ELK Stack

### Key Metrics to Monitor
- Request latency (p50, p95, p99)
- Error rate
- CPU and memory utilization
- Classification accuracy (if tracking)
- API rate limit hits
- Database connection pool usage

---

## Cost Optimization

### Tips
1. Use spot/preemptible instances for non-critical workloads
2. Implement request caching where possible
3. Optimize container image size
4. Use appropriate instance sizes
5. Set up budget alerts
6. Review and optimize database queries
7. Use reserved capacity for predictable workloads

---

## Disaster Recovery

### Backup Strategy
- Database: Daily automated backups with 30-day retention
- Models: Version control and cloud storage
- Configuration: Infrastructure as Code (Terraform/CloudFormation)

### Recovery Procedures
1. Database restoration from backup
2. Redeploy containers from registry
3. Validate system health
4. DNS failover if needed

---

## Multi-tenant Architecture

For supporting multiple organizations:

```python
# Example multi-tenant configuration
TENANT_CONFIG = {
    'organization_id': {
        'db_name': 'tenant_db',
        'model_path': 'models/tenant_model.h5',
        'features': ['classification', 'analytics'],
        'api_limits': {'requests_per_minute': 100}
    }
}
```

---

## Support

For deployment assistance or enterprise support:
- Documentation: See project README
- Issues: GitHub Issues
- Email: support@example.com
