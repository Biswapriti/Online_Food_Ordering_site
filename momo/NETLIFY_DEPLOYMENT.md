# Netlify Deployment Guide for Momo Project

## Prerequisites
- GitHub account with this repository pushed
- Netlify account (free tier available)
- Environment variables configured in Netlify

## Step 1: Push Your Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/momo.git
git push -u origin main
```

## Step 2: Connect to Netlify

1. Go to [netlify.com](https://netlify.com)
2. Click "New site from Git"
3. Choose GitHub and authorize
4. Select your repository
5. Leave build settings as default (they read from `netlify.toml`)
6. Click "Deploy site"

## Step 3: Configure Environment Variables

In Netlify Dashboard:
1. Go to your site settings
2. Navigate to "Build & deploy" → "Environment"
3. Add the following environment variables:

```
CLOUDINARY_CLOUD_NAME: your_cloudinary_cloud_name
CLOUDINARY_API_KEY: your_cloudinary_api_key
CLOUDINARY_API_SECRET: your_cloudinary_api_secret
FLASK_ENV: production
SECRET_KEY: your_secret_key_here
DB_HOST: your_database_host
DB_USER: your_database_user
DB_PASSWORD: your_database_password
DB_NAME: your_database_name
```

## Step 4: Database Setup

**Note:** Netlify Functions have limitations with persistent database connections.

### Option A: Use a Cloud Database (Recommended)
- AWS RDS
- Firebase
- PlanetScale (MySQL compatible)
- MongoDB Atlas

Update your `app.py` to use environment variables for database connection:

```python
conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    port=int(os.getenv('DB_PORT', 3306))
)
```

### Option B: Use a Dedicated Backend Server
- Deploy Flask app to Heroku, Railway, or Render
- Update frontend API calls to point to your backend URL

## Project Structure for Netlify

```
momo/
├── netlify.toml          (Build configuration)
├── Procfile              (Runtime specification)
├── runtime.txt           (Python version)
├── requirements.txt      (Python dependencies)
├── .env.example          (Environment template)
├── app.py                (Flask application)
├── static/               (CSS, JS, images)
├── templates/            (HTML templates)
└── .netlify/
    └── functions/
        └── api.py        (Netlify Function handler)
```

## Configuration Files Included

### netlify.toml
- Specifies build command
- Configures redirects for Flask routing
- Sets up environment contexts

### requirements.txt
- Flask and extensions
- Database driver
- Cloudinary SDK
- Gunicorn (production WSGI server)
- All dependencies pinned to specific versions

### Procfile
- Specifies how to run your app with Gunicorn

### .env.example
- Template for environment variables
- Copy to `.env` and fill in real values

## Important Notes

1. **Limitations**: Netlify Functions have 10-second timeout for free tier
2. **Database**: Ensure your database is accessible from the internet
3. **CORS**: May need to enable CORS for frontend-backend communication
4. **Environment Variables**: Never commit `.env` file with real secrets

## Troubleshooting

### "ModuleNotFoundError"
- Check `requirements.txt` includes all imports from `app.py`
- Verify Python version in `runtime.txt`

### Database connection errors
- Test connection strings locally
- Ensure database firewall allows Netlify IP ranges
- Check environment variables are set correctly

### 502 Bad Gateway
- Check Function logs in Netlify dashboard
- Verify database is accessible
- Check for timeout issues

## Additional Resources

- [Netlify Flask Template](https://github.com/netlify-templates/flask-functions)
- [Netlify Environment Variables](https://docs.netlify.com/configure-builds/environment-variables/)
- [Netlify Functions Documentation](https://docs.netlify.com/functions/overview/)
