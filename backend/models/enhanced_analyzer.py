"""
Enhanced Fruit Analyzer
Comprehensive analysis including classification, ripeness, quality, size, and defect detection
Uses OpenAI Vision API for advanced image analysis
"""
import base64
import json
import os
from openai import OpenAI
from backend.config import Config
from backend.models.nutrition_database import get_nutrition_info
from backend.models.multilingual import translate_result, get_fruit_name


class EnhancedFruitAnalyzer:
    """
    Enhanced fruit analyzer that provides:
    - Fruit classification
    - Ripeness detection (unripe, ripe, overripe)
    - Quality assessment (healthy vs defective)
    - Defect detection (bruises, rot, blemishes)
    - Size estimation and grading
    - Nutritional information
    - Multilingual support
    """
    
    def __init__(self, api_key=None, model=None):
        """
        Initialize the enhanced fruit analyzer
        
        Args:
            api_key: OpenAI API key (defaults to Config.OPENAI_API_KEY)
            model: Model to use (defaults to Config.OPENAI_MODEL)
        """
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model = model or Config.OPENAI_MODEL
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in .env file")
        
        self.client = OpenAI(api_key=self.api_key)
        self.fruit_classes = Config.FRUIT_CLASSES
    
    def encode_image(self, image_path):
        """Encode image to base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze(self, image_path, language='en', include_nutrition=True):
        """
        Perform comprehensive fruit analysis
        
        Args:
            image_path: Path to the image file
            language: Language code for translations (default: 'en')
            include_nutrition: Whether to include nutritional info (default: True)
            
        Returns:
            Dictionary with comprehensive analysis results
        """
        try:
            # Encode image
            base64_image = self.encode_image(image_path)
            
            # Prepare comprehensive prompt
            fruit_list = ", ".join(self.fruit_classes)
            prompt = f"""You are an expert fruit analyst with deep knowledge of agriculture, food science, and quality control.
Analyze this fruit image comprehensively and provide detailed information.

Available fruit categories: {fruit_list}

Provide your response in the following JSON format:
{{
    "classification": {{
        "predicted_class": "FruitName",
        "confidence": 0.95,
        "top_3_predictions": [
            {{"class": "FruitName1", "confidence": 0.95}},
            {{"class": "FruitName2", "confidence": 0.03}},
            {{"class": "FruitName3", "confidence": 0.02}}
        ]
    }},
    "ripeness": {{
        "status": "ripe",
        "confidence": 0.90,
        "description": "The fruit appears to be at optimal ripeness based on color and texture",
        "days_until_overripe": 3
    }},
    "quality": {{
        "overall_status": "healthy",
        "quality_score": 85,
        "is_edible": true,
        "defects_detected": [],
        "description": "The fruit appears healthy with no visible defects"
    }},
    "size_grading": {{
        "estimated_size": "medium",
        "relative_scale": 0.7,
        "grade": "A",
        "suitable_for": ["retail", "export"]
    }},
    "visual_analysis": {{
        "dominant_color": "red",
        "texture": "smooth",
        "shape": "round",
        "surface_condition": "clean"
    }},
    "recommendations": {{
        "storage": "Refrigerate at 4°C for best freshness",
        "consumption_window": "Best consumed within 3-5 days",
        "handling": "Handle gently to prevent bruising"
    }}
}}

Ripeness status options: "unripe", "ripe", "overripe"
Quality status options: "healthy", "minor_defects", "defective", "spoiled"
Size options: "small", "medium", "large", "extra_large"
Grade options: "A" (premium), "B" (standard), "C" (economy)

Defect types to check for: bruises, rot, mold, discoloration, cuts, blemishes, deformity, pest_damage

