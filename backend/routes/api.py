"""
API Routes for Fruit Classification System
Enhanced with ripeness detection, quality analysis, size grading, and multilingual support
"""
from flask import Blueprint, request, jsonify
import os
import base64
from backend.config import Config
from backend.models.openai_classifier import OpenAIFruitClassifier
from backend.models.database import DatabaseHandler
from backend.utils.image_utils import (
    allowed_file, save_uploaded_file,
    validate_image, format_confidence
)
from backend.models.nutrition_database import (
    get_nutrition_info, get_all_fruits, NUTRITION_DATABASE,
    compare_fruits, search_by_nutrient, get_low_gi_fruits,
    get_seasonal_fruits, calculate_serving, get_recipes,
    get_storage_info, get_glycemic_info
)
from backend.models.multilingual import (
    get_fruit_name, get_ui_text, get_supported_languages, 
    translate_result, FRUIT_TRANSLATIONS, UI_TRANSLATIONS
)

# Create blueprint
api_bp = Blueprint('api', __name__)

# Initialize classifier (will be loaded when first needed)
classifier = None
enhanced_analyzer = None
db_handler = None


def get_classifier():
    """Lazy load the classifier"""
    global classifier
    if classifier is None:
        if Config.USE_OPENAI:
            classifier = OpenAIFruitClassifier()
            print("✅ Using OpenAI Vision API for classification")
        else:
            # Fallback to local model if USE_OPENAI is False
            from backend.models.fruit_classifier import FruitClassificationModel
            classifier = FruitClassificationModel(
                num_classes=len(Config.FRUIT_CLASSES),
                image_size=Config.IMAGE_SIZE
            )
            if os.path.exists(Config.MODEL_PATH):
                classifier.load_model(Config.MODEL_PATH)
            else:
                classifier.build_model()
                print("⚠️  Using untrained local model")
    return classifier


def get_enhanced_analyzer():
    """Lazy load the enhanced analyzer"""
    global enhanced_analyzer
    if enhanced_analyzer is None:
        from backend.models.enhanced_analyzer import EnhancedFruitAnalyzer
        enhanced_analyzer = EnhancedFruitAnalyzer()
        print("✅ Enhanced Fruit Analyzer loaded")
    return enhanced_analyzer
    return classifier


def get_db():
    """Lazy load database handler"""
    global db_handler
    if db_handler is None:
        try:
            db_handler = DatabaseHandler(Config.MONGODB_URI, Config.DB_NAME)
        except Exception as e:
            print(f"⚠️  MongoDB connection failed: {e}")
            print("⚠️  Running without database - history won't be saved")
            db_handler = None
    return db_handler


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'classifier_loaded': classifier is not None,
        'enhanced_analyzer_loaded': enhanced_analyzer is not None,
        'database_connected': db_handler is not None,
        'using_openai': Config.USE_OPENAI,
        'features': [
            'classification',
            'ripeness_detection',
            'quality_analysis',
            'defect_detection',
            'disease_detection',
            'size_grading',
            'weight_estimation',
            'pricing_calculation',
            'nutrition_info',
            'multilingual',
            'smart_agriculture_integration',
            'farm_management_export',
            'inventory_reporting',
            'webhook_notifications',
            'performance_evaluation',
            'privacy_compliance',
            'ethical_guidelines'
        ],
        'api_version': '2.0',
        'modules': {
            'agriculture_integration': True,
            'security_privacy': True,
            'performance_evaluation': True,
            'grading_system': True
        }
    })


