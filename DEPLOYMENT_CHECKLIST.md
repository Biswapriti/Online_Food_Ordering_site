# Netlify Deployment Checklist for Momo Project

## ✅ Project Files Prepared

### Configuration Files Created:
- ✅ `netlify.toml` - Build configuration for Netlify
- ✅ `Procfile` - Specifies Gunicorn as production server
- ✅ `runtime.txt` - Python version specification (3.11.7)
- ✅ `.env.example` - Template for environment variables

### Updated Files:
- ✅ `requirements.txt` - All dependencies with pinned versions
- ✅ `app.py` - Updated to use environment variables
- ✅ `.gitignore` - Excludes sensitive files

### Documentation:
- ✅ `NETLIFY_DEPLOYMENT.md` - Comprehensive deployment guide
- ✅ `DEPLOYMENT_CHECKLIST.md` - This checklist

---

## 🚀 Pre-Deployment Setup (Do This First)

### 1. Initialize Git Repository
```bash
cd momo
git init
git add .
git commit -m "Initial commit: Project ready for Netlify deployment"
```

### 2. Create GitHub Repository
- Go to https://github.com/new
- Create a new repository named `momo`
- Add the remote and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/momo.git
git branch -M main
git push -u origin main
```

### 3. Prepare Environment Variables

**Locally**, create a `.env` file (not committed to Git):
```
SECRET_KEY=your_secret_key_here
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
DB_PORT=3306
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
FLASK_ENV=production
```

### 4. Test Locally
```bash
pip install -r requirements.txt
python app.py
```

---

## 🔧 Database Configuration

### Important: Choose Your Database Host

**Option A: Cloud MySQL Database (Recommended)**
- **PlanetScale** (MySQL compatible, free tier)
  - https://planetscale.com
  - Create account → Create database
  - Copy connection string
  - Update DB_* environment variables

- **AWS RDS** (More enterprise)
  - https://aws.amazon.com/rds/
  - Create MySQL instance
  - Get endpoint and credentials
  - Update DB_* environment variables

- **Railway** (Simple hosting)
  - https://railway.app
  - Create MySQL add-on
  - Copy connection variables

**Option B: Firebase/Firestore** (NoSQL alternative)
- More scalable for Netlify Functions
- Requires code changes

---

## 🌐 Netlify Deployment Steps

### Step 1: Connect to Netlify
1. Go to https://netlify.com
2. Sign up or log in
3. Click "New site from Git"
4. Choose GitHub as provider
5. Authorize and select your `momo` repository
6. Click "Deploy site"

### Step 2: Configure Environment Variables in Netlify
1. Go to your Netlify site dashboard
2. Navigate to **Site settings** → **Build & deploy** → **Environment**
3. Add the following variables (copy values from your `.env`):

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | your_secret_key |
| `DB_HOST` | your_database_host |
| `DB_USER` | your_database_user |
| `DB_PASSWORD` | your_database_password |
| `DB_NAME` | your_database_name |
| `DB_PORT` | 3306 |
| `CLOUDINARY_CLOUD_NAME` | your_cloud_name |
| `CLOUDINARY_API_KEY` | your_api_key |
| `CLOUDINARY_API_SECRET` | your_api_secret |
| `FLASK_ENV` | production |

### Step 3: Deploy
1. Push changes to GitHub
2. Netlify automatically builds and deploys
3. Check deployment logs in Netlify dashboard

---

## 📁 Project Structure Overview

```
momo/
├── netlify.toml              ← Netlify build config
├── Procfile                  ← Production server config
├── runtime.txt               ← Python version
├── requirements.txt          ← Python dependencies
├── .env.example              ← Environment template
├── .env                      ← Real secrets (NOT committed)
├── .gitignore                ← Excludes .env and __pycache__
├── app.py                    ← Flask application
├── script.js                 ← Frontend JavaScript
├── amazon-logo.jpg           ← Static assets
├── .netlify/
│   └── functions/
│       └── api.py            ← Netlify Functions handler
├── static/
│   ├── *.css                 ← Stylesheets
│   ├── *.js                  ← Frontend scripts
│   ├── *.jpg                 ← Product images
│   └── cloudinary_map.json   ← Image mappings
└── templates/
    ├── index.html
    ├── login.html
    ├── cart.html
    ├── checkout.html
    └── ...
```

---

## ⚙️ File Descriptions

### netlify.toml
- Specifies build command: `pip install -r requirements.txt`
- Configures redirects for Flask routing
- Sets up environment contexts

### Procfile
```
web: gunicorn app:app
```
Tells Netlify how to run the Flask app with Gunicorn (production WSGI server)

### runtime.txt
```
python-3.11.7
```
Specifies Python version for consistency

### requirements.txt
Pinned versions of all dependencies:
- Flask & extensions
- MySQL connector
- Cloudinary SDK
- Gunicorn server
- Other utilities

---

## ✅ Testing Your Deployment

### 1. Check Build Logs
- In Netlify dashboard → Deploy logs
- Verify: `pip install` succeeded
- Look for errors in build output

### 2. Test Endpoints
- Homepage: `https://your-site.netlify.app/`
- Login: `https://your-site.netlify.app/login`
- Menu: `https://your-site.netlify.app/menu`

### 3. Database Connectivity
- Try logging in
- Add items to cart
- Place an order
- Check if database records are created

---

## 🐛 Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'X'"
**Solution:** Add missing module to `requirements.txt`
```bash
pip install module-name
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### Issue: "502 Bad Gateway"
**Solutions:**
1. Check database connectivity
2. Verify environment variables are set
3. Check for Python syntax errors: `python -m py_compile app.py`
4. View Netlify function logs for more details

### Issue: Database Connection Timeout
**Solutions:**
1. Ensure database is accessible from internet
2. Check database firewall settings
3. Verify credentials in environment variables
4. For cloud databases, whitelist Netlify's IP ranges

### Issue: Static Files Not Loading
**Solutions:**
1. Ensure `static/` folder is committed to Git
2. Check `netlify.toml` publish directory: `publish = "static"`
3. Verify CSS/JS paths in templates use `url_for('static', filename='...')`

### Issue: Session/Cart Data Lost After Reload
**Solutions:**
1. Netlify Functions are stateless
2. Use database to store cart instead of session
3. Or use browser localStorage for client-side cart

---

## 🔒 Security Checklist

- ✅ Never commit `.env` with real secrets
- ✅ Use environment variables in Netlify for all secrets
- ✅ Change `SECRET_KEY` to a random string
- ✅ Use HTTPS only (Netlify provides free SSL)
- ✅ Enable CORS only for your domain
- ✅ Validate all user inputs in Flask
- ✅ Don't expose error details in production

---

## 📚 Useful Resources

- [Netlify Documentation](https://docs.netlify.com)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Netlify Functions Guide](https://docs.netlify.com/functions/overview/)
- [Environment Variables Setup](https://docs.netlify.com/configure-builds/environment-variables/)
- [Netlify Pricing](https://netlify.com/pricing)

---

## 🎯 Next Steps

1. **Choose & Configure Database** → Select PlanetScale, AWS RDS, or Railway
2. **Set Up GitHub** → Push code to GitHub
3. **Connect Netlify** → Link GitHub repository to Netlify
4. **Configure Secrets** → Add environment variables in Netlify dashboard
5. **Test Deployment** → Access your live site and test features
6. **Monitor & Debug** → Check logs and error tracking

---

## 📞 Support

For issues:
1. Check Netlify build logs
2. Check browser console (F12)
3. Check database connection
4. Review error messages carefully
5. Test locally first before deploying

**Happy Deploying! 🚀**
