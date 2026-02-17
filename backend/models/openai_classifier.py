"""
OpenAI-based Fruit Classification
Uses GPT-4 Vision to classify fruit images
"""
import base64
import os
from openai import OpenAI
from backend.config import Config


class OpenAIFruitClassifier:
    def __init__(self, api_key=None, model=None):
        """
        Initialize OpenAI fruit classifier
        
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
        """
        Encode image to base64
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Base64 encoded image string
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def predict(self, image_path):
        """
        Classify fruit image using OpenAI Vision API
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with prediction results
        """
        try:
            # Encode image
            base64_image = self.encode_image(image_path)
            
            # Prepare prompt
            fruit_list = ", ".join(self.fruit_classes)
            prompt = f"""You are a fruit classification expert. Analyze this image and identify the fruit.

Available fruit categories: {fruit_list}

Provide your response in the following JSON format:
{{
    "predicted_class": "FruitName",
    "confidence": 0.95,
    "top_3_predictions": [
        {{"class": "FruitName1", "confidence": 0.95}},
        {{"class": "FruitName2", "confidence": 0.03}},
        {{"class": "FruitName3", "confidence": 0.02}}
    ],
    "reasoning": "Brief explanation of why you identified this fruit"
}}

Rules:
1. The predicted_class MUST be one of the available categories listed above
2. Confidence values should be between 0 and 1
3. If you're not confident, give a lower confidence score
4. If the image doesn't contain a fruit or doesn't match any category, use the closest match with lower confidence
5. Only respond with valid JSON, no additional text"""

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.2
            )
            
            # Parse response
            result_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            # Parse JSON
            import json
            result = json.loads(result_text)
            
            # Validate and normalize the result
            predicted_class = result.get('predicted_class', 'Unknown')
            confidence = float(result.get('confidence', 0.5))
            top_3 = result.get('top_3_predictions', [])
            
            # Ensure predicted_class is in our fruit classes
            if predicted_class not in self.fruit_classes:
                # Try to find a close match
                predicted_class_lower = predicted_class.lower()
                for fruit in self.fruit_classes:
                    if fruit.lower() in predicted_class_lower or predicted_class_lower in fruit.lower():
                        predicted_class = fruit
                        break
                else:
                    # Default to first fruit if no match
                    predicted_class = self.fruit_classes[0]
                    confidence = 0.3
            
            # Normalize top_3 predictions
            if len(top_3) < 3:
                # Fill with remaining fruits
                existing_fruits = {p['class'] for p in top_3}
                for fruit in self.fruit_classes:
                    if fruit not in existing_fruits and len(top_3) < 3:
                        top_3.append({'class': fruit, 'confidence': 0.01})
            
            # Create all_predictions dictionary
            all_predictions = {}
            for pred in top_3:
                all_predictions[pred['class']] = pred['confidence']
            
            # Add remaining fruits with minimal confidence
            for fruit in self.fruit_classes:
                if fruit not in all_predictions:
                    all_predictions[fruit] = 0.001
            
            return {
                'predicted_class': predicted_class,
                'confidence': confidence,
                'top_3_predictions': top_3[:3],
                'all_predictions': all_predictions,
                'reasoning': result.get('reasoning', 'Classification completed')
            }
            
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            print(f"Response text: {result_text}")
            # Return a default response
            return {
                'predicted_class': self.fruit_classes[0],
                'confidence': 0.5,
                'top_3_predictions': [
                    {'class': self.fruit_classes[0], 'confidence': 0.5},
                    {'class': self.fruit_classes[1], 'confidence': 0.3},
                    {'class': self.fruit_classes[2], 'confidence': 0.2}
                ],
                'all_predictions': {fruit: 0.1 for fruit in self.fruit_classes},
                'reasoning': 'Error parsing AI response'
            }
        except Exception as e:
            print(f"Classification error: {e}")
            raise Exception(f"Failed to classify image: {str(e)}")
    
    def test_connection(self):
        """Test OpenAI API connection"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False


if __name__ == "__main__":
    # Test the classifier
    classifier = OpenAIFruitClassifier()
    print("✅ OpenAI Fruit Classifier initialized")
    print(f"Model: {classifier.model}")
    print(f"Available classes: {', '.join(classifier.fruit_classes)}")
    
    if classifier.test_connection():
        print("✅ OpenAI API connection successful")
    else:
        print("❌ OpenAI API connection failed")
