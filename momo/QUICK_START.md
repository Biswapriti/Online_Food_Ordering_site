# 🎯 QUICK START GUIDE - Netlify Deployment

## 3 Simple Steps to Deploy

```
┌─────────────────────┐
│  1. PREPARE LOCAL   │  → Update .env, test locally
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  2. PUSH TO GITHUB  │  → git push origin main
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  3. CONNECT NETLIFY │  → Select repo, deploy!
└─────────────────────┘
           ↓
        🚀 LIVE!
```

---

## ⏱️ 5-Minute Setup

### Step 1: Prepare Environment (2 min)
```bash
# Copy environment template
copy .env.example .env

# Edit .env with your credentials
# - Database info
# - Cloudinary API keys
# - Secret key
```

### Step 2: Test Locally (2 min)
```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask
python app.py

# Open browser to http://localhost:5000
```

### Step 3: Push to GitHub (1 min)
```bash
# Initialize Git
git init
git add .
git commit -m "Production ready"
git push -u origin main
```

---

## 🔗 Then Deploy

1. Go to **https://netlify.com**
2. Click **"New site from Git"**
3. Select **GitHub** → Your **momo** repo
4. Click **"Deploy site"**
5. Add **Environment Variables** from Netlify dashboard

Done! ✨

---

## 📋 Files You Need to Know

### Critical Files
| File | Purpose | Edit? |
|------|---------|-------|
| `.env` | Your secrets | YES ✏️ |
| `requirements.txt` | Dependencies | NO (done) |
| `netlify.toml` | Netlify config | NO (done) |
| `app.py` | Flask app | NO (done) |

### Documentation
| File | Read When |
|------|-----------|
| `README.md` | First time |
| `NETLIFY_DEPLOYMENT.md` | Detailed help needed |
| `DEPLOYMENT_CHECKLIST.md` | Step-by-step guide |
| `ALTERNATIVE_DEPLOYMENTS.md` | Want other options |

---

## 🔐 Environment Variables Template

Create `.env` file:

```env
# Must be set (or deployment fails)
SECRET_KEY=generate_a_random_string
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name

# For image hosting
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

**⚠️ NEVER commit `.env` - it's in `.gitignore`**

---

## 🗄️ Database Quick Setup

### Choose One (Free):

#### PlanetScale (Easiest)
```
1. Go to planetscale.com
2. Create free account
3. Create database
4. Copy connection string
5. Set in .env:
   DB_HOST=xxx.psdb.cloud
   DB_USER=xxx
   DB_PASSWORD=xxx
   DB_NAME=xxx
```

#### Railway.app
```
1. Go to railway.app
2. Create new project
3. Add MySQL service
4. Copy credentials
5. Set in .env
```

---

## 🚀 Deployment Checklist (Copy This)

```
□ Update .env with all credentials
□ Test locally: python app.py
□ Verify database connection
□ Run: git add . && git commit -m "Deploy"
□ Run: git push origin main
□ Go to netlify.com
□ Click "New site from Git"
□ Select momo repository
□ Add environment variables in Netlify dashboard
□ Click "Deploy"
□ Test live site
```

---

## 🧪 Testing After Deployment

```bash
# Test homepage
curl https://your-site.netlify.app/

# Test login page
curl https://your-site.netlify.app/login

# Test if styles load
# Open in browser and check for CSS

# Test database
# Register a new user
# Try logging in
# Place a test order
```

---

## ⚠️ Common Issues & Quick Fixes

### "502 Bad Gateway"
```
→ Check environment variables in Netlify dashboard
→ Verify database is accessible
→ Check build logs for errors
```

### "Database connection refused"
```
→ Verify DB_HOST, DB_USER, DB_PASSWORD
→ Ensure database allows remote connections
→ For cloud DB, whitelist Netlify IP ranges
```

### "ModuleNotFoundError"
```
→ Already fixed! requirements.txt has all modules
→ If still issues, let me know which module
```

### Static files not loading
```
→ Verify static/ folder is committed to Git
→ Netlify reads netlify.toml automatically
```

---

## 📚 Next: Full Documentation

For detailed steps, read:
- **`NETLIFY_DEPLOYMENT.md`** - Complete guide
- **`DEPLOYMENT_CHECKLIST.md`** - Step-by-step
- **`README.md`** - Project overview

---

## 🎯 Expected Timeline

| Step | Time | What Happens |
|------|------|-------------|
| Setup .env | 5 min | Configure credentials |
| Test Local | 5 min | Run on localhost |
| Push Git | 2 min | Upload to GitHub |
| Deploy Netlify | 1 min | Click and go |
| Build & Deploy | 2-5 min | Netlify builds your site |
| **Total** | **15-20 min** | **Live Site Ready!** |

---

## 💡 Pro Tips

1. **Set strong SECRET_KEY**: Use random string from openssl/UUID generator
2. **Use cloud database**: Never trust Netlify with local DB
3. **Monitor logs**: Check Netlify dashboard after deployment
4. **Test everything**: Register, login, order before declaring success
5. **Backup database**: Regularly backup your cloud database

---

## 🎉 You're Ready!

Everything is configured. You just need to:

1. Edit `.env`
2. Run `python app.py` to test
3. `git push` to GitHub
4. Deploy on Netlify

**That's it! 🚀**

Need help? See `NETLIFY_DEPLOYMENT.md` for detailed instructions.

---

**Status: ✅ Ready to Deploy**
