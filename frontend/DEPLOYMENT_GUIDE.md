# Deployment Guide - FineZ

Complete guide for deploying Next.js 14 to production.

## Option 1: Vercel (Recommended) ⭐

**Cost**: Free tier → Paid as you grow
**Setup Time**: 2 minutes
**Best for**: Automatically optimal Next.js hosting

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/finez.git
git push -u origin main
```

### Step 2: Deploy on Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "Import Git Repository"
3. Select your repository
4. Add environment variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `NEXT_PUBLIC_APP_URL=https://finezapp.com`
5. Click "Deploy"

### Step 3: Connect Domain
1. In Vercel dashboard → Settings → Domains
2. Add your domain (e.g., finezapp.com)
3. Update DNS records at your registrar

### Features with Vercel
- ✅ Automatic HTTPS
- ✅ Global CDN (edge caching)
- ✅ Serverless functions for API routes
- ✅ Automatic deployments on git push
- ✅ Preview deployments for PRs
- ✅ Analytics included

## Option 2: Docker + Self-Hosted

**Cost**: $5-50/month (VPS)
**Setup Time**: 15 minutes
**Best for**: Full control, custom domains, VPS

### Step 1: Create VPS
- DigitalOcean App Platform
- AWS EC2
- Linode
- Hetzner

### Step 2: Install Docker
```bash
curl -fsSL get.docker.com | sh
sudo usermod -aG docker $USER
```

### Step 3: Build and Deploy
```bash
# Clone repository
git clone https://github.com/yourusername/finez.git
cd finez/frontend

# Set environment variables
cp .env.example .env.local
nano .env.local  # Edit with your Supabase keys

# Build Docker image
docker build -t finez:latest .

# Run container
docker run -d \
  -p 3000:80 \
  -e NEXT_PUBLIC_SUPABASE_URL=$NEXT_PUBLIC_SUPABASE_URL \
  -e NEXT_PUBLIC_SUPABASE_ANON_KEY=$NEXT_PUBLIC_SUPABASE_ANON_KEY \
  -e SUPABASE_SERVICE_ROLE_KEY=$SUPABASE_SERVICE_ROLE_KEY \
  --restart always \
  --name finez \
  finez:latest
```

### Step 4: Setup Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name finezapp.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name finezapp.com;

    ssl_certificate /etc/letsencrypt/live/finezapp.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/finezapp.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Cache static assets
    location /_next/static {
        proxy_cache_valid 200 30d;
        proxy_pass http://localhost:3000;
    }

    # Cache product data
    location /api/products {
        proxy_cache_valid 200 1h;
        proxy_pass http://localhost:3000;
    }
}
```

### Step 5: Enable SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d finezapp.com
```

## Option 3: AWS (ECS/Fargate)

**Cost**: $10-100+/month
**Setup Time**: 30 minutes
**Best for**: Enterprise, scaling, complex infrastructure

### Step 1: Create ECR Repository
```bash
aws ecr create-repository --repository-name finez --region us-east-1
```

### Step 2: Push Docker Image
```bash
# Build and tag
docker build -t finez:latest .
docker tag finez:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/finez:latest

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/finez:latest
```

### Step 3: Create ECS Cluster and Task Definition
Use AWS Console or:
```bash
aws ecs create-cluster --cluster-name finez
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

### Step 4: Create Service
```bash
aws ecs create-service \
  --cluster finez \
  --service-name finez-service \
  --task-definition finez:1 \
  --desired-count 2 \
  --launch-type FARGATE
```

## Option 4: Heroku (Less Recommended) ⚠️

Heroku has reduced free tier. Still good for testing:

```bash
heroku create finez-app
git push heroku main
heroku config:set NEXT_PUBLIC_SUPABASE_URL=...
heroku config:set NEXT_PUBLIC_SUPABASE_ANON_KEY=...
heroku config:set SUPABASE_SERVICE_ROLE_KEY=...
```

## Monitoring & Logging

### Enable Analytics
```bash
# In Vercel dashboard or add to .env.local
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

### Monitor Errors
```bash
# Sentry integration
npm install @sentry/nextjs
# Configure in next.config.js
```

### Check Logs
```bash
# Vercel
vercel logs

# Docker
docker logs finez

# AWS
aws logs tail /ecs/finez --follow
```

## Database Backups

### Supabase Automatic Backups
- Free plan: 1-day backups
- Pro plan: 7-day backups
- Business plan: 30-day backups

### Manual Backup
```bash
# Export from Supabase SQL editor
SELECT * INTO OUTFILE 'backup.sql' FROM products;
```

### Enable Point-in-Time Recovery
In Supabase dashboard → Settings → Backups

## CDN & Caching

### Vercel (Automatic)
- Caches all static assets worldwide
- 1-day stale-while-revalidate

### Cloudflare (Custom)
1. Add domain to Cloudflare
2. Update nameservers
3. Enable caching rules:
   - Product pages: 1 hour
   - API: 5 minutes

## Performance Checklist

- [ ] Core Web Vitals < 2.5s LCP
- [ ] Page load < 3s on 4G
- [ ] Images optimized with Next.js Image
- [ ] Static assets gzipped
- [ ] Minified JavaScript/CSS
- [ ] Service worker caching
- [ ] Database query optimization

## Security Checklist

- [ ] HTTPS enabled (SSL/TLS)
- [ ] Security headers configured
- [ ] CORS properly set
- [ ] Rate limiting enabled
- [ ] SQL injection protected (Supabase parameterized)
- [ ] XSS protection enabled
- [ ] Environment variables not committed
- [ ] Database backups enabled

## Rollback Procedure

### Vercel
1. Go to deployment history
2. Click "Redeploy" on previous version

### Docker
```bash
docker tag finez:stable finez:latest
docker run -d ... finez:latest
```

### GitHub
```bash
git revert <commit-hash>
git push
```

## Cost Estimation

| Platform | Base | Overages | CDN | Total Estimate |
|----------|------|----------|-----|-----------------|
| Vercel | $0 | $0.50/GB | Included | $0-50+ |
| Docker (DigitalOcean) | $5 | - | Cloudflare Free | $5-15 |
| AWS ECS | $10-20 | $0.032/hour | $0.085/GB | $20-100+ |
| Heroku | Discontinued | - | - | - |

**Recommendation for Launch**: **Vercel** (free tier, then $20/month for team features)

## Troubleshooting

### App Not Loading
- Check environment variables in deployment platform
- Verify Supabase connection string
- Check logs for error messages

### Slow Performance
- Enable caching headers
- Optimize images
- Check database query times

### Database Connection Issues
- Verify `NEXT_PUBLIC_SUPABASE_URL` is correct
- Check `NEXT_PUBLIC_SUPABASE_ANON_KEY` permissions
- Ensure RLS policies allow necessary queries

### PWA Not Installing
- Verify manifest.json is served
- Check HTTPS is enabled
- Wait 24 hours for app stores to update

---

**Next**: Deploy to production within 1 hour!
