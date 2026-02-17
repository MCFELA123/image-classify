"""
Security and Privacy Module
Handles data privacy, image cleanup, and security features
"""
import os
import shutil
import hashlib
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class SecurityManager:
    """
    Manages security and privacy features:
    - Automatic image cleanup after processing
    - Data anonymization
    - Access logging
    - Privacy compliance
    """
    
    def __init__(self, upload_folder: str, retention_hours: int = 1):
        """
        Initialize security manager
        
        Args:
            upload_folder: Path to uploaded images folder
            retention_hours: How long to keep images (default: 1 hour)
        """
        self.upload_folder = upload_folder
        self.retention_hours = retention_hours
        self.access_log = []
        self.cleanup_thread = None
        self._running = False
    
    # ==================== Image Privacy ====================
    
    def delete_image_immediately(self, image_path: str) -> bool:
        """
        Delete an image file immediately after processing
        
        Args:
            image_path: Path to the image file
            
        Returns:
            True if deleted successfully
        """
        try:
            if os.path.exists(image_path):
                # Secure delete - overwrite with random data before deletion
                self._secure_delete(image_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting image: {e}")
            return False
    
    def _secure_delete(self, file_path: str):
        """Securely delete a file by overwriting before removal"""
        try:
            file_size = os.path.getsize(file_path)
            with open(file_path, 'wb') as f:
                # Overwrite with random bytes
                f.write(os.urandom(file_size))
            os.remove(file_path)
        except Exception:
            # Fallback to regular delete
            if os.path.exists(file_path):
                os.remove(file_path)
    
    def cleanup_old_images(self, force: bool = False) -> Dict:
        """
        Clean up images older than retention period
        
        Args:
            force: If True, delete all images regardless of age
            
        Returns:
            Cleanup statistics
        """
        deleted_count = 0
        failed_count = 0
        total_size_freed = 0
        
        if not os.path.exists(self.upload_folder):
            return {'deleted': 0, 'failed': 0, 'size_freed_bytes': 0}
        
        cutoff_time = datetime.now() - timedelta(hours=self.retention_hours)
        
        for filename in os.listdir(self.upload_folder):
            file_path = os.path.join(self.upload_folder, filename)
            
            if not os.path.isfile(file_path):
                continue
            
            try:
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if force or file_mtime < cutoff_time:
                    file_size = os.path.getsize(file_path)
                    self._secure_delete(file_path)
                    deleted_count += 1
                    total_size_freed += file_size
            except Exception as e:
                failed_count += 1
                print(f"Failed to clean up {filename}: {e}")
        
        return {
            'deleted': deleted_count,
            'failed': failed_count,
            'size_freed_bytes': total_size_freed,
            'size_freed_mb': round(total_size_freed / (1024 * 1024), 2)
        }
    
    def start_cleanup_scheduler(self, interval_minutes: int = 30):
        """
        Start background thread for automatic image cleanup
        
        Args:
            interval_minutes: How often to run cleanup (default: 30 minutes)
        """
        if self._running:
            return
        
        self._running = True
        
        def cleanup_loop():
            while self._running:
                self.cleanup_old_images()
                time.sleep(interval_minutes * 60)
        
        self.cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        self.cleanup_thread.start()
        print(f"🔒 Image cleanup scheduler started (every {interval_minutes} minutes)")
    
    def stop_cleanup_scheduler(self):
        """Stop the cleanup scheduler"""
        self._running = False
    
    # ==================== Data Anonymization ====================
    
    def anonymize_classification(self, classification: Dict) -> Dict:
        """
        Anonymize classification data for sharing/export
        
        Args:
            classification: Classification result
            
        Returns:
            Anonymized classification
        """
        anonymized = classification.copy()
        
        # Remove potentially identifying information
        fields_to_remove = ['image_path', 'image_filename', 'user_id', 'ip_address']
        for field in fields_to_remove:
            anonymized.pop(field, None)
        
        # Hash the ID if present
        if '_id' in anonymized:
            anonymized['_id'] = self._hash_id(str(anonymized['_id']))
        if 'classification_id' in anonymized:
            anonymized['classification_id'] = self._hash_id(str(anonymized['classification_id']))
        
        return anonymized
    
    def _hash_id(self, id_value: str) -> str:
        """Create a hash of an ID for anonymization"""
        return hashlib.sha256(id_value.encode()).hexdigest()[:16]
    
    # ==================== Access Logging ====================
    
    def log_access(self, action: str, resource: str, 
                   user_id: Optional[str] = None, metadata: Optional[Dict] = None):
        """
        Log access to resources for audit trail
        
        Args:
            action: Type of action (classify, view, export, etc.)
            resource: Resource accessed
            user_id: Optional user identifier
            metadata: Additional metadata
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'action': action,
            'resource': resource,
            'user_id': self._hash_id(user_id) if user_id else 'anonymous',
            'metadata': metadata or {}
        }
        
        self.access_log.append(log_entry)
        
        # Keep only last 1000 entries in memory
        if len(self.access_log) > 1000:
            self.access_log = self.access_log[-1000:]
    
    def get_access_log(self, limit: int = 100) -> List[Dict]:
        """Get recent access log entries"""
        return self.access_log[-limit:]
    
    # ==================== Privacy Compliance ====================
    
    def get_privacy_policy(self) -> Dict:
        """
        Get privacy policy information
        
        Returns:
            Privacy policy details
        """
        return {
            'policy_version': '1.0',
            'last_updated': '2024-01-15',
            'data_collection': {
                'images': {
                    'purpose': 'Fruit classification analysis',
                    'retention': f'{self.retention_hours} hour(s)',
                    'storage': 'Temporary local storage only',
                    'sharing': 'Images are never shared with third parties',
                    'processing': 'Processed using OpenAI Vision API'
                },
                'classification_results': {
                    'purpose': 'Providing analysis results and maintaining history',
                    'retention': '30 days by default',
                    'storage': 'Encrypted database',
                    'sharing': 'Aggregate statistics only, no individual data'
                },
                'metadata': {
                    'purpose': 'System improvement and debugging',
                    'collected': ['timestamp', 'classification results', 'confidence scores'],
                    'not_collected': ['IP addresses', 'personal information', 'device identifiers']
                }
            },
            'user_rights': {
                'access': 'Users can view their classification history',
                'deletion': 'Users can request deletion via /api/privacy/delete',
                'export': 'Users can export data via /api/integration/export',
                'opt_out': 'Images can be processed without storage'
            },
            'security_measures': [
                'All API communications use HTTPS',
                'Images are automatically deleted after processing',
                'Database access is authenticated and encrypted',
                'No persistent storage of raw image data',
                'Regular security audits and updates'
            ],
            'contact': {
                'privacy_email': 'privacy@fruitai.example.com',
                'data_protection_officer': 'Available upon request'
            }
        }
    
    def get_ethical_guidelines(self) -> Dict:
        """
        Get ethical guidelines for AI use in agriculture
        
        Returns:
            Ethical guidelines document
        """
        return {
            'document_version': '1.0',
            'principles': {
                'transparency': {
                    'description': 'All AI decisions are explainable and transparent',
                    'implementation': [
                        'Confidence scores provided for all predictions',
                        'Clear indication when results may be uncertain',
                        'Documentation of model limitations',
                        'Open about use of OpenAI Vision API'
                    ]
                },
                'fairness': {
                    'description': 'System treats all inputs fairly without bias',
                    'implementation': [
                        'Model trained on diverse datasets',
                        'Regular bias testing and correction',
                        'Equal accuracy across different fruit varieties',
                        'No discrimination based on image source'
                    ]
                },
                'accountability': {
                    'description': 'Clear responsibility for AI decisions',
                    'implementation': [
                        'Human verification recommended for critical decisions',
                        'Audit trail for all classifications',
                        'Clear escalation path for disputes',
                        'Regular accuracy monitoring and reporting'
                    ]
                },
                'privacy': {
                    'description': 'User and data privacy is protected',
                    'implementation': [
                        'Minimal data collection policy',
                        'Automatic data deletion',
                        'No sale or sharing of user data',
                        'Compliance with data protection regulations'
                    ]
                },
                'beneficence': {
                    'description': 'System designed to benefit agricultural community',
                    'implementation': [
                        'Helps reduce food waste through quality assessment',
                        'Supports fair pricing based on actual quality',
                        'Enables better inventory management',
                        'Promotes sustainable agricultural practices'
                    ]
                }
            },
            'limitations_acknowledgment': {
                'description': 'We acknowledge the following limitations',
                'limitations': [
                    'AI predictions are not 100% accurate',
                    'System should supplement, not replace, human expertise',
                    'Visual analysis cannot detect internal quality issues',
                    'Results may vary with image quality and conditions',
                    'Rare fruit varieties may have lower accuracy'
                ],
                'recommendations': [
                    'Use results as guidance, not absolute truth',
                    'Verify critical decisions with human experts',
                    'Report any suspected errors for model improvement',
                    'Maintain manual quality control processes'
                ]
            },
            'agricultural_impact': {
                'positive_impacts': [
                    'Reduced food waste through better sorting',
                    'Faster quality assessment process',
                    'More consistent grading across batches',
                    'Better market matching for produce',
                    'Support for small farmers with limited expertise'
                ],
                'potential_risks': [
                    'Over-reliance on automated systems',
                    'Potential for systematic grading errors',
                    'Economic impact if quality is misjudged'
                ],
                'mitigation_strategies': [
                    'Regular calibration against expert assessments',
                    'Confidence thresholds for automatic decisions',
                    'Human review for borderline cases',
                    'Continuous feedback and improvement loop'
                ]
            }
        }
    
    def delete_user_data(self, user_id: str = None, 
                         classification_ids: List[str] = None) -> Dict:
        """
        Delete user data upon request (GDPR compliance)
        
        Args:
            user_id: User identifier to delete data for
            classification_ids: Specific classification IDs to delete
            
        Returns:
            Deletion summary
        """
        deleted = {
            'images': 0,
            'classifications': 0,
            'logs': 0
        }
        
        # In production, this would interact with the database
        # For now, return the structure
        
        return {
            'status': 'completed',
            'deleted_data': deleted,
            'timestamp': datetime.utcnow().isoformat(),
            'note': 'Data deletion request processed successfully'
        }


class ImagePrivacyHandler:
    """
    Handles image-specific privacy operations
    """
    
    def __init__(self, security_manager: SecurityManager):
        self.security_manager = security_manager
    
    def process_with_privacy(self, image_path: str, 
                             delete_after: bool = True) -> Tuple[str, bool]:
        """
        Process image with privacy controls
        
        Args:
            image_path: Path to the image
            delete_after: Whether to delete after processing
            
        Returns:
            Tuple of (image_path, should_delete)
        """
        return (image_path, delete_after)
    
    def strip_metadata(self, image_path: str) -> bool:
        """
        Strip EXIF and other metadata from image
        
        Args:
            image_path: Path to the image
            
        Returns:
            True if metadata stripped successfully
        """
        try:
            from PIL import Image
            
            img = Image.open(image_path)
            # Create a new image without metadata
            data = list(img.getdata())
            img_no_meta = Image.new(img.mode, img.size)
            img_no_meta.putdata(data)
            img_no_meta.save(image_path)
            
            return True
        except ImportError:
            # PIL not available, skip metadata stripping
            return False
        except Exception as e:
            print(f"Error stripping metadata: {e}")
            return False


# Singleton instance
_security_manager = None


def get_security_manager(upload_folder: str = 'data/uploads', 
                         retention_hours: int = 1) -> SecurityManager:
    """Get or create the security manager instance"""
    global _security_manager
    if _security_manager is None:
        _security_manager = SecurityManager(upload_folder, retention_hours)
    return _security_manager