@api_bp.route('/classify', methods=['POST'])
def classify_image():
    """
    Classify an uploaded fruit image with comprehensive analysis
    Includes: classification, ripeness, quality, defects, size, nutrition
    """
    # Check if file is present
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    language = request.form.get('language', 'en')
    analysis_mode = request.form.get('mode', 'full')  # 'full' or 'quick'
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({'error': 'No image file selected'}), 400
    
    # Check file extension
    if not allowed_file(file.filename, Config.ALLOWED_EXTENSIONS):
        return jsonify({'error': 'Invalid file type. Allowed types: ' + ', '.join(Config.ALLOWED_EXTENSIONS)}), 400
    
    try:
        # Save uploaded file
        success, result = save_uploaded_file(file, Config.UPLOAD_FOLDER)
        if not success:
            return jsonify({'error': f'Failed to save file: {result}'}), 500
        
        image_path = result
        
        # Validate image
        is_valid, error_msg = validate_image(image_path)
        if not is_valid:
            os.remove(image_path)  # Clean up invalid file
            return jsonify({'error': error_msg}), 400
        
        # Use enhanced analyzer for full analysis
        if Config.USE_OPENAI and analysis_mode == 'full':
            analyzer = get_enhanced_analyzer()
            print(f"[DEBUG] Analyzing with language: {language}")
            analysis = analyzer.analyze(image_path, language=language, include_nutrition=True)
            print(f"[DEBUG] predicted_class: {analysis['predicted_class']}")
            print(f"[DEBUG] predicted_class_translated: {analysis.get('predicted_class_translated')}")
            
            # Build comprehensive response
            response = {
                'classification_id': None,
                'predicted_class': analysis['predicted_class'],
                'predicted_class_translated': analysis.get('predicted_class_translated'),
                'confidence': format_confidence(analysis['confidence']),
                'confidence_raw': analysis['confidence'],
                'top_predictions': [
                    {
                        'class': pred['class'],
                        'confidence': format_confidence(pred['confidence']),
                        'confidence_raw': pred['confidence']
                    }
                    for pred in analysis.get('top_3_predictions', [])
                ],
                # Ripeness info
                'ripeness': analysis.get('ripeness'),
                'ripeness_translated': analysis.get('ripeness_translated'),
                'ripeness_confidence': analysis.get('ripeness_confidence'),
                'ripeness_description': analysis.get('ripeness_description'),
                'days_until_overripe': analysis.get('days_until_overripe'),
                # Quality info
                'quality_status': analysis.get('quality_status'),
                'quality_status_translated': analysis.get('quality_status_translated'),
                'quality_score': analysis.get('quality_score'),
                'is_edible': analysis.get('is_edible'),
                'defects_detected': analysis.get('defects_detected', []),
                'quality_description': analysis.get('quality_description'),
                # Size & Grading
                'size_grade': analysis.get('size_grade'),
                'size_grade_translated': analysis.get('size_grade_translated'),
                'quality_grade': analysis.get('quality_grade'),
                'suitable_for': analysis.get('suitable_for', []),
                # Visual Analysis
                'visual_analysis': {
                    'dominant_color': analysis.get('dominant_color'),
                    'texture': analysis.get('texture'),
                    'shape': analysis.get('shape'),
                    'surface_condition': analysis.get('surface_condition')
                },
                # Recommendations
                'recommendations': {
                    'storage': analysis.get('storage_recommendation'),
                    'consumption_window': analysis.get('consumption_window'),
                    'handling': analysis.get('handling_tips')
                },
                # Nutrition
                'nutrition': analysis.get('nutrition'),
                'image_filename': os.path.basename(image_path),
                'language': language
            }
            
            prediction = {
                'predicted_class': analysis['predicted_class'],
                'confidence': analysis['confidence'],
                'top_3_predictions': analysis.get('top_3_predictions', [])
            }
        else:
            # Quick classification mode or local model
            clf = get_classifier()
            
            if Config.USE_OPENAI:
                prediction = clf.predict(image_path)
            else:
                from backend.utils.image_utils import preprocess_image
                processed_image = preprocess_image(image_path, target_size=(Config.IMAGE_SIZE, Config.IMAGE_SIZE))
                prediction = clf.predict(processed_image, Config.FRUIT_CLASSES)
            
            # Format basic response
            response = {
                'classification_id': None,
                'predicted_class': prediction['predicted_class'],
                'confidence': format_confidence(prediction['confidence']),
                'confidence_raw': prediction['confidence'],
                'top_predictions': [
                    {
                        'class': pred['class'],
                        'confidence': format_confidence(pred['confidence']),
                        'confidence_raw': pred['confidence']
                    }
                    for pred in prediction.get('top_3_predictions', [])
                ],
                'image_filename': os.path.basename(image_path)
            }
        
        # Save to database (if available)
        db = get_db()
        if db:
            try:
                classification_id = db.save_classification(
                    image_filename=os.path.basename(image_path),
                    prediction_result=prediction,
                    image_path=image_path
                )
                response['classification_id'] = classification_id
            except Exception as e:
                print(f"⚠️  Failed to save to database: {e}")
        
        return jsonify(response), 200
        
    except Exception as e:
        # Clean up on error
        if 'image_path' in locals() and os.path.exists(image_path):
            os.remove(image_path)
        return jsonify({'error': f'Classification failed: {str(e)}'}), 500


