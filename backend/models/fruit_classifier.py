"""
CNN Model for Fruit Classification
Uses Transfer Learning with MobileNetV2
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os


class FruitClassificationModel:
    def __init__(self, num_classes=10, image_size=224):
        """
        Initialize the fruit classification model
        
        Args:
            num_classes: Number of fruit categories
            image_size: Input image size (default: 224x224)
        """
        self.num_classes = num_classes
        self.image_size = image_size
        self.model = None
        
    def build_model(self):
        """
        Build CNN model using Transfer Learning with MobileNetV2
        """
        # Load pre-trained MobileNetV2 without top layers
        base_model = MobileNetV2(
            input_shape=(self.image_size, self.image_size, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Build model
        self.model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile model
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return self.model
    
    def train_model(self, train_data_dir, validation_data_dir=None, epochs=20, batch_size=32):
        """
        Train the model on fruit images
        
        Args:
            train_data_dir: Directory containing training images
            validation_data_dir: Directory containing validation images
            epochs: Number of training epochs
            batch_size: Batch size for training
        """
        if self.model is None:
            self.build_model()
        
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest',
            validation_split=0.2 if validation_data_dir is None else 0.0
        )
        
        # Prepare training data
        train_generator = train_datagen.flow_from_directory(
            train_data_dir,
            target_size=(self.image_size, self.image_size),
            batch_size=batch_size,
            class_mode='categorical',
            subset='training' if validation_data_dir is None else None
        )
        
        # Prepare validation data
        if validation_data_dir:
            val_datagen = ImageDataGenerator(rescale=1./255)
            validation_generator = val_datagen.flow_from_directory(
                validation_data_dir,
                target_size=(self.image_size, self.image_size),
                batch_size=batch_size,
                class_mode='categorical'
            )
        else:
            validation_generator = train_datagen.flow_from_directory(
                train_data_dir,
                target_size=(self.image_size, self.image_size),
                batch_size=batch_size,
                class_mode='categorical',
                subset='validation'
            )
        
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-7
            )
        ]
        
        # Train model
        history = self.model.fit(
            train_generator,
            epochs=epochs,
            validation_data=validation_generator,
            callbacks=callbacks
        )
        
        return history
    
    def save_model(self, filepath):
        """Save the trained model"""
        if self.model:
            self.model.save(filepath)
            print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load a pre-trained model"""
        if os.path.exists(filepath):
            self.model = keras.models.load_model(filepath)
            print(f"Model loaded from {filepath}")
            return True
        return False
    
    def predict(self, image_array, class_names):
        """
        Predict fruit class for an image
        
        Args:
            image_array: Preprocessed image array
            class_names: List of class names
            
        Returns:
            Dictionary with prediction results
        """
        if self.model is None:
            raise ValueError("Model not loaded or built")
        
        # Ensure image has batch dimension
        if len(image_array.shape) == 3:
            image_array = np.expand_dims(image_array, axis=0)
        
        # Make prediction
        predictions = self.model.predict(image_array)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        # Get top 3 predictions
        top_3_idx = np.argsort(predictions[0])[-3:][::-1]
        top_3_predictions = [
            {
                'class': class_names[idx],
                'confidence': float(predictions[0][idx])
            }
            for idx in top_3_idx
        ]
        
        return {
            'predicted_class': class_names[predicted_class_idx],
            'confidence': confidence,
            'top_3_predictions': top_3_predictions,
            'all_predictions': {
                class_names[i]: float(predictions[0][i])
                for i in range(len(class_names))
            }
        }


def create_sample_model(output_path='trained_models/fruit_classifier.h5', num_classes=10):
    """
    Create and save a sample pre-trained model structure
    This is for demo purposes when you don't have training data yet
    """
    model = FruitClassificationModel(num_classes=num_classes)
    model.build_model()
    
    # Save the model structure
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    model.save_model(output_path)
    print(f"Sample model created and saved to {output_path}")
    print("Note: This model needs to be trained with actual fruit images for accurate predictions")
    
    return model


if __name__ == "__main__":
    # Create a sample model
    create_sample_model()
