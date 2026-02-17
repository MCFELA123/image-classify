"""
Explainable AI Module
Implements Grad-CAM and other visualization techniques to explain model predictions.
Highlights image regions that influenced the classification decision.
"""
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import base64
import io
from datetime import datetime


class ExplainableAI:
    """
    Provides explainability features for AI predictions.
    Implements Grad-CAM visualization and attention analysis.
    """
    
    def __init__(self):
        """Initialize explainable AI module"""
        self._tf_available = self._check_tensorflow()
        self._cv2_available = self._check_opencv()
        self._matplotlib_available = self._check_matplotlib()
    
    def _check_tensorflow(self) -> bool:
        """Check if TensorFlow is available"""
        try:
            import tensorflow as tf
            return True
        except ImportError:
            return False
    
    def _check_opencv(self) -> bool:
        """Check if OpenCV is available"""
        try:
            import cv2
            return True
        except ImportError:
            return False
    
    def _check_matplotlib(self) -> bool:
        """Check if Matplotlib is available"""
        try:
            import matplotlib.pyplot as plt
            return True
        except ImportError:
            return False
    
    def generate_gradcam(
        self,
        model,
        image_path: str,
        target_class: Optional[int] = None,
        layer_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate Grad-CAM visualization for a prediction.
        
        Args:
            model: Trained Keras/TensorFlow model
            image_path: Path to input image
            target_class: Target class index (None = predicted class)
            layer_name: Target layer for gradients (None = last conv layer)
        
        Returns:
            Grad-CAM visualization result
        """
        if not self._tf_available:
            return self._generate_fallback_explanation(image_path)
        
        try:
            import tensorflow as tf
            from tensorflow.keras.preprocessing import image as keras_image
            
            # Load and preprocess image
            img = keras_image.load_img(image_path, target_size=(224, 224))
            img_array = keras_image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0
            
            # Find last convolutional layer if not specified
            if layer_name is None:
                for layer in reversed(model.layers):
                    if 'conv' in layer.name.lower():
                        layer_name = layer.name
                        break
            
            if layer_name is None:
                return {'error': 'No convolutional layer found in model'}
            
            # Create gradient model
            grad_model = tf.keras.models.Model(
                [model.inputs],
                [model.get_layer(layer_name).output, model.output]
            )
            
            # Compute gradients
            with tf.GradientTape() as tape:
                conv_outputs, predictions = grad_model(img_array)
                if target_class is None:
                    target_class = tf.argmax(predictions[0])
                loss = predictions[:, target_class]
            
            # Get gradients of the loss with respect to conv layer output
            grads = tape.gradient(loss, conv_outputs)
            
            # Global average pooling of gradients
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
            
            # Weight output feature map with gradients
            conv_outputs = conv_outputs[0]
            heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
            heatmap = tf.squeeze(heatmap)
            
            # Normalize heatmap
            heatmap = tf.maximum(heatmap, 0) / tf.maximum(tf.reduce_max(heatmap), 1e-10)
            heatmap = heatmap.numpy()
            
            # Generate visualization
            visualization = self._create_heatmap_overlay(image_path, heatmap)
            
            return {
                'success': True,
                'method': 'grad-cam',
                'target_layer': layer_name,
                'target_class': int(target_class),
                'heatmap': visualization['heatmap_base64'],
                'overlay': visualization['overlay_base64'],
                'attention_regions': self._identify_attention_regions(heatmap),
                'explanation': self._generate_text_explanation(heatmap),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'fallback': self._generate_fallback_explanation(image_path)
            }
    
    def _create_heatmap_overlay(
        self,
        image_path: str,
        heatmap: np.ndarray
    ) -> Dict[str, str]:
        """Create heatmap overlay visualization"""
        if not self._cv2_available or not self._matplotlib_available:
            return {
                'heatmap_base64': None,
                'overlay_base64': None,
                'note': 'Install opencv-python and matplotlib for visualizations'
            }
        
        try:
            import cv2
            import matplotlib.pyplot as plt
            from matplotlib import cm
            
            # Load original image
            original = cv2.imread(image_path)
            original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
            original = cv2.resize(original, (224, 224))
            
            # Resize heatmap to match image
            heatmap_resized = cv2.resize(heatmap, (224, 224))
            
            # Create colored heatmap
            heatmap_colored = cm.jet(heatmap_resized)[:, :, :3]
            heatmap_colored = (heatmap_colored * 255).astype(np.uint8)
            
            # Create overlay
            overlay = (heatmap_colored * 0.4 + original * 0.6).astype(np.uint8)
            
            # Convert to base64
            heatmap_base64 = self._array_to_base64(heatmap_colored)
            overlay_base64 = self._array_to_base64(overlay)
            
            return {
                'heatmap_base64': heatmap_base64,
                'overlay_base64': overlay_base64
            }
            
        except Exception as e:
            return {
                'heatmap_base64': None,
                'overlay_base64': None,
                'error': str(e)
            }
    
    def _array_to_base64(self, img_array: np.ndarray) -> str:
        """Convert numpy array to base64 encoded PNG"""
        try:
            from PIL import Image
            
            img = Image.fromarray(img_array.astype(np.uint8))
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
        except:
            return None
    
    def _identify_attention_regions(self, heatmap: np.ndarray) -> List[Dict[str, Any]]:
        """Identify high-attention regions in heatmap"""
        regions = []
        
        # Find threshold for high attention
        threshold = 0.5
        high_attention = heatmap >= threshold
        
        # Calculate region statistics
        if np.any(high_attention):
            rows, cols = np.where(high_attention)
            if len(rows) > 0:
                center_y = int(np.mean(rows) / heatmap.shape[0] * 100)
                center_x = int(np.mean(cols) / heatmap.shape[1] * 100)
                coverage = np.sum(high_attention) / heatmap.size * 100
                
                regions.append({
                    'type': 'primary_focus',
                    'center': {'x': center_x, 'y': center_y},
                    'coverage_percentage': round(coverage, 1),
                    'intensity': round(float(np.max(heatmap)), 3)
                })
        
        return regions
    
    def _generate_text_explanation(self, heatmap: np.ndarray) -> str:
        """Generate human-readable explanation of attention pattern"""
        max_attention = float(np.max(heatmap))
        coverage = np.sum(heatmap >= 0.5) / heatmap.size * 100
        
        # Determine focus pattern
        if coverage < 10:
            pattern = "highly focused on a specific region"
        elif coverage < 30:
            pattern = "concentrated on a moderate area"
        else:
            pattern = "distributed across multiple regions"
        
        # Determine confidence indicator
        if max_attention > 0.8:
            confidence = "The model shows high confidence in this classification"
        elif max_attention > 0.5:
            confidence = "The model shows moderate confidence"
        else:
            confidence = "The model shows some uncertainty"
        
        return (
            f"The classification decision was {pattern}. "
            f"{confidence}, with the highlighted areas indicating "
            f"the image features that most influenced the prediction."
        )
    
    def _generate_fallback_explanation(self, image_path: str) -> Dict[str, Any]:
        """Generate fallback explanation when Grad-CAM unavailable"""
        return {
            'success': True,
            'method': 'text_explanation',
            'note': 'Grad-CAM visualization requires TensorFlow and OpenCV',
            'install_instructions': [
                'pip install tensorflow',
                'pip install opencv-python',
                'pip install matplotlib'
            ],
            'explanation': {
                'general': (
                    "The AI model analyzes various visual features of the fruit "
                    "to make its classification decision."
                ),
                'features_analyzed': [
                    'Color and color distribution',
                    'Shape and contour',
                    'Size estimation',
                    'Surface texture and patterns',
                    'Visible defects or blemishes',
                    'Ripeness indicators'
                ],
                'typical_focus_areas': [
                    'Overall fruit shape',
                    'Skin color and uniformity',
                    'Surface texture',
                    'Stem and calyx area (if visible)',
                    'Any spots or discoloration'
                ]
            }
        }
    
    def analyze_prediction_confidence(
        self,
        predictions: List[Dict[str, Any]],
        threshold: float = 0.5
    ) -> Dict[str, Any]:
        """
        Analyze prediction confidence and provide interpretation.
        
        Args:
            predictions: List of predictions with class and confidence
            threshold: Confidence threshold for reliable prediction
        
        Returns:
            Confidence analysis with interpretation
        """
        if not predictions:
            return {'error': 'No predictions provided'}
        
        top_pred = predictions[0]
        top_confidence = top_pred.get('confidence', 0)
        
        # Analyze confidence distribution
        confidences = [p.get('confidence', 0) for p in predictions]
        confidence_spread = max(confidences) - min(confidences) if len(confidences) > 1 else 1.0
        
        # Determine reliability
        if top_confidence >= 0.9:
            reliability = 'very_high'
            interpretation = 'The model is highly confident in this classification.'
        elif top_confidence >= 0.7:
            reliability = 'high'
            interpretation = 'The model is confident, but there is slight uncertainty.'
        elif top_confidence >= 0.5:
            reliability = 'moderate'
            interpretation = 'The model shows moderate confidence. Consider manual verification.'
        else:
            reliability = 'low'
            interpretation = 'The model is uncertain. Manual verification recommended.'
        
        # Check for close alternatives
        alternatives = []
        if len(predictions) > 1:
            for pred in predictions[1:3]:
                if pred.get('confidence', 0) > 0.2:
                    alternatives.append({
                        'class': pred['class'],
                        'confidence': pred['confidence'],
                        'difference_from_top': round(top_confidence - pred['confidence'], 3)
                    })
        
        return {
            'top_prediction': top_pred,
            'reliability': reliability,
            'interpretation': interpretation,
            'confidence_spread': round(confidence_spread, 3),
            'alternatives': alternatives,
            'recommendation': self._get_recommendation(reliability, alternatives),
            'factors_affecting_confidence': [
                'Image quality and lighting',
                'Angle and visibility of fruit',
                'Similarity to training data',
                'Presence of multiple fruits',
                'Background complexity'
            ]
        }
    
    def _get_recommendation(self, reliability: str, alternatives: List) -> str:
        """Get recommendation based on confidence analysis"""
        if reliability == 'very_high':
            return "Classification is reliable. No additional verification needed."
        elif reliability == 'high':
            return "Classification is likely correct. Quick visual check recommended."
        elif reliability == 'moderate':
            if alternatives:
                alt_classes = [a['class'] for a in alternatives]
                return f"Consider that this could also be: {', '.join(alt_classes)}. Manual verification advised."
            return "Manual verification recommended to confirm classification."
        else:
            return "Low confidence classification. Please verify manually or provide a better image."
    
    def explain_quality_assessment(
        self,
        quality_score: float,
        ripeness: str,
        defects: List[str],
        visual_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Explain quality assessment decision.
        
        Args:
            quality_score: Overall quality score (0-100)
            ripeness: Ripeness status
            defects: Detected defects
            visual_analysis: Visual analysis results
        
        Returns:
            Detailed explanation of quality assessment
        """
        factors = []
        
        # Explain quality score contributors
        if quality_score >= 90:
            factors.append({
                'factor': 'Overall Quality',
                'contribution': 'positive',
                'explanation': 'Excellent overall condition with minimal imperfections'
            })
        elif quality_score >= 70:
            factors.append({
                'factor': 'Overall Quality',
                'contribution': 'moderate',
                'explanation': 'Good condition with minor issues'
            })
        else:
            factors.append({
                'factor': 'Overall Quality',
                'contribution': 'negative',
                'explanation': 'Quality concerns detected'
            })
        
        # Explain ripeness impact
        ripeness_contrib = 'positive' if ripeness == 'ripe' else 'moderate' if ripeness == 'unripe' else 'negative'
        factors.append({
            'factor': 'Ripeness',
            'contribution': ripeness_contrib,
            'explanation': f'Fruit assessed as {ripeness}'
        })
        
        # Explain defects impact
        if defects:
            factors.append({
                'factor': 'Defects',
                'contribution': 'negative',
                'explanation': f'Detected issues: {", ".join(defects)}'
            })
        else:
            factors.append({
                'factor': 'Defects',
                'contribution': 'positive',
                'explanation': 'No significant defects detected'
            })
        
        # Visual analysis factors
        if visual_analysis:
            if visual_analysis.get('surface_condition') == 'good':
                factors.append({
                    'factor': 'Surface',
                    'contribution': 'positive',
                    'explanation': 'Surface appears smooth and healthy'
                })
        
        return {
            'quality_score': quality_score,
            'factors': factors,
            'summary': self._summarize_factors(factors),
            'improvement_suggestions': self._get_quality_suggestions(quality_score, defects)
        }
    
    def _summarize_factors(self, factors: List[Dict]) -> str:
        """Summarize factor contributions"""
        positive = sum(1 for f in factors if f['contribution'] == 'positive')
        negative = sum(1 for f in factors if f['contribution'] == 'negative')
        
        if positive > negative:
            return "The quality assessment is predominantly positive based on the analyzed factors."
        elif negative > positive:
            return "Several factors negatively impacted the quality assessment."
        else:
            return "The assessment shows mixed results across different quality factors."
    
    def _get_quality_suggestions(self, score: float, defects: List[str]) -> List[str]:
        """Get suggestions for quality improvement"""
        suggestions = []
        
        if score < 70:
            suggestions.append("Consider sorting for processing rather than fresh sale")
        
        if 'bruise' in str(defects).lower():
            suggestions.append("Improve handling to reduce bruising")
        
        if 'mold' in str(defects).lower() or 'rot' in str(defects).lower():
            suggestions.append("Check cold chain integrity")
            suggestions.append("Reduce storage time")
        
        if not suggestions:
            suggestions.append("Maintain current quality control practices")
        
        return suggestions
    
    def get_model_info(self, model=None) -> Dict[str, Any]:
        """Get model architecture information for explainability"""
        info = {
            'explainability_methods': ['grad-cam', 'text_explanation', 'confidence_analysis'],
            'visualization_available': self._tf_available and self._cv2_available,
            'dependencies': {
                'tensorflow': self._tf_available,
                'opencv': self._cv2_available,
                'matplotlib': self._matplotlib_available
            }
        }
        
        if model and self._tf_available:
            try:
                info['model_summary'] = {
                    'total_layers': len(model.layers),
                    'trainable_params': sum([np.prod(w.shape) for w in model.trainable_weights]),
                    'conv_layers': [l.name for l in model.layers if 'conv' in l.name.lower()]
                }
            except:
                pass
        
        return info