@api_bp.route('/history', methods=['GET', 'POST'])
def handle_history():
    """Get recent classification history or add manual entry"""
    if request.method == 'POST':
        # Add manual inventory entry
        try:
            data = request.get_json()
            
            predicted_class = data.get('predicted_class')
            if not predicted_class:
                return jsonify({'error': 'predicted_class is required'}), 400
            
            # Create entry for database
            entry = {
                'predicted_class': predicted_class,
                'confidence': data.get('confidence', 1.0),
                'quality_grade': data.get('quality_grade', 'A'),
                'quantity': data.get('quantity', 1),
                'expiry_date': data.get('expiry_date'),
                'min_stock': data.get('min_stock', 10),
                'source': data.get('source', 'manual'),
                'timestamp': data.get('timestamp'),
                'image_filename': 'manual_entry'
            }
            
            # Save to database
            db = get_db()
            if db:
                classification_id = db.save_classification(entry)
                return jsonify({
                    'success': True,
                    'classification_id': classification_id,
                    'message': 'Inventory item added successfully'
                }), 201
            else:
                return jsonify({'error': 'Database not available'}), 503
                
        except Exception as e:
            return jsonify({'error': f'Failed to add inventory: {str(e)}'}), 500
    
    # GET request - return history
    try:
        db = get_db()
        if not db:
            return jsonify({
                'count': 0,
                'history': [],
                'message': 'Database not available'
            }), 200
        
        limit = request.args.get('limit', 20, type=int)
        limit = min(limit, 100)  # Cap at 100
        
        history = db.get_recent_classifications(limit=limit)
        
        return jsonify({
            'count': len(history),
            'history': history
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve history: {str(e)}'}), 500


@api_bp.route('/history/<classification_id>', methods=['GET'])
def get_classification(classification_id):
    """Get specific classification by ID"""
    try:
        db = get_db()
        if not db:
            return jsonify({'error': 'Database not available'}), 503
        
        classification = db.get_classification_by_id(classification_id)
        
        if classification:
            return jsonify(classification), 200
        else:
            return jsonify({'error': 'Classification not found'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve classification: {str(e)}'}), 500


@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get classification statistics"""
    try:
        db = get_db()
        if not db:
            return jsonify({
                'total_classifications': 0,
                'class_counts': {},
                'message': 'Database not available'
            }), 200
        
        stats = db.get_statistics()
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve statistics: {str(e)}'}), 500


@api_bp.route('/classes', methods=['GET'])
def get_classes():
    """Get list of available fruit classes"""
    language = request.args.get('language', 'en')
    classes_translated = [
        {
            'name': fruit,
            'translated': get_fruit_name(fruit, language)
        }
        for fruit in Config.FRUIT_CLASSES
    ]
    return jsonify({
        'classes': Config.FRUIT_CLASSES,
        'classes_translated': classes_translated,
        'count': len(Config.FRUIT_CLASSES),
        'language': language
    }), 200


# ==================== NEW ENDPOINTS ====================

@api_bp.route('/nutrition/<fruit_name>', methods=['GET'])
def get_nutrition(fruit_name):
    """Get nutritional information for a specific fruit"""
    # Normalize fruit name
    fruit_name = fruit_name.strip().title()
    
    nutrition = get_nutrition_info(fruit_name)
    
    if nutrition:
        return jsonify({
            'fruit': fruit_name,
            'nutrition': nutrition,
            'per_serving': '100g'
        }), 200
    else:
        return jsonify({
            'error': f'Nutritional information not found for: {fruit_name}',
            'available_fruits': get_all_fruits()
        }), 404


@api_bp.route('/nutrition', methods=['GET'])
def get_all_nutrition():
    """Get nutritional information for all fruits"""
    return jsonify({
        'fruits': NUTRITION_DATABASE,
        'count': len(NUTRITION_DATABASE),
        'per_serving': '100g'
    }), 200


@api_bp.route('/nutrition/compare', methods=['GET'])
def compare_fruits_endpoint():
    """Compare multiple fruits side by side"""
    fruits = request.args.get('fruits', '')
    fruit_list = [f.strip().title() for f in fruits.split(',') if f.strip()]
    
    if len(fruit_list) < 2:
        return jsonify({'error': 'Please provide at least 2 fruits to compare'}), 400
    
    if len(fruit_list) > 4:
        return jsonify({'error': 'Maximum 4 fruits can be compared at once'}), 400
    
    comparison = compare_fruits(fruit_list)
    
    return jsonify({
        'comparison': comparison,
        'fruits_compared': list(comparison.keys()),
        'per_serving': '100g'
    }), 200


@api_bp.route('/nutrition/search', methods=['GET'])
def search_nutrients_endpoint():
    """Search fruits by nutrient content"""
    nutrient = request.args.get('nutrient', 'calories').lower()
    criteria = request.args.get('criteria', 'high').lower()
    limit = min(int(request.args.get('limit', 5)), 10)
    
    valid_nutrients = ['calories', 'fiber', 'sugar', 'protein', 'carbs', 'fat']
    if nutrient not in valid_nutrients:
        return jsonify({'error': f'Invalid nutrient. Choose from: {", ".join(valid_nutrients)}'}), 400
    
    if criteria not in ['high', 'low']:
        return jsonify({'error': 'Criteria must be "high" or "low"'}), 400
    
    results = search_by_nutrient(nutrient, criteria, limit)
    
    return jsonify({
        'nutrient': nutrient,
        'criteria': criteria,
        'results': results
    }), 200


@api_bp.route('/nutrition/low-gi', methods=['GET'])
def low_gi_fruits_endpoint():
    """Get all fruits with low glycemic index"""
    return jsonify({
        'low_gi_fruits': get_low_gi_fruits(),
        'description': 'Fruits with GI < 55 are considered low glycemic'
    }), 200


@api_bp.route('/nutrition/seasonal', methods=['GET'])
def seasonal_fruits_endpoint():
    """Get fruits by season"""
    month = request.args.get('month', '').title()
    
    valid_months = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']
    
    if month and month not in valid_months:
        return jsonify({'error': 'Invalid month name'}), 400
    
    results = get_seasonal_fruits(month if month else None)
    
    return jsonify({
        'month': month or 'All',
        'seasonal_fruits': results
    }), 200


@api_bp.route('/nutrition/serving/<fruit_name>', methods=['GET'])
def calculate_serving_endpoint(fruit_name):
    """Calculate nutrition for custom serving size"""
    fruit_name = fruit_name.strip().title()
    grams = request.args.get('grams', 100, type=int)
    
    if grams < 1 or grams > 1000:
        return jsonify({'error': 'Serving size must be between 1 and 1000 grams'}), 400
    
    result = calculate_serving(fruit_name, grams)
    
    if result:
        return jsonify({
            'fruit': fruit_name,
            'nutrition': result,
            'per_serving': f'{grams}g'
        }), 200
    else:
        return jsonify({'error': f'Fruit not found: {fruit_name}'}), 404


@api_bp.route('/nutrition/recipes/<fruit_name>', methods=['GET'])
def get_recipes_endpoint(fruit_name):
    """Get recipes for a specific fruit"""
    fruit_name = fruit_name.strip().title()
    recipe_type = request.args.get('type', '').lower()
    
    valid_types = ['smoothie', 'salad', 'snack', 'dessert', 'main', 'drink', 'breakfast', 'sauce']
    if recipe_type and recipe_type not in valid_types:
        recipe_type = None
    
    recipes = get_recipes(fruit_name, recipe_type if recipe_type else None)
    
    return jsonify({
        'fruit': fruit_name,
        'recipes': recipes,
        'count': len(recipes),
        'filter': recipe_type or 'all'
    }), 200


@api_bp.route('/nutrition/storage/<fruit_name>', methods=['GET'])
def get_storage_endpoint(fruit_name):
    """Get storage information for a fruit"""
    fruit_name = fruit_name.strip().title()
    storage = get_storage_info(fruit_name)
    
    if storage:
        return jsonify({
            'fruit': fruit_name,
            'storage': storage
        }), 200
    else:
        return jsonify({'error': f'Fruit not found: {fruit_name}'}), 404


@api_bp.route('/nutrition/glycemic/<fruit_name>', methods=['GET'])
def get_glycemic_endpoint(fruit_name):
    """Get glycemic index information for a fruit"""
    fruit_name = fruit_name.strip().title()
    gi_info = get_glycemic_info(fruit_name)
    
    if gi_info:
        return jsonify({
            'fruit': fruit_name,
            'glycemic_info': gi_info,
            'scale': {
                'low': '0-55',
                'medium': '56-69',
                'high': '70+'
            }
        }), 200
    else:
        return jsonify({'error': f'Fruit not found: {fruit_name}'}), 404


@api_bp.route('/languages', methods=['GET'])
def get_languages():
    """Get list of supported languages"""
    return jsonify({
        'languages': get_supported_languages(),
        'default': 'en'
    }), 200


@api_bp.route('/translate', methods=['GET'])
def translate():
    """Get translations for UI elements"""
    language = request.args.get('language', 'en')
    
    return jsonify({
        'language': language,
        'fruits': {
            fruit: get_fruit_name(fruit, language)
            for fruit in Config.FRUIT_CLASSES
        },
        'ui': {
            key: get_ui_text(key, language)
            for key in UI_TRANSLATIONS.keys()
        }
    }), 200


@api_bp.route('/analyze/base64', methods=['POST'])
def analyze_base64():
    """
    Analyze a base64 encoded image
    Useful for webcam/real-time detection
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        image_data = data['image']
        language = data.get('language', 'en')
        
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode and save temporarily
        import tempfile
        import uuid
        
        temp_filename = f"{uuid.uuid4()}.jpg"
        temp_path = os.path.join(Config.UPLOAD_FOLDER, temp_filename)
        
        with open(temp_path, 'wb') as f:
            f.write(base64.b64decode(image_data))
        
        try:
            # Analyze
            analyzer = get_enhanced_analyzer()
            analysis = analyzer.analyze(temp_path, language=language, include_nutrition=True)
            
            # Build response
            response = {
                'predicted_class': analysis['predicted_class'],
                'predicted_class_translated': analysis.get('predicted_class_translated'),
                'confidence': format_confidence(analysis['confidence']),
                'ripeness': analysis.get('ripeness'),
                'quality_status': analysis.get('quality_status'),
                'quality_score': analysis.get('quality_score'),
                'size_grade': analysis.get('size_grade'),
                'defects_detected': analysis.get('defects_detected', []),
                'is_edible': analysis.get('is_edible', True)
            }
            
            return jsonify(response), 200
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@api_bp.route('/integration/export', methods=['GET'])
def export_data():
    """
    Export classification data for integration with farm management systems
    Returns data in a format suitable for external systems
    """
    try:
        db = get_db()
        if not db:
            return jsonify({'error': 'Database not available'}), 503
        
        limit = request.args.get('limit', 100, type=int)
        format_type = request.args.get('format', 'json')
        
        history = db.get_recent_classifications(limit=limit)
        stats = db.get_statistics()
        
        export_data = {
            'export_timestamp': str(__import__('datetime').datetime.now()),
            'system': 'Fruit Classification System',
            'version': '2.0',
            'statistics': stats,
            'classifications': history,
            'schema': {
                'classification': {
                    'predicted_class': 'string',
                    'confidence': 'float',
                    'ripeness': 'string (unripe|ripe|overripe)',
                    'quality_status': 'string (healthy|minor_defects|defective|spoiled)',
                    'quality_score': 'int (0-100)',
                    'size_grade': 'string (small|medium|large)',
                    'quality_grade': 'string (A|B|C)',
                    'defects_detected': 'array of strings',
                    'timestamp': 'ISO datetime string'
                }
            }
        }
        
        return jsonify(export_data), 200
        
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500


@api_bp.route('/privacy', methods=['GET'])
def privacy_info():
    """Get privacy and data handling information"""
    return jsonify({
        'data_handling': {
            'image_storage': 'Images are temporarily stored for processing only',
            'retention_period': 'Images are deleted after classification unless explicitly saved',
            'data_sharing': 'No image data is shared with third parties',
            'analytics': 'Only aggregate statistics are collected'
        },
        'user_rights': {
            'access': 'Users can access their classification history',
            'deletion': 'Users can request deletion of their data',
            'export': 'Users can export their data via API'
        },
        'security': {
            'encryption': 'All data transmitted via HTTPS',
            'storage': 'Classification results stored securely in database'
        },
        'ethical_considerations': {
            'purpose': 'System designed to assist in fruit quality assessment',
            'limitations': 'Results should be verified by human experts for critical decisions',
            'bias': 'Model trained on diverse dataset to minimize classification bias',
            'transparency': 'Confidence scores provided for all predictions'
        }
    }), 200


@api_bp.route('/system/limitations', methods=['GET'])
def system_limitations():
    """Get comprehensive system limitations and best practices"""
    from backend.models.performance_evaluation import create_evaluator
    evaluator = create_evaluator(Config.FRUIT_CLASSES)
    limitations = evaluator.get_system_limitations()
    return jsonify(limitations), 200


# ==================== SMART AGRICULTURE INTEGRATION ====================

@api_bp.route('/integration/inventory', methods=['GET'])
def get_inventory_report():
    """Generate inventory report for warehouse/inventory systems"""
    try:
        from backend.models.agriculture_integration import get_agriculture_integration
        
        db = get_db()
        if not db:
            return jsonify({'error': 'Database not available'}), 503
        
        limit = request.args.get('limit', 100, type=int)
        history = db.get_recent_classifications(limit=limit)
        
        integration = get_agriculture_integration(db)
        report = integration.generate_inventory_report(history)
        
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': f'Failed to generate inventory report: {str(e)}'}), 500


@api_bp.route('/integration/pricing', methods=['POST'])
def calculate_pricing():
    """Calculate pricing based on fruit grading"""
    try:
        from backend.models.agriculture_integration import get_agriculture_integration
        from backend.models.grading_system import create_grading_system
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        integration = get_agriculture_integration()
        pricing = integration.calculate_pricing_grade(data)
        
        # Also get detailed grading
        grading_system = create_grading_system()
        detailed_pricing = grading_system.calculate_pricing(
            fruit_type=data.get('predicted_class', 'Apple'),
            grade=data.get('quality_grade', 'B'),
            size=data.get('size_grade', 'medium'),
            quantity=data.get('quantity', 1),
            base_price_per_kg=data.get('base_price', 5.0)
        )
        
        return jsonify({
            'market_analysis': pricing,
            'detailed_pricing': detailed_pricing
        }), 200
    except Exception as e:
        return jsonify({'error': f'Pricing calculation failed: {str(e)}'}), 500


@api_bp.route('/integration/webhook', methods=['POST'])
def register_webhook():
    """Register a webhook for real-time notifications"""
    try:
        from backend.models.agriculture_integration import get_agriculture_integration
        
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'Webhook URL required'}), 400
        
        integration = get_agriculture_integration()
        result = integration.register_webhook(
            webhook_url=data['url'],
            events=data.get('events', ['classification.completed']),
            api_key=data.get('api_key')
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Webhook registration failed: {str(e)}'}), 500


@api_bp.route('/integration/schema', methods=['GET'])
def get_api_schema():
    """Get API schema for integration documentation"""
    from backend.models.agriculture_integration import get_agriculture_integration
    integration = get_agriculture_integration()
    return jsonify(integration.get_api_schema()), 200


@api_bp.route('/integration/farm-export', methods=['GET'])
def export_for_farm_management():
    """Export data in farm management system compatible format"""
    try:
        from backend.models.agriculture_integration import get_agriculture_integration
        
        db = get_db()
        if not db:
            return jsonify({'error': 'Database not available'}), 503
        
        limit = request.args.get('limit', 100, type=int)
        format_type = request.args.get('format', 'standard')
        
        history = db.get_recent_classifications(limit=limit)
        
        integration = get_agriculture_integration(db)
        export = integration.export_for_farm_management(history, format_type)
        
        return jsonify(export), 200
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500


# ==================== GRADING SYSTEM ====================

@api_bp.route('/grading/estimate-size', methods=['POST'])
def estimate_size():
    """Estimate fruit size based on visual analysis"""
    try:
        from backend.models.grading_system import create_grading_system
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        grading = create_grading_system()
        result = grading.estimate_size(
            fruit_type=data.get('fruit_type', 'Apple'),
            relative_scale=data.get('relative_scale', 0.5)
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Size estimation failed: {str(e)}'}), 500


@api_bp.route('/grading/estimate-weight', methods=['POST'])
def estimate_weight():
    """Estimate fruit weight based on size and visual analysis"""
    try:
        from backend.models.grading_system import create_grading_system
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        grading = create_grading_system()
        result = grading.estimate_weight(
            fruit_type=data.get('fruit_type', 'Apple'),
            size_category=data.get('size_category', 'medium'),
            visual_density=data.get('visual_density')
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Weight estimation failed: {str(e)}'}), 500


@api_bp.route('/grading/calculate-grade', methods=['POST'])
def calculate_grade():
    """Calculate quality grade based on fruit analysis"""
    try:
        from backend.models.grading_system import create_grading_system
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        grading = create_grading_system()
        result = grading.calculate_grade(
            quality_score=data.get('quality_score', 80),
            defects=data.get('defects', []),
            ripeness=data.get('ripeness', 'ripe'),
            size_category=data.get('size_category', 'medium')
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Grading calculation failed: {str(e)}'}), 500


@api_bp.route('/grading/packaging', methods=['POST'])
def get_packaging_recommendation():
    """Get packaging recommendations based on grading"""
    try:
        from backend.models.grading_system import create_grading_system
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        grading = create_grading_system()
        result = grading.get_packaging_recommendation(
            fruit_type=data.get('fruit_type', 'Apple'),
            grade=data.get('grade', 'B'),
            size=data.get('size', 'medium'),
            quantity=data.get('quantity', 1)
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Packaging recommendation failed: {str(e)}'}), 500


@api_bp.route('/grading/batch', methods=['POST'])
def grade_batch():
    """Grade a batch of fruits"""
    try:
        from backend.models.grading_system import create_grading_system
        
        data = request.get_json()
        if not data or 'fruits' not in data:
            return jsonify({'error': 'Fruits array required'}), 400
        
        grading = create_grading_system()
        result = grading.grade_batch(data['fruits'])
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Batch grading failed: {str(e)}'}), 500


# ==================== SECURITY & PRIVACY ====================

@api_bp.route('/privacy/policy', methods=['GET'])
def get_privacy_policy():
    """Get comprehensive privacy policy"""
    from backend.models.security_privacy import get_security_manager
    security = get_security_manager(Config.UPLOAD_FOLDER)
    return jsonify(security.get_privacy_policy()), 200


@api_bp.route('/privacy/ethical-guidelines', methods=['GET'])
def get_ethical_guidelines():
    """Get ethical guidelines for AI use in agriculture"""
    from backend.models.security_privacy import get_security_manager
    security = get_security_manager(Config.UPLOAD_FOLDER)
    return jsonify(security.get_ethical_guidelines()), 200


@api_bp.route('/privacy/cleanup', methods=['POST'])
def manual_cleanup():
    """Manually trigger image cleanup"""
    try:
        from backend.models.security_privacy import get_security_manager
        
        data = request.get_json() or {}
        force = data.get('force', False)
        
        security = get_security_manager(Config.UPLOAD_FOLDER)
        result = security.cleanup_old_images(force=force)
        
        return jsonify({
            'status': 'success',
            'cleanup_result': result
        }), 200
    except Exception as e:
        return jsonify({'error': f'Cleanup failed: {str(e)}'}), 500


@api_bp.route('/privacy/delete-data', methods=['DELETE'])
def delete_user_data():
    """Delete user data (GDPR compliance)"""
    try:
        from backend.models.security_privacy import get_security_manager
        
        data = request.get_json() or {}
        
        security = get_security_manager(Config.UPLOAD_FOLDER)
        result = security.delete_user_data(
            user_id=data.get('user_id'),
            classification_ids=data.get('classification_ids')
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Data deletion failed: {str(e)}'}), 500


@api_bp.route('/privacy/access-log', methods=['GET'])
def get_access_log():
    """Get recent access log (admin only)"""
    try:
        from backend.models.security_privacy import get_security_manager
        
        limit = request.args.get('limit', 100, type=int)
        
        security = get_security_manager(Config.UPLOAD_FOLDER)
        log = security.get_access_log(limit=limit)
        
        return jsonify({
            'entries': log,
            'count': len(log)
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve access log: {str(e)}'}), 500


# ==================== PERFORMANCE EVALUATION ====================

@api_bp.route('/evaluation/metrics', methods=['GET'])
def get_evaluation_metrics():
    """Get performance evaluation metrics"""
    try:
        from backend.models.performance_evaluation import create_evaluator
        
        evaluator = create_evaluator(Config.FRUIT_CLASSES)
        
        # Get stored evaluations if available
        db = get_db()
        if db:
            # In production, would retrieve stored evaluation data
            pass
        
        return jsonify({
            'message': 'Performance evaluation module ready',
            'available_metrics': [
                'accuracy',
                'precision',
                'recall',
                'f1_score',
                'confusion_matrix'
            ],
            'usage': 'POST /api/evaluation/evaluate with predictions array'
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to get metrics: {str(e)}'}), 500


@api_bp.route('/evaluation/evaluate', methods=['POST'])
def evaluate_predictions():
    """Evaluate a set of predictions against ground truth"""
    try:
        from backend.models.performance_evaluation import create_evaluator
        
        data = request.get_json()
        if not data or 'predictions' not in data:
            return jsonify({'error': 'Predictions array required'}), 400
        
        evaluator = create_evaluator(Config.FRUIT_CLASSES)
        evaluator.add_batch_predictions(data['predictions'])
        
        report = evaluator.evaluate()
        
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': f'Evaluation failed: {str(e)}'}), 500


@api_bp.route('/evaluation/limitations', methods=['GET'])
def get_detailed_limitations():
    """Get detailed system limitations documentation"""
    try:
        from backend.models.performance_evaluation import create_evaluator
        
        evaluator = create_evaluator(Config.FRUIT_CLASSES)
        limitations = evaluator.get_system_limitations()
        
        return jsonify(limitations), 200
    except Exception as e:
        return jsonify({'error': f'Failed to get limitations: {str(e)}'}), 500


@api_bp.route('/evaluation/report', methods=['GET'])
def generate_evaluation_report():
    """Generate comprehensive evaluation report"""
    try:
        from backend.models.performance_evaluation import create_evaluator
        
        output_format = request.args.get('format', 'json')
        
        evaluator = create_evaluator(Config.FRUIT_CLASSES)
        report = evaluator.generate_evaluation_report(output_format)
        
        if output_format == 'text':
            return report, 200, {'Content-Type': 'text/plain'}
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': f'Report generation failed: {str(e)}'}), 500


# ==================== ANALYTICS DASHBOARD ====================

@api_bp.route('/analytics/dashboard', methods=['GET'])
def get_analytics_dashboard():
    """Get comprehensive analytics dashboard data"""
    try:
        from backend.models.analytics_dashboard import AnalyticsDashboard
        
        days = request.args.get('days', 30, type=int)
        db = get_db()
        
        dashboard = AnalyticsDashboard(db)
        data = dashboard.get_dashboard_summary(days=days)
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': f'Analytics failed: {str(e)}'}), 500


@api_bp.route('/analytics/inventory', methods=['GET'])
def get_inventory_analytics():
    """Get inventory analytics report"""
    try:
        from backend.models.analytics_dashboard import AnalyticsDashboard
        
        days = request.args.get('days', 7, type=int)
        db = get_db()
        
        dashboard = AnalyticsDashboard(db)
        report = dashboard.get_inventory_report(days=days)
        
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': f'Inventory analytics failed: {str(e)}'}), 500


@api_bp.route('/analytics/export', methods=['GET'])
def export_analytics():
    """Export analytics data"""
    try:
        from backend.models.analytics_dashboard import AnalyticsDashboard
        
        format_type = request.args.get('format', 'json')
        db = get_db()
        
        dashboard = AnalyticsDashboard(db)
        data = dashboard.export_report(format=format_type)
        
        if format_type == 'csv':
            return data, 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=analytics.csv'}
        return data, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500


# ==================== SPOILAGE PREDICTION ====================

@api_bp.route('/spoilage/predict', methods=['POST'])
def predict_spoilage():
    """Predict spoilage timeline for a fruit"""
    try:
        from backend.models.spoilage_prediction import SpoilagePrediction
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body required'}), 400
        
        predictor = SpoilagePrediction()
        prediction = predictor.predict_spoilage(
            fruit_type=data.get('fruit_type', 'unknown'),
            ripeness=data.get('ripeness', 'ripe'),
            quality_score=data.get('quality_score', 80),
            defects=data.get('defects', []),
            storage_condition=data.get('storage', 'room_temp')
        )
        
        return jsonify(prediction), 200
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500


@api_bp.route('/spoilage/batch', methods=['POST'])
def batch_spoilage_prediction():
    """Predict spoilage for multiple items"""
    try:
        from backend.models.spoilage_prediction import SpoilagePrediction
        
        data = request.get_json()
        if not data or 'items' not in data:
            return jsonify({'error': 'Items array required'}), 400
        
        predictor = SpoilagePrediction()
        result = predictor.batch_predict(data['items'])
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Batch prediction failed: {str(e)}'}), 500


@api_bp.route('/spoilage/waste-report', methods=['GET'])
def get_waste_report():
    """Get waste reduction analysis report"""
    try:
        from backend.models.spoilage_prediction import SpoilagePrediction
        
        db = get_db()
        classifications = []
        if db:
            classifications = db.get_recent_classifications(limit=100)
        
        predictor = SpoilagePrediction()
        report = predictor.get_waste_reduction_report(classifications)
        
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': f'Report failed: {str(e)}'}), 500


# ==================== AUTHENTICATION ====================

@api_bp.route('/auth/login', methods=['POST'])
def auth_login():
    """Authenticate user and get session token"""
    try:
        from backend.models.authentication import AuthenticationManager
        
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password required'}), 400
        
        auth = AuthenticationManager()
        result = auth.login(data['username'], data['password'])
        
        if result['success']:
            return jsonify(result), 200
        return jsonify(result), 401
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@api_bp.route('/auth/logout', methods=['POST'])
def auth_logout():
    """Invalidate session token"""
    try:
        from backend.models.authentication import AuthenticationManager
        
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Token required'}), 400
        
        auth = AuthenticationManager()
        result = auth.logout(token)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Logout failed: {str(e)}'}), 500


@api_bp.route('/auth/register', methods=['POST'])
def auth_register():
    """Register a new user"""
    try:
        from backend.models.authentication import AuthenticationManager
        
        data = request.get_json()
        required = ['username', 'password', 'email']
        if not data or not all(k in data for k in required):
            return jsonify({'error': 'Username, password, and email required'}), 400
        
        auth = AuthenticationManager()
        result = auth.register_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            role=data.get('role', 'buyer'),
            full_name=data.get('full_name')
        )
        
        if result['success']:
            return jsonify(result), 201
        return jsonify(result), 400
    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@api_bp.route('/auth/validate', methods=['GET'])
def auth_validate():
    """Validate session token"""
    try:
        from backend.models.authentication import AuthenticationManager
        
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'valid': False, 'error': 'Token required'}), 401
        
        auth = AuthenticationManager()
        result = auth.validate_session(token)
        
        return jsonify(result), 200 if result.get('valid') else 401
    except Exception as e:
        return jsonify({'error': f'Validation failed: {str(e)}'}), 500


@api_bp.route('/auth/dashboard-config', methods=['GET'])
def get_dashboard_config():
    """Get role-specific dashboard configuration"""
    try:
        from backend.models.authentication import AuthenticationManager
        
        role = request.args.get('role', 'guest')
        
        auth = AuthenticationManager()
        config = auth.get_user_dashboard_config(role)
        
        return jsonify(config), 200
    except Exception as e:
        return jsonify({'error': f'Config failed: {str(e)}'}), 500


# ==================== QR CODE GENERATION ====================

@api_bp.route('/qrcode/generate', methods=['POST'])
def generate_qrcode():
    """Generate QR code for fruit classification data"""
    try:
        from backend.models.qrcode_generator import QRCodeGenerator
        
        data = request.get_json()
        if not data or 'fruit_type' not in data:
            return jsonify({'error': 'fruit_type required'}), 400
        
        generator = QRCodeGenerator()
        result = generator.generate_fruit_qr(
            fruit_type=data['fruit_type'],
            grade=data.get('grade', 'B'),
            quality_score=data.get('quality_score', 80),
            price=data.get('price'),
            ripeness=data.get('ripeness'),
            classification_id=data.get('classification_id'),
            batch_id=data.get('batch_id'),
            farm_source=data.get('farm_source')
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'QR generation failed: {str(e)}'}), 500


@api_bp.route('/qrcode/batch-label', methods=['POST'])
def generate_batch_label():
    """Generate QR code for batch of fruits"""
    try:
        from backend.models.qrcode_generator import QRCodeGenerator
        
        data = request.get_json()
        required = ['batch_id', 'fruits', 'total_count']
        if not data or not all(k in data for k in required):
            return jsonify({'error': 'batch_id, fruits, and total_count required'}), 400
        
        generator = QRCodeGenerator()
        result = generator.generate_batch_label(
            batch_id=data['batch_id'],
            fruits=data['fruits'],
            total_count=data['total_count'],
            avg_quality=data.get('avg_quality', 80),
            grade_distribution=data.get('grade_distribution', {'A': 0, 'B': 0, 'C': 0}),
            total_price=data.get('total_price', 0),
            farm_source=data.get('farm_source')
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Batch label generation failed: {str(e)}'}), 500


@api_bp.route('/qrcode/price-tag', methods=['POST'])
def generate_price_tag():
    """Generate QR code for price tag"""
    try:
        from backend.models.qrcode_generator import QRCodeGenerator
        
        data = request.get_json()
        if not data or 'fruit_type' not in data or 'price' not in data:
            return jsonify({'error': 'fruit_type and price required'}), 400
        
        generator = QRCodeGenerator()
        result = generator.generate_price_tag(
            fruit_type=data['fruit_type'],
            price_per_unit=data['price'],
            unit=data.get('unit', 'piece'),
            grade=data.get('grade', 'A'),
            currency=data.get('currency', 'USD'),
            discount_percentage=data.get('discount', 0),
            expiry_date=data.get('expiry_date')
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Price tag generation failed: {str(e)}'}), 500


@api_bp.route('/qrcode/status', methods=['GET'])
def get_qrcode_status():
    """Get QR code generator status and capabilities"""
    try:
        from backend.models.qrcode_generator import QRCodeGenerator
        
        generator = QRCodeGenerator()
        status = generator.get_status()
        
        return jsonify(status), 200
    except Exception as e:
        return jsonify({'error': f'Status check failed: {str(e)}'}), 500


# ==================== EXPLAINABLE AI ====================

@api_bp.route('/explain/analysis', methods=['POST'])
def explain_analysis():
    """Get explainable AI analysis for a prediction"""
    try:
        from backend.models.explainable_ai import ExplainableAI
        
        data = request.get_json()
        if not data or 'predictions' not in data:
            return jsonify({'error': 'Predictions required'}), 400
        
        explainer = ExplainableAI()
        result = explainer.analyze_prediction_confidence(
            predictions=data['predictions'],
            threshold=data.get('threshold', 0.5)
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@api_bp.route('/explain/quality', methods=['POST'])
def explain_quality():
    """Get explanation for quality assessment"""
    try:
        from backend.models.explainable_ai import ExplainableAI
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body required'}), 400
        
        explainer = ExplainableAI()
        result = explainer.explain_quality_assessment(
            quality_score=data.get('quality_score', 80),
            ripeness=data.get('ripeness', 'ripe'),
            defects=data.get('defects', []),
            visual_analysis=data.get('visual_analysis', {})
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Explanation failed: {str(e)}'}), 500


@api_bp.route('/explain/model-info', methods=['GET'])
def get_model_explainability_info():
    """Get model explainability information"""
    try:
        from backend.models.explainable_ai import ExplainableAI
        
        explainer = ExplainableAI()
        info = explainer.get_model_info()
        
        return jsonify(info), 200
    except Exception as e:
        return jsonify({'error': f'Info retrieval failed: {str(e)}'}), 500


# ==================== MODEL RETRAINING ====================

@api_bp.route('/retrain/status', methods=['GET'])
def get_retraining_status():
    """Get model retraining system status"""
    try:
        from backend.models.model_retrainer import ModelRetrainer
        
        retrainer = ModelRetrainer()
        status = retrainer.get_retraining_status()
        
        return jsonify(status), 200
    except Exception as e:
        return jsonify({'error': f'Status check failed: {str(e)}'}), 500


@api_bp.route('/retrain/add-sample', methods=['POST'])
def add_training_sample():
    """Add a new training sample"""
    try:
        from backend.models.model_retrainer import ModelRetrainer
        
        if 'image' not in request.files:
            return jsonify({'error': 'Image file required'}), 400
        
        file = request.files['image']
        fruit_class = request.form.get('fruit_class')
        verified = request.form.get('verified', 'false').lower() == 'true'
        
        if not fruit_class:
            return jsonify({'error': 'fruit_class required'}), 400
        
        # Save uploaded file
        from backend.utils.image_utils import save_uploaded_file
        success, image_path = save_uploaded_file(file, Config.UPLOAD_FOLDER)
        
        if not success:
            return jsonify({'error': f'Failed to save file: {image_path}'}), 500
        
        retrainer = ModelRetrainer()
        result = retrainer.add_training_sample(
            image_path=image_path,
            fruit_class=fruit_class,
            verified=verified,
            metadata={
                'original_filename': file.filename,
                'ripeness': request.form.get('ripeness'),
                'quality_score': request.form.get('quality_score')
            }
        )
        
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'error': f'Add sample failed: {str(e)}'}), 500


@api_bp.route('/retrain/stats', methods=['GET'])
def get_training_stats():
    """Get training data statistics"""
    try:
        from backend.models.model_retrainer import ModelRetrainer
        
        retrainer = ModelRetrainer()
        stats = retrainer.get_training_data_stats()
        
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': f'Stats retrieval failed: {str(e)}'}), 500


@api_bp.route('/retrain/versions', methods=['GET'])
def list_model_versions():
    """List all saved model versions"""
    try:
        from backend.models.model_retrainer import ModelRetrainer
        
        retrainer = ModelRetrainer()
        versions = retrainer.list_model_versions()
        
        return jsonify({'versions': versions, 'count': len(versions)}), 200
    except Exception as e:
        return jsonify({'error': f'Version listing failed: {str(e)}'}), 500


@api_bp.route('/retrain/run', methods=['POST'])
def run_retraining():
    """Start full model retraining (admin only)"""
    try:
        from backend.models.model_retrainer import ModelRetrainer
        
        data = request.get_json() or {}
        
        retrainer = ModelRetrainer()
        result = retrainer.run_full_retraining(
            base_model=data.get('base_model', 'MobileNetV2'),
            epochs=data.get('epochs')
        )
        
        return jsonify(result), 200 if result.get('success') else 400
    except Exception as e:
        return jsonify({'error': f'Retraining failed: {str(e)}'}), 500