Rules:
1. The predicted_class MUST be one of the available categories
2. Confidence values should be between 0 and 1
3. Quality score should be 0-100
4. Be specific about any defects detected
5. Consider ripeness based on color, texture, and typical fruit characteristics
6. Only respond with valid JSON, no additional text"""

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.2
            )
            
            # Parse response
            result_text = response.choices[0].message.content.strip()
            
            # Clean JSON
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            # Parse JSON
            analysis = json.loads(result_text)
            
            # Build response
            result = self._build_response(analysis, language, include_nutrition)
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            return self._get_fallback_response(language)
        except Exception as e:
            print(f"Analysis error: {e}")
            raise Exception(f"Failed to analyze image: {str(e)}")
    
    def _build_response(self, analysis, language, include_nutrition):
        """Build comprehensive response from analysis"""
        classification = analysis.get('classification', {})
        ripeness = analysis.get('ripeness', {})
        quality = analysis.get('quality', {})
        size_grading = analysis.get('size_grading', {})
        visual = analysis.get('visual_analysis', {})
        recommendations = analysis.get('recommendations', {})
        
        predicted_class = classification.get('predicted_class', self.fruit_classes[0])
        
        # Validate fruit class
        if predicted_class not in self.fruit_classes:
            for fruit in self.fruit_classes:
                if fruit.lower() in predicted_class.lower():
                    predicted_class = fruit
                    break
            else:
                predicted_class = self.fruit_classes[0]
        
        result = {
            # Classification
            'predicted_class': predicted_class,
            'predicted_class_translated': get_fruit_name(predicted_class, language),
            'confidence': classification.get('confidence', 0.8),
            'top_3_predictions': classification.get('top_3_predictions', []),
            
            # Ripeness
            'ripeness': ripeness.get('status', 'ripe'),
            'ripeness_confidence': ripeness.get('confidence', 0.8),
            'ripeness_description': ripeness.get('description', ''),
            'days_until_overripe': ripeness.get('days_until_overripe'),
            
            # Quality
            'quality_status': quality.get('overall_status', 'healthy'),
            'quality_score': quality.get('quality_score', 80),
            'is_edible': quality.get('is_edible', True),
            'defects_detected': quality.get('defects_detected', []),
            'quality_description': quality.get('description', ''),
            
            # Size & Grading
            'size_grade': size_grading.get('estimated_size', 'medium'),
            'size_scale': size_grading.get('relative_scale', 0.5),
            'quality_grade': size_grading.get('grade', 'B'),
            'suitable_for': size_grading.get('suitable_for', ['retail']),
            
            # Visual Analysis
            'dominant_color': visual.get('dominant_color', ''),
            'texture': visual.get('texture', ''),
            'shape': visual.get('shape', ''),
            'surface_condition': visual.get('surface_condition', ''),
            
            # Recommendations
            'storage_recommendation': recommendations.get('storage', ''),
            'consumption_window': recommendations.get('consumption_window', ''),
            'handling_tips': recommendations.get('handling', '')
        }
        
        # Add nutritional info
        if include_nutrition:
            nutrition = get_nutrition_info(predicted_class)
            if nutrition:
                result['nutrition'] = {
                    'calories': nutrition['calories'],
                    'carbohydrates': nutrition['carbohydrates'],
                    'fiber': nutrition['fiber'],
                    'sugar': nutrition['sugar'],
                    'protein': nutrition['protein'],
                    'fat': nutrition['fat'],
                    'vitamins': nutrition['vitamins'],
                    'minerals': nutrition['minerals'],
                    'health_benefits': nutrition['health_benefits']
                }
        
        # Apply translations
        result = translate_result(result, language)
        
        return result
    
    def _get_fallback_response(self, language='en'):
        """Return fallback response on error"""
        return {
            'predicted_class': self.fruit_classes[0],
            'predicted_class_translated': get_fruit_name(self.fruit_classes[0], language),
            'confidence': 0.5,
            'top_3_predictions': [
                {'class': self.fruit_classes[0], 'confidence': 0.5},
                {'class': self.fruit_classes[1], 'confidence': 0.3},
                {'class': self.fruit_classes[2], 'confidence': 0.2}
            ],
            'ripeness': 'ripe',
            'ripeness_confidence': 0.5,
            'ripeness_description': 'Unable to determine ripeness accurately',
            'quality_status': 'healthy',
            'quality_score': 50,
            'is_edible': True,
            'defects_detected': [],
            'size_grade': 'medium',
            'quality_grade': 'B',
            'error': 'Analysis completed with reduced accuracy'
        }
    
    def quick_classify(self, image_path):
        """
        Quick classification without full analysis
        For backward compatibility
        """
        result = self.analyze(image_path, include_nutrition=False)
        return {
            'predicted_class': result['predicted_class'],
            'confidence': result['confidence'],
            'top_3_predictions': result['top_3_predictions'],
            'all_predictions': {p['class']: p['confidence'] for p in result['top_3_predictions']}
        }


# Convenience function for backward compatibility
def create_analyzer():
    """Create and return an enhanced fruit analyzer"""
    return EnhancedFruitAnalyzer()
