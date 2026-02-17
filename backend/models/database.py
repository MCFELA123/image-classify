"""
MongoDB Database Handler for Fruit Classification System
"""
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import json


class DatabaseHandler:
    def __init__(self, mongodb_uri, db_name):
        """
        Initialize MongoDB connection
        
        Args:
            mongodb_uri: MongoDB connection string
            db_name: Database name
        """
        # Add SSL certificate options for MongoDB Atlas
        import ssl
        self.client = MongoClient(
            mongodb_uri,
            tlsAllowInvalidCertificates=True,  # Bypass SSL verification
            serverSelectionTimeoutMS=5000
        )
        self.db = self.client[db_name]
        self.classifications = self.db['classifications']
        self.statistics = self.db['statistics']
        self.users = self.db['users']
        self.sessions = self.db['sessions']
        
        # Create indexes
        self.classifications.create_index([('timestamp', -1)])
        self.classifications.create_index([('predicted_class', 1)])
        self.users.create_index([('username', 1)], unique=True)
        self.users.create_index([('email', 1)], unique=True)
        self.sessions.create_index([('token', 1)], unique=True)
        self.sessions.create_index([('expires_at', 1)], expireAfterSeconds=0)
        
        # Initialize default users if not exist
        self._init_default_users()
    
    def save_classification(self, image_filename, prediction_result, image_path=None):
        """
        Save a classification result to the database
        
        Args:
            image_filename: Name of the classified image
            prediction_result: Dictionary containing prediction results
            image_path: Optional path to the saved image
            
        Returns:
            Inserted document ID
        """
        document = {
            'image_filename': image_filename,
            'image_path': image_path,
            'predicted_class': prediction_result['predicted_class'],
            'confidence': prediction_result['confidence'],
            'top_3_predictions': prediction_result['top_3_predictions'],
            'all_predictions': prediction_result.get('all_predictions', {}),
            'timestamp': datetime.utcnow()
        }
        
        result = self.classifications.insert_one(document)
        
        # Update statistics
        self._update_statistics(prediction_result['predicted_class'])
        
        return str(result.inserted_id)
    
    def get_classification_by_id(self, classification_id):
        """
        Retrieve a classification by its ID
        
        Args:
            classification_id: String ID of the classification
            
        Returns:
            Classification document or None
        """
        try:
            doc = self.classifications.find_one({'_id': ObjectId(classification_id)})
            if doc:
                doc['_id'] = str(doc['_id'])
                doc['timestamp'] = doc['timestamp'].isoformat()
            return doc
        except:
            return None
    
    def get_recent_classifications(self, limit=20):
        """
        Get recent classification results
        
        Args:
            limit: Number of results to return
            
        Returns:
            List of classification documents
        """
        cursor = self.classifications.find().sort('timestamp', -1).limit(limit)
        results = []
        
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            if hasattr(doc.get('timestamp'), 'isoformat'):
                doc['timestamp'] = doc['timestamp'].isoformat()
            results.append(doc)
        
        return results
    
    def get_classifications_in_range(self, days=30):
        """
        Get classifications within a date range
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of classification documents
        """
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        cursor = self.classifications.find(
            {'timestamp': {'$gte': cutoff_date}}
        ).sort('timestamp', -1)
        
        results = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            if hasattr(doc.get('timestamp'), 'isoformat'):
                doc['timestamp'] = doc['timestamp'].isoformat()
            results.append(doc)
        
        return results
    
    def get_classifications_by_class(self, fruit_class, limit=20):
        """
        Get classifications for a specific fruit class
        
        Args:
            fruit_class: Name of the fruit class
            limit: Number of results to return
            
        Returns:
            List of classification documents
        """
        cursor = self.classifications.find(
            {'predicted_class': fruit_class}
        ).sort('timestamp', -1).limit(limit)
        
        results = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            doc['timestamp'] = doc['timestamp'].isoformat()
            results.append(doc)
        
        return results
    
    def _update_statistics(self, fruit_class):
        """
        Update classification statistics
        
        Args:
            fruit_class: Classified fruit class
        """
        self.statistics.update_one(
            {'_id': 'overall'},
            {
                '$inc': {
                    'total_classifications': 1,
                    f'class_counts.{fruit_class}': 1
                },
                '$set': {'last_updated': datetime.utcnow()}
            },
            upsert=True
        )
    
    def get_statistics(self):
        """
        Get overall classification statistics
        
        Returns:
            Statistics document
        """
        stats = self.statistics.find_one({'_id': 'overall'})
        
        if stats:
            stats['_id'] = str(stats['_id'])
            if 'last_updated' in stats:
                stats['last_updated'] = stats['last_updated'].isoformat()
            return stats
        
        return {
            'total_classifications': 0,
            'class_counts': {}
        }
    
    def clear_old_classifications(self, days=30):
        """
        Delete classifications older than specified days
        
        Args:
            days: Number of days to keep
            
        Returns:
            Number of deleted documents
        """
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        result = self.classifications.delete_many({
            'timestamp': {'$lt': cutoff_date}
        })
        
        return result.deleted_count
    
    def close_connection(self):
        """Close the database connection"""
        self.client.close()
    
    def _init_default_users(self):
        """Initialize default users if they don't exist"""
        import hashlib
        import secrets
        
        secret_key = 'fruitai_secret_key_2024'
        
        def hash_password(password):
            salt = secret_key[:16]
            return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
        
        default_users = [
            {
                'username': 'admin',
                'password_hash': hash_password('admin123'),
                'email': 'admin@fruitai.com',
                'role': 'admin',
                'full_name': 'System Administrator',
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'username': 'farmer1',
                'password_hash': hash_password('farmer123'),
                'email': 'farmer@fruitai.com',
                'role': 'farmer',
                'full_name': 'Demo Farmer',
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'username': 'buyer1',
                'password_hash': hash_password('buyer123'),
                'email': 'buyer@fruitai.com',
                'role': 'buyer',
                'full_name': 'Demo Buyer',
                'created_at': datetime.utcnow(),
                'is_active': True
            }
        ]
        
        for user in default_users:
            try:
                self.users.update_one(
                    {'username': user['username']},
                    {'$setOnInsert': user},
                    upsert=True
                )
            except:
                pass
    
    # ==================== USER MANAGEMENT ====================
    
    def get_user_by_username(self, username):
        """Get user by username"""
        user = self.users.find_one({'username': username})
        if user:
            user['_id'] = str(user['_id'])
            if 'created_at' in user and hasattr(user['created_at'], 'isoformat'):
                user['created_at'] = user['created_at'].isoformat()
            if 'last_login' in user and user['last_login'] and hasattr(user['last_login'], 'isoformat'):
                user['last_login'] = user['last_login'].isoformat()
        return user
    
    def create_user(self, username, password_hash, email, role, full_name):
        """Create a new user"""
        user = {
            'username': username,
            'password_hash': password_hash,
            'email': email,
            'role': role,
            'full_name': full_name,
            'created_at': datetime.utcnow(),
            'last_login': None,
            'is_active': True
        }
        
        try:
            result = self.users.insert_one(user)
            return {'success': True, 'user_id': str(result.inserted_id)}
        except Exception as e:
            if 'duplicate key' in str(e).lower():
                return {'success': False, 'error': 'Username or email already exists'}
            return {'success': False, 'error': str(e)}
    
    def update_user_login(self, username):
        """Update user's last login time"""
        self.users.update_one(
            {'username': username},
            {'$set': {'last_login': datetime.utcnow()}}
        )
    
    def check_user_exists(self, username=None, email=None):
        """Check if user exists by username or email"""
        query = {}
        if username:
            query['username'] = username
        if email:
            query['email'] = email
        return self.users.find_one(query) is not None
    
    # ==================== SESSION MANAGEMENT ====================
    
    def create_session(self, token, username, role, expires_at):
        """Create a new session"""
        session = {
            'token': token,
            'username': username,
            'role': role,
            'created_at': datetime.utcnow(),
            'expires_at': expires_at
        }
        
        try:
            self.sessions.insert_one(session)
            return True
        except:
            return False
    
    def get_session(self, token):
        """Get session by token"""
        session = self.sessions.find_one({'token': token})
        if session and session.get('expires_at', datetime.utcnow()) > datetime.utcnow():
            return session
        return None
    
    def delete_session(self, token):
        """Delete a session"""
        self.sessions.delete_one({'token': token})

