"""
Model Retraining Module
Enables periodic model retraining with new fruit images.
Supports data collection, augmentation, and incremental learning.
"""
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import os
import json
import shutil


class ModelRetrainer:
    """
    Manages model retraining pipeline with new data.
    Supports data collection, validation, and training workflows.
    """
    
    def __init__(self, base_path: str = None):
        """
        Initialize retraining module.
        
        Args:
            base_path: Base path for training data and models
        """
        self.base_path = base_path or os.path.join(os.getcwd(), 'training_data')
        self.new_data_path = os.path.join(self.base_path, 'new_samples')
        self.validated_path = os.path.join(self.base_path, 'validated')
        self.model_history_path = os.path.join(self.base_path, 'model_versions')
        
        # Ensure directories exist
        for path in [self.new_data_path, self.validated_path, self.model_history_path]:
            os.makedirs(path, exist_ok=True)
        
        # Training configuration
        self.config = {
            'min_samples_per_class': 10,
            'validation_split': 0.2,
            'image_size': (224, 224),
            'batch_size': 32,
            'epochs': 10,
            'learning_rate': 0.0001,
            'augmentation': True
        }
        
        self._tf_available = self._check_tensorflow()
    
    def _check_tensorflow(self) -> bool:
        """Check if TensorFlow is available"""
        try:
            import tensorflow as tf
            return True
        except ImportError:
            return False
    
    def add_training_sample(
        self,
        image_path: str,
        fruit_class: str,
        verified: bool = False,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Add a new training sample to the collection.
        
        Args:
            image_path: Path to the image file
            fruit_class: Verified fruit class label
            verified: Whether label has been manually verified
            metadata: Additional metadata (ripeness, quality, etc.)
        
        Returns:
            Result of adding the sample
        """
        if not os.path.exists(image_path):
            return {'success': False, 'error': 'Image file not found'}
        
        # Create class directory
        class_dir = os.path.join(
            self.validated_path if verified else self.new_data_path,
            fruit_class.lower()
        )
        os.makedirs(class_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        ext = os.path.splitext(image_path)[1]
        new_filename = f"{fruit_class.lower()}_{timestamp}{ext}"
        new_path = os.path.join(class_dir, new_filename)
        
        # Copy image
        shutil.copy2(image_path, new_path)
        
        # Save metadata
        meta = {
            'original_path': image_path,
            'fruit_class': fruit_class,
            'verified': verified,
            'added_at': datetime.now().isoformat(),
            **(metadata or {})
        }
        
        meta_path = new_path + '.json'
        with open(meta_path, 'w') as f:
            json.dump(meta, f, indent=2)
        
        return {
            'success': True,
            'message': 'Sample added successfully',
            'sample_id': new_filename,
            'class': fruit_class,
            'verified': verified,
            'path': new_path
        }
    
    def verify_sample(
        self,
        sample_id: str,
        correct_class: str
    ) -> Dict[str, Any]:
        """
        Verify and potentially correct a sample's class.
        
        Args:
            sample_id: Sample identifier
            correct_class: Verified correct class
        
        Returns:
            Verification result
        """
        # Search for sample in new_data_path
        for root, dirs, files in os.walk(self.new_data_path):
            for file in files:
                if file == sample_id:
                    old_path = os.path.join(root, file)
                    
                    # Move to validated directory with correct class
                    new_class_dir = os.path.join(self.validated_path, correct_class.lower())
                    os.makedirs(new_class_dir, exist_ok=True)
                    new_path = os.path.join(new_class_dir, file)
                    
                    shutil.move(old_path, new_path)
                    
                    # Update metadata
                    old_meta = old_path + '.json'
                    new_meta = new_path + '.json'
                    if os.path.exists(old_meta):
                        with open(old_meta, 'r') as f:
                            meta = json.load(f)
                        meta['verified'] = True
                        meta['verified_class'] = correct_class
                        meta['verified_at'] = datetime.now().isoformat()
                        with open(new_meta, 'w') as f:
                            json.dump(meta, f, indent=2)
                        os.remove(old_meta)
                    
                    return {
                        'success': True,
                        'message': 'Sample verified and moved to training set',
                        'sample_id': sample_id,
                        'class': correct_class
                    }
        
        return {'success': False, 'error': 'Sample not found'}
    
    def get_training_data_stats(self) -> Dict[str, Any]:
        """
        Get statistics about available training data.
        
        Returns:
            Training data statistics
        """
        stats = {
            'validated_samples': {},
            'unverified_samples': {},
            'total_validated': 0,
            'total_unverified': 0,
            'classes': [],
            'ready_for_training': False
        }
        
        # Count validated samples
        if os.path.exists(self.validated_path):
            for class_dir in os.listdir(self.validated_path):
                class_path = os.path.join(self.validated_path, class_dir)
                if os.path.isdir(class_path):
                    count = len([f for f in os.listdir(class_path) if not f.endswith('.json')])
                    stats['validated_samples'][class_dir] = count
                    stats['total_validated'] += count
                    if class_dir not in stats['classes']:
                        stats['classes'].append(class_dir)
        
        # Count unverified samples
        if os.path.exists(self.new_data_path):
            for class_dir in os.listdir(self.new_data_path):
                class_path = os.path.join(self.new_data_path, class_dir)
                if os.path.isdir(class_path):
                    count = len([f for f in os.listdir(class_path) if not f.endswith('.json')])
                    stats['unverified_samples'][class_dir] = count
                    stats['total_unverified'] += count
        
        # Check if ready for training
        min_samples = self.config['min_samples_per_class']
        stats['ready_for_training'] = (
            len(stats['validated_samples']) >= 2 and
            all(count >= min_samples for count in stats['validated_samples'].values())
        )
        
        stats['min_samples_required'] = min_samples
        stats['classes_count'] = len(stats['classes'])
        
        return stats
    
    def prepare_dataset(
        self,
        augment: bool = True
    ) -> Dict[str, Any]:
        """
        Prepare dataset for training with optional augmentation.
        
        Args:
            augment: Whether to apply data augmentation
        
        Returns:
            Dataset preparation result
        """
        if not self._tf_available:
            return {
                'success': False,
                'error': 'TensorFlow required for dataset preparation',
                'install': 'pip install tensorflow'
            }
        
        stats = self.get_training_data_stats()
        if not stats['ready_for_training']:
            return {
                'success': False,
                'error': 'Insufficient training data',
                'stats': stats
            }
        
        try:
            from tensorflow.keras.preprocessing.image import ImageDataGenerator
            
            # Define augmentation
            if augment:
                train_datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=20,
                    width_shift_range=0.2,
                    height_shift_range=0.2,
                    shear_range=0.2,
                    zoom_range=0.2,
                    horizontal_flip=True,
                    fill_mode='nearest',
                    validation_split=self.config['validation_split']
                )
            else:
                train_datagen = ImageDataGenerator(
                    rescale=1./255,
                    validation_split=self.config['validation_split']
                )
            
            # Create generators
            train_generator = train_datagen.flow_from_directory(
                self.validated_path,
                target_size=self.config['image_size'],
                batch_size=self.config['batch_size'],
                class_mode='categorical',
                subset='training'
            )
            
            validation_generator = train_datagen.flow_from_directory(
                self.validated_path,
                target_size=self.config['image_size'],
                batch_size=self.config['batch_size'],
                class_mode='categorical',
                subset='validation'
            )
            
            return {
                'success': True,
                'train_generator': train_generator,
                'validation_generator': validation_generator,
                'classes': list(train_generator.class_indices.keys()),
                'num_classes': len(train_generator.class_indices),
                'train_samples': train_generator.n,
                'validation_samples': validation_generator.n,
                'augmentation_enabled': augment
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_model(
        self,
        num_classes: int,
        base_model: str = 'MobileNetV2'
    ) -> Dict[str, Any]:
        """
        Create a new model for training using transfer learning.
        
        Args:
            num_classes: Number of fruit classes
            base_model: Base model architecture
        
        Returns:
            Created model
        """
        if not self._tf_available:
            return {
                'success': False,
                'error': 'TensorFlow required',
                'install': 'pip install tensorflow'
            }
        
        try:
            import tensorflow as tf
            from tensorflow.keras import layers, models
            from tensorflow.keras.applications import MobileNetV2, ResNet50, EfficientNetB0
            
            input_shape = (*self.config['image_size'], 3)
            
            # Select base model
            base_models = {
                'MobileNetV2': MobileNetV2,
                'ResNet50': ResNet50,
                'EfficientNetB0': EfficientNetB0
            }
            
            if base_model not in base_models:
                base_model = 'MobileNetV2'
            
            # Create base model
            base = base_models[base_model](
                weights='imagenet',
                include_top=False,
                input_shape=input_shape
            )
            
            # Freeze base layers
            base.trainable = False
            
            # Build model
            model = models.Sequential([
                base,
                layers.GlobalAveragePooling2D(),
                layers.Dropout(0.3),
                layers.Dense(256, activation='relu'),
                layers.Dropout(0.3),
                layers.Dense(num_classes, activation='softmax')
            ])
            
            # Compile
            model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=self.config['learning_rate']),
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            return {
                'success': True,
                'model': model,
                'base_model': base_model,
                'num_classes': num_classes,
                'trainable_params': sum([tf.keras.backend.count_params(w) for w in model.trainable_weights]),
                'total_params': sum([tf.keras.backend.count_params(w) for w in model.weights])
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def train_model(
        self,
        model,
        train_generator,
        validation_generator,
        epochs: int = None
    ) -> Dict[str, Any]:
        """
        Train the model on prepared data.
        
        Args:
            model: Keras model to train
            train_generator: Training data generator
            validation_generator: Validation data generator
            epochs: Number of training epochs
        
        Returns:
            Training results
        """
        if not self._tf_available:
            return {'success': False, 'error': 'TensorFlow required'}
        
        epochs = epochs or self.config['epochs']
        
        try:
            import tensorflow as tf
            
            # Callbacks
            callbacks = [
                tf.keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=3,
                    restore_best_weights=True
                ),
                tf.keras.callbacks.ReduceLROnPlateau(
                    monitor='val_loss',
                    factor=0.5,
                    patience=2
                )
            ]
            
            # Train
            history = model.fit(
                train_generator,
                epochs=epochs,
                validation_data=validation_generator,
                callbacks=callbacks,
                verbose=1
            )
            
            # Get final metrics
            final_train_acc = history.history['accuracy'][-1]
            final_val_acc = history.history['val_accuracy'][-1]
            final_train_loss = history.history['loss'][-1]
            final_val_loss = history.history['val_loss'][-1]
            
            return {
                'success': True,
                'epochs_completed': len(history.history['loss']),
                'final_train_accuracy': round(final_train_acc, 4),
                'final_val_accuracy': round(final_val_acc, 4),
                'final_train_loss': round(final_train_loss, 4),
                'final_val_loss': round(final_val_loss, 4),
                'history': {
                    'accuracy': [round(x, 4) for x in history.history['accuracy']],
                    'val_accuracy': [round(x, 4) for x in history.history['val_accuracy']],
                    'loss': [round(x, 4) for x in history.history['loss']],
                    'val_loss': [round(x, 4) for x in history.history['val_loss']]
                },
                'model': model
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def save_model(
        self,
        model,
        version: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Save trained model with versioning.
        
        Args:
            model: Trained Keras model
            version: Version string (auto-generated if None)
            metadata: Training metadata to save
        
        Returns:
            Save result
        """
        if version is None:
            version = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        version_dir = os.path.join(self.model_history_path, version)
        os.makedirs(version_dir, exist_ok=True)
        
        model_path = os.path.join(version_dir, 'model.h5')
        
        try:
            model.save(model_path)
            
            # Save metadata
            meta = {
                'version': version,
                'saved_at': datetime.now().isoformat(),
                'model_path': model_path,
                **(metadata or {})
            }
            
            meta_path = os.path.join(version_dir, 'metadata.json')
            with open(meta_path, 'w') as f:
                json.dump(meta, f, indent=2)
            
            return {
                'success': True,
                'version': version,
                'model_path': model_path,
                'metadata_path': meta_path
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def load_model(self, version: str) -> Dict[str, Any]:
        """
        Load a specific model version.
        
        Args:
            version: Version string
        
        Returns:
            Loaded model and metadata
        """
        if not self._tf_available:
            return {'success': False, 'error': 'TensorFlow required'}
        
        version_dir = os.path.join(self.model_history_path, version)
        model_path = os.path.join(version_dir, 'model.h5')
        meta_path = os.path.join(version_dir, 'metadata.json')
        
        if not os.path.exists(model_path):
            return {'success': False, 'error': f'Model version {version} not found'}
        
        try:
            import tensorflow as tf
            
            model = tf.keras.models.load_model(model_path)
            
            metadata = {}
            if os.path.exists(meta_path):
                with open(meta_path, 'r') as f:
                    metadata = json.load(f)
            
            return {
                'success': True,
                'model': model,
                'version': version,
                'metadata': metadata
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def list_model_versions(self) -> List[Dict[str, Any]]:
        """List all saved model versions"""
        versions = []
        
        if os.path.exists(self.model_history_path):
            for version in sorted(os.listdir(self.model_history_path), reverse=True):
                version_dir = os.path.join(self.model_history_path, version)
                if os.path.isdir(version_dir):
                    meta_path = os.path.join(version_dir, 'metadata.json')
                    metadata = {}
                    if os.path.exists(meta_path):
                        try:
                            with open(meta_path, 'r') as f:
                                metadata = json.load(f)
                        except:
                            pass
                    
                    versions.append({
                        'version': version,
                        'path': version_dir,
                        'metadata': metadata
                    })
        
        return versions
    
    def compare_models(
        self,
        version1: str,
        version2: str,
        test_data=None
    ) -> Dict[str, Any]:
        """
        Compare two model versions.
        
        Args:
            version1: First model version
            version2: Second model version
            test_data: Optional test data for evaluation
        
        Returns:
            Comparison results
        """
        model1_result = self.load_model(version1)
        model2_result = self.load_model(version2)
        
        if not model1_result['success']:
            return {'success': False, 'error': f'Cannot load {version1}: {model1_result.get("error")}'}
        if not model2_result['success']:
            return {'success': False, 'error': f'Cannot load {version2}: {model2_result.get("error")}'}
        
        comparison = {
            'version1': {
                'version': version1,
                'metadata': model1_result.get('metadata', {})
            },
            'version2': {
                'version': version2,
                'metadata': model2_result.get('metadata', {})
            }
        }
        
        # Compare training metrics if available
        meta1 = model1_result.get('metadata', {})
        meta2 = model2_result.get('metadata', {})
        
        if 'final_val_accuracy' in meta1 and 'final_val_accuracy' in meta2:
            comparison['accuracy_comparison'] = {
                'version1_accuracy': meta1['final_val_accuracy'],
                'version2_accuracy': meta2['final_val_accuracy'],
                'improvement': meta2['final_val_accuracy'] - meta1['final_val_accuracy']
            }
        
        return {
            'success': True,
            'comparison': comparison
        }
    
    def get_retraining_status(self) -> Dict[str, Any]:
        """Get overall retraining system status"""
        stats = self.get_training_data_stats()
        versions = self.list_model_versions()
        
        return {
            'tensorflow_available': self._tf_available,
            'data_stats': stats,
            'model_versions': len(versions),
            'latest_version': versions[0]['version'] if versions else None,
            'config': self.config,
            'paths': {
                'base': self.base_path,
                'new_data': self.new_data_path,
                'validated': self.validated_path,
                'models': self.model_history_path
            }
        }
    
    def run_full_retraining(
        self,
        base_model: str = 'MobileNetV2',
        epochs: int = None
    ) -> Dict[str, Any]:
        """
        Run complete retraining pipeline.
        
        Args:
            base_model: Base model architecture
            epochs: Training epochs
        
        Returns:
            Complete retraining results
        """
        results = {'steps': []}
        
        # Step 1: Prepare dataset
        dataset_result = self.prepare_dataset()
        results['steps'].append({'step': 'prepare_dataset', 'result': 'success' if dataset_result['success'] else 'failed'})
        
        if not dataset_result['success']:
            results['success'] = False
            results['error'] = dataset_result.get('error')
            return results
        
        # Step 2: Create model
        num_classes = dataset_result['num_classes']
        model_result = self.create_model(num_classes, base_model)
        results['steps'].append({'step': 'create_model', 'result': 'success' if model_result['success'] else 'failed'})
        
        if not model_result['success']:
            results['success'] = False
            results['error'] = model_result.get('error')
            return results
        
        # Step 3: Train
        train_result = self.train_model(
            model_result['model'],
            dataset_result['train_generator'],
            dataset_result['validation_generator'],
            epochs
        )
        results['steps'].append({'step': 'train', 'result': 'success' if train_result['success'] else 'failed'})
        
        if not train_result['success']:
            results['success'] = False
            results['error'] = train_result.get('error')
            return results
        
        # Step 4: Save
        save_result = self.save_model(
            train_result['model'],
            metadata={
                'base_model': base_model,
                'num_classes': num_classes,
                'classes': dataset_result['classes'],
                'final_train_accuracy': train_result['final_train_accuracy'],
                'final_val_accuracy': train_result['final_val_accuracy']
            }
        )
        results['steps'].append({'step': 'save', 'result': 'success' if save_result['success'] else 'failed'})
        
        results['success'] = True
        results['version'] = save_result.get('version')
        results['training_metrics'] = {
            'accuracy': train_result['final_val_accuracy'],
            'loss': train_result['final_val_loss']
        }
        
        return results
