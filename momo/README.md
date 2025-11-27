# Momo - Food Ordering Web Application
## Deployment Ready for Netlify & Other Platforms

![Momo Project](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)

---

## 🚀 Quick Start Deployment

### For Netlify:
1. Push code to GitHub
2. Go to [netlify.com](https://netlify.com) → Connect repository
3. Add environment variables from `.env.example`
4. Done! Your site deploys automatically

See **NETLIFY_DEPLOYMENT.md** for detailed instructions.

---

## 📋 Project Overview

A full-stack momo (Asian dumplings) ordering web application built with:
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL
- **Image Hosting:** Cloudinary
- **Deployment:** Netlify, Vercel, Railway, Render

### Features
- User registration & login
- Product catalog with categories
- Shopping cart functionality
- Checkout & order placement
- User profile with order history
- Contact form
- Responsive design

---

## 📁 Project Structure

```
momo/
├── Deployment Configuration
│   ├── netlify.toml              # Netlify build config
│   ├── vercel.json               # Vercel config (alternative)
│   ├── Procfile                  # Production server config
│   ├── runtime.txt               # Python version
│   └── requirements.txt           # Python dependencies
│
├── Application
│   ├── app.py                    # Flask application
│   ├── .env.example              # Environment variables template
│   ├── .env                      # Local secrets (not committed)
│   └── .gitignore                # Git ignore rules
│
├── Frontend
│   ├── script.js                 # Main JS file
│   ├── static/                   # Static files
│   │   ├── style.css             # Main stylesheet
│   │   ├── cart.css              # Cart styling
│   │   ├── login.css             # Login styling
│   │   ├── veg_momo.css          # Veg menu styling
│   │   ├── *.jpg                 # Product images
│   │   ├── cloudinary_map.json   # Image URL mappings
│   │   └── script.js             # Frontend utilities
│   └── templates/                # HTML templates
│       ├── index.html            # Homepage
│       ├── login.html            # Login page
│       ├── register.html         # Registration
│       ├── all_momos.html        # Menu page
│       ├── veg_momo.html         # Veg menu
│       ├── cart.html             # Shopping cart
│       ├── checkout.html         # Checkout page
│       ├── order_success.html    # Order confirmation
│       └── profile.html          # User profile
│
├── Backend Services
│   ├── scripts/
│   │   └── upload_images_to_cloudinary.py
│   ├── .netlify/functions/
│   │   └── api.py                # Netlify Functions handler
│
└── Documentation
    ├── README.md                 # This file
    ├── NETLIFY_DEPLOYMENT.md     # Netlify guide
    ├── DEPLOYMENT_CHECKLIST.md   # Step-by-step checklist
    └── ALTERNATIVE_DEPLOYMENTS.md # Other platforms
```

---

## 🔧 Environment Variables

Create `.env` file with:

```env
# Server
SECRET_KEY=your_random_secret_key_here
FLASK_ENV=production

# Database
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
DB_PORT=3306

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_key
CLOUDINARY_API_SECRET=your_cloudinary_secret
```

**Never commit `.env` file!** It's in `.gitignore`.

---

## 💾 Requirements

All dependencies are in `requirements.txt`:

```
Flask==3.0.0
Flask-Cors==4.0.0
mysql-connector-python==8.2.0
cloudinary==1.36.0
python-dotenv==1.0.0
werkzeug==3.0.0
gunicorn==21.2.0
```

Install locally:
```bash
pip install -r requirements.txt
```

---

## 🏃 Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment
set FLASK_ENV=development  # On Windows
# OR
export FLASK_ENV=development  # On Mac/Linux

# Run Flask app
python app.py

# Open browser to http://localhost:5000
```

---

## 🌐 Deployment Platforms

### ✅ Tested & Recommended

**1. Netlify** (Free tier available)
- Automatic builds from GitHub
- Free SSL/TLS
- See: NETLIFY_DEPLOYMENT.md

**2. Railway.app** (Free with credits)
- Supports Python apps
- MySQL database included
- Simple GitHub integration

**3. Vercel** (Free tier)
- Fast deployments
- GitHub integration
- Use: vercel.json (included)

**4. Render.com** (Free tier)
- Good uptime
- PostgreSQL or MySQL support
- Web services + databases

See **ALTERNATIVE_DEPLOYMENTS.md** for detailed setup.

---

## 🗄️ Database Setup

### Option A: Cloud MySQL (Recommended)

**PlanetScale** (easiest, MySQL compatible):
```
1. Go to planetscale.com
2. Create free account
3. Create new database
4. Get connection string
5. Set DB_* env variables
```

**Railway.app:**
```
1. Create new project
2. Add MySQL service
3. Get credentials
4. Set env variables
```

**AWS RDS:**
```
1. Create MySQL instance
2. Configure security groups
3. Get endpoint & credentials
4. Set env variables
```

### Option B: Local Database
Only for development. For production, use cloud DB.

```bash
# MySQL on your machine
mysql -u root -p

CREATE DATABASE priti;
USE priti;

# Then create tables as needed
```

---

## 📝 Deployment Checklist

- [ ] Push code to GitHub
- [ ] Create Netlify account
- [ ] Connect GitHub repo to Netlify
- [ ] Set up environment variables in Netlify
- [ ] Configure database (choose PlanetScale/Railway/AWS)
- [ ] Set database environment variables
- [ ] Deploy and test
- [ ] Fix any issues using deployment logs
- [ ] Monitor after deployment

See **DEPLOYMENT_CHECKLIST.md** for details.

---

## 🧪 Testing Deployment

After deploying to Netlify:

```bash
# Test homepage
curl https://your-site.netlify.app/

# Test login
curl -X POST https://your-site.netlify.app/login \
  -d "username=test&password=test"

# Test cart
curl https://your-site.netlify.app/cart
```

---

## 🐛 Troubleshooting

### "502 Bad Gateway"
- Check Netlify build logs
- Verify database connection
- Check environment variables
- Look for Python syntax errors

### "ModuleNotFoundError"
- Add missing package to `requirements.txt`
- Redeploy: `git push`

### "Database connection refused"
- Verify database credentials
- Check database is accessible from internet
- Whitelist Netlify IPs in firewall

### Static files not loading
- Verify `static/` folder committed to Git
- Check CSS/JS paths use `url_for()`
- Rebuild: `git push`

See **NETLIFY_DEPLOYMENT.md** for more solutions.

---

## 🔒 Security

**Before Production:**
- [ ] Change `SECRET_KEY` to random string
- [ ] Never commit `.env` file
- [ ] Use strong database password
- [ ] Enable HTTPS (Netlify provides free SSL)
- [ ] Validate all user inputs
- [ ] Test CORS settings
- [ ] Review environment variables

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `NETLIFY_DEPLOYMENT.md` | Complete Netlify setup guide |
| `DEPLOYMENT_CHECKLIST.md` | Step-by-step deployment checklist |
| `ALTERNATIVE_DEPLOYMENTS.md` | Other hosting platforms |
| `requirements.txt` | Python dependencies |
| `netlify.toml` | Netlify configuration |
| `vercel.json` | Vercel configuration |
| `Procfile` | Production server settings |

---

## 🤝 Support Resources

- [Netlify Docs](https://docs.netlify.com)
- [Flask Docs](https://flask.palletsprojects.com)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Cloudinary Docs](https://cloudinary.com/documentation)

---

## 📈 Performance Tips

1. Optimize images with Cloudinary
2. Use browser caching
3. Minimize CSS/JS files
4. Enable gzip compression (Netlify auto)
5. Use CDN for static files
6. Database indexing on frequently queried columns

---

## 🎯 Next Steps

1. **Local Testing** → Run `python app.py` and test
2. **GitHub Setup** → Push code to GitHub
3. **Choose Host** → Decide between Netlify/Railway/Render
4. **Deploy** → Follow platform-specific guide
5. **Configure DB** → Set up cloud database
6. **Monitor** → Check logs and test features

---

## 📞 Need Help?

1. Check deployment logs in your platform's dashboard
2. Review the relevant documentation file
3. Test locally with `python app.py`
4. Verify environment variables are set
5. Check database connectivity

---

**Happy Deploying! 🚀**

Last Updated: November 2025
Version: 1.0 - Production Ready
