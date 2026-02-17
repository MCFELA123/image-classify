# Fruit Classification System - Render Deployment Guide

## 🚀 Quick Deploy to Render

### Option 1: Deploy from Dashboard (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Create MongoDB on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "MongoDB"
   - Name: `fruit-classifier-db`
   - Plan: Free (or Starter for production)
   - Click "Create Database"
   - **Copy the Internal Connection String** (e.g., `mongodb://...`)

3. **Deploy Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `fruit-classifier`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn backend.app:app`
     - **Instance Type**: Free (or Starter)

4. **Add Environment Variables**
   Click "Environment" tab and add:
   - `OPENAI_API_KEY` = `sk-your-openai-api-key`
   - `MONGODB_URI` = `your-mongodb-connection-string-from-step-2`
   - `PORT` = `10000` (auto-set by Render)

5. **Deploy!**
   - Click "Create Web Service"
   - Render will build and deploy automatically
   - Your app will be live at: `https://fruit-classifier.onrender.com`

### Option 2: Deploy with render.yaml (Infrastructure as Code)

If you have `render.yaml` in your repo:
1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect your GitHub repo
4. Render will auto-detect `render.yaml` and deploy everything

### 🔧 Environment Variables Required

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-proj-...` |
| `MONGODB_URI` | MongoDB connection string | `mongodb://...` |
| `PORT` | Port (auto-set by Render) | `10000` |

### 📝 Important Notes

1. **Free Tier Limitations**:
   - Service spins down after 15 minutes of inactivity
   - First request after spin-down takes ~30 seconds
   - 750 hours/month free

2. **MongoDB Atlas Alternative** (if not using Render MongoDB):
   - Create free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Get connection string
   - Add to `MONGODB_URI` environment variable

3. **File Uploads**:
   - Render uses ephemeral storage
   - Uploaded files persist during the instance lifetime
   - Consider using S3/Cloudinary for persistent storage in production

### 🔍 Verify Deployment

Once deployed, test these endpoints:
- Health Check: `https://your-app.onrender.com/api/health`
- Main Page: `https://your-app.onrender.com/`
- API Status: `https://your-app.onrender.com/api/status`

### 🐛 Troubleshooting

**Build fails?**
- Check `requirements.txt` has all dependencies
- Ensure Python version compatibility

**App doesn't start?**
- Verify `OPENAI_API_KEY` is set correctly
- Check logs in Render Dashboard
- Ensure MongoDB connection string is correct

**Slow first load?**
- Normal on free tier (spin-up time)
- Upgrade to paid tier for always-on service

### 💰 Cost Estimate

- **Free Tier**: $0/month
  - Web Service: Free
  - MongoDB on Render: Free (256 MB)
  
- **Production Tier**: ~$12/month
  - Web Service Starter: $7/month
  - MongoDB Starter: $5/month

### 🔗 Useful Links

- [Render Dashboard](https://dashboard.render.com/)
- [Render Docs - Flask](https://render.com/docs/deploy-flask)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
