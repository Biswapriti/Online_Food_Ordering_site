#!/bin/bash
# Quick deployment setup script for Netlify

echo "🚀 Momo Project - Netlify Deployment Setup"
echo "=========================================="
echo ""

# Check if Git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository already initialized"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  .env file not found"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env created - Please edit it with your actual values"
    echo ""
    echo "Edit the following in .env:"
    echo "  - SECRET_KEY"
    echo "  - DB_HOST, DB_USER, DB_PASSWORD, DB_NAME"
    echo "  - CLOUDINARY credentials"
else
    echo "✅ .env file already exists"
fi

# Check requirements are installed
echo ""
echo "📦 Installing Python requirements..."
pip install -r requirements.txt
echo "✅ Requirements installed"

# Run local tests
echo ""
echo "🧪 Running local tests..."
python -m py_compile app.py
if [ $? -eq 0 ]; then
    echo "✅ Python syntax is valid"
else
    echo "❌ Python syntax errors found"
    exit 1
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your database and Cloudinary credentials"
echo "2. Test locally: python app.py"
echo "3. Commit changes: git add . && git commit -m 'Setup for Netlify'"
echo "4. Push to GitHub: git push -u origin main"
echo "5. Deploy on Netlify.com"
echo ""
echo "📚 Read NETLIFY_DEPLOYMENT.md for detailed instructions"
