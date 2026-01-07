"""
Simple local file storage for images
No cloud services required - completely free
"""
import os
from werkzeug.utils import secure_filename
from flask import current_app, url_for
import uuid

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file, folder='general'):
    """
    Save uploaded image to local storage
    
    Args:
        file: FileStorage object from request.files
        folder: Subfolder name (e.g., 'bakeries', 'products', 'surplus_bags')
        
    Returns:
        URL path to saved image, or None if failed
    """
    if not file or not allowed_file(file.filename):
        return None
    
    # Create unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    
    # Create upload directory if it doesn't exist
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads', folder)
    os.makedirs(upload_path, exist_ok=True)
    
    # Save file
    filepath = os.path.join(upload_path, filename)
    file.save(filepath)
    
    # Return URL path
    return f"/static/uploads/{folder}/{filename}"

def delete_image(image_url):
    """
    Delete image file from local storage
    
    Args:
        image_url: URL path to image (e.g., '/static/uploads/bakeries/abc123.jpg')
    """
    if not image_url or not image_url.startswith('/static/uploads/'):
        return
    
    try:
        filepath = os.path.join(current_app.root_path, image_url.lstrip('/'))
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Error deleting image: {str(e)}")
