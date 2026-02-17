"""
Configuration settings for the Fruit Classification System
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DB_NAME = os.getenv('DB_NAME', 'fruit_classification_db')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'data/uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')
    USE_OPENAI = os.getenv('USE_OPENAI', 'true').lower() == 'true'
    
    # Model Configuration (for local model if needed)
    MODEL_PATH = os.getenv('MODEL_PATH', 'trained_models/fruit_classifier.h5')
    IMAGE_SIZE = int(os.getenv('IMAGE_SIZE', 224))
    
    # Fruit Categories
    FRUIT_CLASSES = [
        'Apple', 'Banana', 'Orange', 'Mango', 'Strawberry',
        'Grape', 'Watermelon', 'Pineapple', 'Cherry', 'Kiwi'
    ]
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
