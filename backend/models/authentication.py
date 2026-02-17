"""
User Authentication & Role Management Module
Provides secure authentication with role-based access control.
Supports Admin, Farmer, and Buyer roles with different permissions.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from functools import wraps
import hashlib
import secrets
import json


class UserRole:
    """User role definitions"""
    ADMIN = 'admin'
    FARMER = 'farmer'
    BUYER = 'buyer'
    GUEST = 'guest'


class Permission:
    """Permission definitions"""
    # Classification
    CLASSIFY = 'classify'
    VIEW_HISTORY = 'view_history'
    DELETE_HISTORY = 'delete_history'
    
    # Analytics
    VIEW_ANALYTICS = 'view_analytics'
    EXPORT_REPORTS = 'export_reports'
    
    # Inventory
    VIEW_INVENTORY = 'view_inventory'
    MANAGE_INVENTORY = 'manage_inventory'
    
    # Pricing
    VIEW_PRICING = 'view_pricing'
    SET_PRICING = 'set_pricing'
    
    # Admin
    MANAGE_USERS = 'manage_users'
    SYSTEM_CONFIG = 'system_config'
    VIEW_AUDIT_LOG = 'view_audit_log'
    RETRAIN_MODEL = 'retrain_model'
    
    # API
    API_ACCESS = 'api_access'
    WEBHOOK_MANAGE = 'webhook_manage'


# Role-Permission Mapping
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        Permission.CLASSIFY, Permission.VIEW_HISTORY, Permission.DELETE_HISTORY,
        Permission.VIEW_ANALYTICS, Permission.EXPORT_REPORTS,
        Permission.VIEW_INVENTORY, Permission.MANAGE_INVENTORY,
        Permission.VIEW_PRICING, Permission.SET_PRICING,
        Permission.MANAGE_USERS, Permission.SYSTEM_CONFIG, Permission.VIEW_AUDIT_LOG,
        Permission.RETRAIN_MODEL, Permission.API_ACCESS, Permission.WEBHOOK_MANAGE
    ],
    UserRole.FARMER: [
        Permission.CLASSIFY, Permission.VIEW_HISTORY,
        Permission.VIEW_ANALYTICS, Permission.EXPORT_REPORTS,
        Permission.VIEW_INVENTORY, Permission.MANAGE_INVENTORY,
        Permission.VIEW_PRICING,
        Permission.API_ACCESS
    ],
    UserRole.BUYER: [
        Permission.CLASSIFY, Permission.VIEW_HISTORY,
        Permission.VIEW_ANALYTICS,
        Permission.VIEW_INVENTORY,
        Permission.VIEW_PRICING,
        Permission.API_ACCESS
    ],
    UserRole.GUEST: [
        Permission.CLASSIFY
    ]
}


class AuthenticationManager:
    """
    Manages user authentication, sessions, and role-based access control.
    Uses MongoDB for persistent storage.
    """
    
    # Use a fixed secret key for consistent password hashing
    SECRET_KEY = 'fruitai_secret_key_2024'
    
    def __init__(self, db_handler=None):
        """
        Initialize authentication manager.
        
        Args:
            db_handler: Optional database handler for persistent storage
        """
        self.db = db_handler
        if self.db is None:
            try:
                from backend.models.database import DatabaseHandler
                from backend.config import Config
                self.db = DatabaseHandler(Config.MONGODB_URI, Config.DB_NAME)
            except Exception as e:
                print(f"Warning: Could not connect to MongoDB: {e}")
                self.db = None
        
        self.session_timeout = 3600  # 1 hour
    
    def _hash_password(self, password: str) -> str:
        """Hash password securely"""
        salt = self.SECRET_KEY[:16]
        return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return self._hash_password(password) == password_hash
    
    def _generate_token(self) -> str:
        """Generate secure session token"""
        return secrets.token_urlsafe(32)
    
    def register_user(
        self,
        username: str,
        password: str,
        email: str,
        role: str = UserRole.BUYER,
        full_name: str = None,
        **extra_fields
    ) -> Dict[str, Any]:
        """
        Register a new user.
        
        Args:
            username: Unique username
            password: Plain text password (will be hashed)
            email: User email
            role: User role (admin, farmer, buyer, guest)
            full_name: Optional full name
        
        Returns:
            Registration result
        """
        # Validate inputs
        if len(username) < 3:
            return {'success': False, 'error': 'Username must be at least 3 characters'}
        
        if len(password) < 6:
            return {'success': False, 'error': 'Password must be at least 6 characters'}
        
        # Prevent creating admin accounts through registration
        if role == UserRole.ADMIN:
            role = UserRole.BUYER
        
        if self.db:
            # Check if user exists
            if self.db.check_user_exists(username=username):
                return {'success': False, 'error': 'Username already exists'}
            
            if self.db.check_user_exists(email=email):
                return {'success': False, 'error': 'Email already registered'}
            
            # Create user in MongoDB
            result = self.db.create_user(
                username=username,
                password_hash=self._hash_password(password),
                email=email,
                role=role,
                full_name=full_name or username
            )
            
            if result['success']:
                return {
                    'success': True,
                    'message': 'User registered successfully',
                    'user': {
                        'username': username,
                        'email': email,
                        'role': role
                    }
                }
            return result
        else:
            return {'success': False, 'error': 'Database not available'}
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user and create session.
        
        Args:
            username: Username
            password: Plain text password
        
        Returns:
            Login result with session token if successful
        """
        if not self.db:
            return {'success': False, 'error': 'Database not available'}
        
        user = self.db.get_user_by_username(username)
        
        if not user:
            return {'success': False, 'error': 'Invalid username or password'}
        
        if not user.get('is_active', True):
            return {'success': False, 'error': 'Account is inactive'}
        
        if not self._verify_password(password, user['password_hash']):
            return {'success': False, 'error': 'Invalid username or password'}
        
        # Create session
        token = self._generate_token()
        expires_at = datetime.now() + timedelta(seconds=self.session_timeout)
        
        self.db.create_session(token, username, user['role'], expires_at)
        self.db.update_user_login(username)
        
        return {
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': {
                'username': user['username'],
                'role': user['role'],
                'full_name': user.get('full_name', username),
                'email': user.get('email', ''),
                'permissions': ROLE_PERMISSIONS.get(user['role'], [])
            }
        }
    
    def logout(self, token: str) -> Dict[str, Any]:
        """
        Invalidate a session token.
        
        Args:
            token: Session token
        
        Returns:
            Logout result
        """
        if self.db:
            self.db.delete_session(token)
        return {'success': True, 'message': 'Logged out successfully'}
    
    def validate_session(self, token: str) -> Dict[str, Any]:
        """
        Validate a session token.
        
        Args:
            token: Session token
        
        Returns:
            Validation result with user info if valid
        """
        if not self.db:
            return {'valid': False, 'error': 'Database not available'}
        
        session = self.db.get_session(token)
        
        if not session:
            return {'valid': False, 'error': 'Invalid or expired token'}
        
        user = self.db.get_user_by_username(session['username'])
        if not user:
            return {'valid': False, 'error': 'User not found'}
        
        return {
            'valid': True,
            'user': {
                'username': user['username'],
                'role': user['role'],
                'full_name': user.get('full_name', ''),
                'permissions': ROLE_PERMISSIONS.get(user['role'], [])
            }
        }
    
    def check_permission(self, token: str, permission: str) -> bool:
        """
        Check if session has specific permission.
        
        Args:
            token: Session token
            permission: Required permission
        
        Returns:
            True if permission granted
        """
        session = self.validate_session(token)
        if not session.get('valid'):
            return False
        
        return permission in session.get('user', {}).get('permissions', [])
    
    def get_role_permissions(self, role: str) -> List[str]:
        """Get permissions for a role"""
        return ROLE_PERMISSIONS.get(role, [])
    
    def get_user_dashboard_config(self, role: str) -> Dict[str, Any]:
        """
        Get role-specific dashboard configuration.
        
        Args:
            role: User role
        
        Returns:
            Dashboard configuration for the role
        """
        configs = {
            UserRole.ADMIN: {
                'sections': ['classification', 'analytics', 'inventory', 'pricing', 'users', 'system', 'reports'],
                'widgets': ['kpi_overview', 'quality_chart', 'defect_alerts', 'user_activity', 'system_status'],
                'quick_actions': ['new_classification', 'export_report', 'manage_users', 'system_config'],
                'theme': 'admin'
            },
            UserRole.FARMER: {
                'sections': ['classification', 'analytics', 'inventory', 'reports'],
                'widgets': ['kpi_overview', 'quality_chart', 'spoilage_alerts', 'inventory_status'],
                'quick_actions': ['new_classification', 'export_report', 'update_inventory'],
                'theme': 'farmer'
            },
            UserRole.BUYER: {
                'sections': ['classification', 'analytics', 'inventory', 'pricing'],
                'widgets': ['available_inventory', 'quality_summary', 'price_trends'],
                'quick_actions': ['new_classification', 'view_inventory', 'contact_seller'],
                'theme': 'buyer'
            },
            UserRole.GUEST: {
                'sections': ['classification'],
                'widgets': ['classification_result'],
                'quick_actions': ['new_classification'],
                'theme': 'guest'
            }
        }
        
        return configs.get(role, configs[UserRole.GUEST])
    
    def _log_action(self, username: str, action: str, details: Dict):
        """Log authentication action for audit"""
        self.audit_log.append({
            'timestamp': datetime.now().isoformat(),
            'username': username,
            'action': action,
            'details': details
        })
        # Keep only last 1000 entries
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-1000:]
    
    def get_audit_log(self, limit: int = 100) -> List[Dict]:
        """Get recent audit log entries"""
        return self.audit_log[-limit:]
    
    def get_all_users(self) -> List[Dict]:
        """Get all users (admin only, passwords excluded)"""
        return [
            {
                'username': u['username'],
                'email': u['email'],
                'role': u['role'],
                'full_name': u.get('full_name'),
                'created_at': u['created_at'],
                'last_login': u['last_login'],
                'is_active': u.get('is_active', True)
            }
            for u in self.users.values()
        ]
    
    def update_user_role(self, admin_token: str, username: str, new_role: str) -> Dict[str, Any]:
        """
        Update user's role (admin only).
        
        Args:
            admin_token: Admin session token
            username: Target username
            new_role: New role to assign
        
        Returns:
            Update result
        """
        if not self.check_permission(admin_token, Permission.MANAGE_USERS):
            return {'success': False, 'error': 'Insufficient permissions'}
        
        if username not in self.users:
            return {'success': False, 'error': 'User not found'}
        
        if new_role not in [UserRole.ADMIN, UserRole.FARMER, UserRole.BUYER, UserRole.GUEST]:
            return {'success': False, 'error': 'Invalid role'}
        
        self.users[username]['role'] = new_role
        admin_username = self.sessions.get(admin_token, {}).get('username', 'unknown')
        self._log_action(admin_username, 'role_updated', {'target_user': username, 'new_role': new_role})
        
        return {'success': True, 'message': f'User {username} role updated to {new_role}'}
    
    def deactivate_user(self, admin_token: str, username: str) -> Dict[str, Any]:
        """Deactivate a user account (admin only)"""
        if not self.check_permission(admin_token, Permission.MANAGE_USERS):
            return {'success': False, 'error': 'Insufficient permissions'}
        
        if username not in self.users:
            return {'success': False, 'error': 'User not found'}
        
        self.users[username]['is_active'] = False
        
        # Invalidate any active sessions
        tokens_to_remove = [t for t, s in self.sessions.items() if s['username'] == username]
        for token in tokens_to_remove:
            del self.sessions[token]
        
        return {'success': True, 'message': f'User {username} deactivated'}


def require_permission(permission: str):
    """
    Decorator to require specific permission for route access.
    
    Usage:
        @app.route('/admin/users')
        @require_permission(Permission.MANAGE_USERS)
        def manage_users():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request, jsonify
            
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            
            if not token:
                return jsonify({'error': 'Authentication required'}), 401
            
            # Get auth manager from app context
            from flask import current_app
            auth_manager = getattr(current_app, 'auth_manager', None)
            
            if not auth_manager:
                return jsonify({'error': 'Authentication system not configured'}), 500
            
            session = auth_manager.validate_session(token)
            if not session.get('valid'):
                return jsonify({'error': session.get('error', 'Invalid session')}), 401
            
            if not auth_manager.check_permission(token, permission):
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
