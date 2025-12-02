# Deployment Guide - Intraday Swing Analyzer Web App

## Quick Deploy Options

### Option 1: Streamlit Cloud (Easiest - Free)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/intraday-analyzer.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

3. **Your app will be live at**: `https://your-app-name.streamlit.app`

### Option 2: Railway (Free Tier Available)

1. **Install Railway CLI**:
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Deploy**:
   ```bash
   railway init
   railway up
   ```

3. **Set environment variables** (if needed):
   ```bash
   railway variables set PORT=8501
   ```

### Option 3: Render (Free Tier Available)

1. **Create `render.yaml`**:
   ```yaml
   services:
     - type: web
       name: intraday-analyzer
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
       envVars:
         - key: PORT
           value: 8501
   ```

2. **Deploy**:
   - Connect GitHub repository
   - Render will auto-detect and deploy

### Option 4: Heroku

1. **Create `Procfile`** (already created):
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 5: Docker

1. **Create `Dockerfile`**:
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8501

   HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

   ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and run**:
   ```bash
   docker build -t intraday-analyzer .
   docker run -p 8501:8501 intraday-analyzer
   ```

3. **For production**, use docker-compose:
   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "8501:8501"
       volumes:
         - ./output:/app/output
   ```

## Pre-Deployment Checklist

- [ ] All dependencies in `requirements.txt`
- [ ] `app.py` is the main file
- [ ] Output directory exists or will be created
- [ ] Environment variables set (if needed)
- [ ] Port configuration correct
- [ ] CORS settings configured (if needed)

## Post-Deployment

1. **Run initial analysis**:
   - Use the "Analysis" tab in the web app
   - Or run: `python intraday_swing_analyzer.py`

2. **Verify**:
   - Check that CSV files are generated
   - Test all tabs in the web app
   - Verify charts load correctly

## Environment Variables

If you need to set environment variables:

```bash
# Streamlit Cloud
# Add in dashboard under "Settings" > "Secrets"

# Railway
railway variables set VARIABLE_NAME=value

# Render
# Add in dashboard under "Environment"

# Heroku
heroku config:set VARIABLE_NAME=value
```

## Troubleshooting Deployment

### Port Issues

- Ensure `$PORT` is used (for cloud platforms)
- Check that port is exposed in Dockerfile
- Verify firewall settings

### Missing Dependencies

- Check `requirements.txt` is complete
- Verify all imports are available
- Check Python version compatibility

### Data Not Loading

- Ensure `output/` directory exists
- Check file permissions
- Verify CSV files are generated
- Clear cache: `st.cache_data.clear()`

### Performance Issues

- Increase cache TTL
- Reduce number of tickers
- Optimize data loading
- Use background processing

## Custom Domain

### Streamlit Cloud
- Not supported (use subdomain)

### Railway/Render/Heroku
- Add custom domain in dashboard
- Update DNS records
- SSL auto-configured

## Monitoring

### Streamlit Cloud
- Built-in analytics
- View in dashboard

### Other Platforms
- Use platform's monitoring tools
- Add logging: `st.logger.info()`
- Monitor error rates

## Updates

To update your deployed app:

```bash
git add .
git commit -m "Update app"
git push
```

Most platforms auto-deploy on push.

## Cost Estimates

- **Streamlit Cloud**: Free (unlimited apps)
- **Railway**: Free tier (500 hours/month)
- **Render**: Free tier (limited hours)
- **Heroku**: Free tier discontinued (paid plans)
- **Docker (self-hosted)**: VPS costs (~$5-20/month)

## Security Considerations

1. **Don't commit secrets**: Use environment variables
2. **Rate limiting**: Add if needed
3. **Authentication**: Add if sharing sensitive data
4. **HTTPS**: Auto-enabled on most platforms
5. **Input validation**: Validate user inputs

## Support

For deployment issues:
1. Check platform documentation
2. Review error logs
3. Test locally first
4. Check dependencies

---

**Ready to deploy! 🚀**

