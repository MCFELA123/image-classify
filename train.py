"""
Training script for the Fruit Classification Model
This script helps you train the model with your own dataset
"""
import os
import sys
from backend.models.fruit_classifier import FruitClassificationModel
from backend.config import Config


def train_model(train_data_dir, validation_data_dir=None, epochs=20, batch_size=32):
    """
    Train the fruit classification model
    
    Args:
        train_data_dir: Path to training data directory
        validation_data_dir: Path to validation data directory (optional)
        epochs: Number of training epochs
        batch_size: Batch size for training
    """
    print("🍎 Starting Fruit Classification Model Training...")
    print(f"Training data: {train_data_dir}")
    print(f"Epochs: {epochs}")
    print(f"Batch size: {batch_size}")
    print("-" * 50)
    
    # Check if training data exists
    if not os.path.exists(train_data_dir):
        print(f"❌ Error: Training data directory not found: {train_data_dir}")
        print("\nPlease organize your training data as follows:")
        print("training_data/")
        print("  ├── Apple/")
        print("  │   ├── image1.jpg")
        print("  │   ├── image2.jpg")
        print("  │   └── ...")
        print("  ├── Banana/")
        print("  │   └── ...")
        print("  └── ...")
        return
    
    # Initialize model
    model = FruitClassificationModel(
        num_classes=len(Config.FRUIT_CLASSES),
        image_size=Config.IMAGE_SIZE
    )
    
    # Build model
    print("\n🏗️  Building model architecture...")
    model.build_model()
    print(model.model.summary())
    
    # Train model
    print("\n🎯 Training model...")
    history = model.train_model(
        train_data_dir=train_data_dir,
        validation_data_dir=validation_data_dir,
        epochs=epochs,
        batch_size=batch_size
    )
    
    # Save model
    os.makedirs('trained_models', exist_ok=True)
    model_path = Config.MODEL_PATH
    print(f"\n💾 Saving model to {model_path}...")
    model.save_model(model_path)
    
    print("\n✅ Training completed successfully!")
    print(f"📊 Final training accuracy: {history.history['accuracy'][-1]:.4f}")
    print(f"📊 Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")
    
    return model, history


def create_demo_model():
    """
    Create a demo model structure (untrained)
    Useful for testing the API without training data
    """
    print("🍎 Creating demo model structure...")
    
    model = FruitClassificationModel(
        num_classes=len(Config.FRUIT_CLASSES),
        image_size=Config.IMAGE_SIZE
    )
    
    model.build_model()
    
    os.makedirs('trained_models', exist_ok=True)
    model_path = Config.MODEL_PATH
    model.save_model(model_path)
    
    print(f"✅ Demo model created at {model_path}")
    print("⚠️  Note: This is an untrained model. Train it with real data for accurate predictions.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train Fruit Classification Model')
    parser.add_argument('--train-dir', type=str, help='Path to training data directory')
    parser.add_argument('--val-dir', type=str, help='Path to validation data directory')
    parser.add_argument('--epochs', type=int, default=20, help='Number of epochs')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    parser.add_argument('--demo', action='store_true', help='Create demo model without training')
    
    args = parser.parse_args()
    
    if args.demo:
        create_demo_model()
    elif args.train_dir:
        train_model(
            train_data_dir=args.train_dir,
            validation_data_dir=args.val_dir,
            epochs=args.epochs,
            batch_size=args.batch_size
        )
    else:
        print("Usage:")
        print("  Create demo model:")
        print("    python train.py --demo")
        print("\n  Train with data:")
        print("    python train.py --train-dir path/to/training_data --epochs 20")
        print("\n  Train with validation data:")
        print("    python train.py --train-dir path/to/training_data --val-dir path/to/val_data")
