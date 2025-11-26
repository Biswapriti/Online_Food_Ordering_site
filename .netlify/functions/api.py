import json
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import Flask app
from app import app

def handler(event, context):
    """AWS Lambda handler for Netlify Functions"""
    
    # Parse the incoming request
    path = event.get('path', '')
    method = event.get('httpMethod', 'GET')
    headers = event.get('headers', {})
    body = event.get('body', '')
    query_params = event.get('queryStringParameters', {})
    
    # Create a Flask test client request
    with app.test_client() as client:
        # Build the query string
        query_string = '&'.join([f"{k}={v}" for k, v in (query_params or {}).items()])
        full_path = path
        if query_string:
            full_path = f"{path}?{query_string}"
        
        # Make the request
        if method == 'GET':
            response = client.get(full_path, headers=headers)
        elif method == 'POST':
            response = client.post(full_path, data=body, headers=headers)
        elif method == 'PUT':
            response = client.put(full_path, data=body, headers=headers)
        elif method == 'DELETE':
            response = client.delete(full_path, headers=headers)
        else:
            response = client.get(full_path, headers=headers)
    
    return {
        'statusCode': response.status_code,
        'body': response.get_data(as_text=True),
        'headers': dict(response.headers)
    }
