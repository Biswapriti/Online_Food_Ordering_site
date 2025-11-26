"""
Upload static images to Cloudinary and write a mapping file `static/cloudinary_map.json`.

Usage:
  - Set your Cloudinary credentials via the environment variable `CLOUDINARY_URL`
    (format: cloudinary://API_KEY:API_SECRET@CLOUD_NAME) or set them manually in the script.
  - Run: `python scripts/upload_images_to_cloudinary.py`

The script uploads image files from the `static/` folder and writes a JSON mapping of
local filename -> secure_url to `static/cloudinary_map.json` which the Flask app will
use automatically to serve cloud-hosted images when available.
"""
import os
import json
import sys
from dotenv import load_dotenv

try:
    import cloudinary
    import cloudinary.uploader
except Exception:
    print('Missing cloudinary package. Install with `pip install cloudinary`')
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(__file__))
STATIC_DIR = os.path.join(ROOT, 'static')
MAP_PATH = os.path.join(STATIC_DIR, 'cloudinary_map.json')

# Load .env from project root so credentials in .env are available
load_dotenv(os.path.join(ROOT, '.env'))

# Configure Cloudinary using environment variables for security.
# Preferred: set the `CLOUDINARY_URL` env var (format: cloudinary://API_KEY:API_SECRET@CLOUD_NAME)
# Alternatively set `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET`.
if os.environ.get('CLOUDINARY_URL'):
    cloudinary.config(cloudinary_url=os.environ.get('CLOUDINARY_URL'))
else:
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
    api_key = os.environ.get('CLOUDINARY_API_KEY')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
    if cloud_name and api_key and api_secret:
        cloudinary.config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)
    else:
        print('Cloudinary credentials not found in environment. Set CLOUDINARY_URL or CLOUDINARY_CLOUD_NAME/CLOUDINARY_API_KEY/CLOUDINARY_API_SECRET')
        sys.exit(1)

print('Using static dir:', STATIC_DIR)

# Collect image files in static dir
files = [f for f in os.listdir(STATIC_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
if not files:
    print('No image files found in static/. Place images there first.')

mapping = {}
for fname in files:
    local_path = os.path.join(STATIC_DIR, fname)
    print('Uploading', fname)
    try:
        res = cloudinary.uploader.upload(local_path, public_id=os.path.splitext(fname)[0], folder='momo_images', overwrite=True)
        url = res.get('secure_url') or res.get('url')
        if url:
            mapping[fname] = url
            print(' ->', url)
        else:
            print('Upload succeeded but no url returned for', fname)
    except Exception as e:
        print('Failed to upload', fname, '->', e)

# Save mapping
with open(MAP_PATH, 'w', encoding='utf-8') as fh:
    json.dump(mapping, fh, indent=2)

print('Mapping written to', MAP_PATH)
print('Done')
