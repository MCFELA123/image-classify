"""
Utility functions for image processing and validation
"""
import os
from PIL import Image
import numpy as np
from werkzeug.utils import secure_filename


def allowed_file(filename, allowed_extensions):
    """
    Check if file has an allowed extension
    
    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions
        
    Returns:
        Boolean indicating if file is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def preprocess_image(image_path, target_size=(224, 224)):
    """
    Preprocess image for model prediction
    
    Args:
        image_path: Path to the image file
        target_size: Target size for resizing (width, height)
        
    Returns:
        Preprocessed image array
    """
    # Load image
    img = Image.open(image_path)
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize image
    img = img.resize(target_size, Image.LANCZOS)
    
    # Convert to array and normalize
    img_array = np.array(img)
    img_array = img_array.astype('float32') / 255.0
    
    return img_array


def save_uploaded_file(file, upload_folder):
    """
    Save uploaded file securely
    
    Args:
        file: FileStorage object from Flask
        upload_folder: Directory to save the file
        
    Returns:
        Tuple of (success, filepath or error message)
    """
    try:
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Create unique filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        unique_filename = f"{name}_{timestamp}{ext}"
        
        # Ensure upload folder exists
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save file
        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)
        
        return True, filepath
    except Exception as e:
        return False, str(e)


def validate_image(image_path, max_size_mb=10):
    """
    Validate image file
    
    Args:
        image_path: Path to the image file
        max_size_mb: Maximum file size in MB
        
    Returns:
        Tuple of (is_valid, error_message or None)
    """
    try:
        # Check file size
        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
        if file_size_mb > max_size_mb:
            return False, f"File size exceeds {max_size_mb}MB limit"
        
        # Try to open and verify image
        img = Image.open(image_path)
        img.verify()
        
        # Reopen image (verify closes it)
        img = Image.open(image_path)
        
        # Check image dimensions
        width, height = img.size
        if width < 50 or height < 50:
            return False, "Image dimensions too small (minimum 50x50 pixels)"
        
        if width > 5000 or height > 5000:
            return False, "Image dimensions too large (maximum 5000x5000 pixels)"
        
        return True, None
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"


def create_thumbnail(image_path, thumbnail_size=(150, 150)):
    """
    Create a thumbnail of an image
    
    Args:
        image_path: Path to the original image
        thumbnail_size: Size of the thumbnail (width, height)
        
    Returns:
        Path to the thumbnail or None if failed
    """
    try:
        img = Image.open(image_path)
        img.thumbnail(thumbnail_size, Image.LANCZOS)
        
        # Create thumbnail path
        directory = os.path.dirname(image_path)
        filename = os.path.basename(image_path)
        name, ext = os.path.splitext(filename)
        thumbnail_path = os.path.join(directory, f"{name}_thumb{ext}")
        
        # Save thumbnail
        img.save(thumbnail_path)
        
        return thumbnail_path
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return None


def format_confidence(confidence):
    """
    Format confidence score as percentage
    
    Args:
        confidence: Confidence score (0-1)
        
    Returns:
        Formatted string (e.g., "95.5%")
    """
    return f"{confidence * 100:.1f}%"


def get_color_for_confidence(confidence):
    """
    Get color code based on confidence level
    
    Args:
        confidence: Confidence score (0-1)
        
    Returns:
        Color name or hex code
    """
    if confidence >= 0.8:
        return "green"
    elif confidence >= 0.6:
        return "yellow"
    else:
        return "red"
