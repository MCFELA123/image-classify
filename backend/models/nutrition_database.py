"""
Nutritional Information Database for Fruits
Contains comprehensive nutrition data, health benefits, storage tips, recipes and more
"""

# Daily recommended values for calculating percentages
DAILY_VALUES = {
    'calories': 2000,
    'carbohydrates': 300,
    'fiber': 25,
    'sugar': 50,
    'protein': 50,
    'fat': 65,
    'vitamin_c': 60,
    'potassium': 3500
}

# Nutritional information per 100g serving
NUTRITION_DATABASE = {
    'Apple': {
        'calories': 52,
        'carbohydrates': 14,
        'fiber': 2.4,
        'sugar': 10,
        'protein': 0.3,
        'fat': 0.2,
        'vitamins': {
            'Vitamin C': '4.6mg (8% DV)',
            'Vitamin K': '2.2μg (3% DV)',
            'Vitamin B6': '0.04mg (2% DV)',
            'Vitamin A': '3μg (0% DV)'
        },
        'minerals': {
            'Potassium': '107mg (3% DV)',
            'Manganese': '0.04mg (2% DV)',
            'Phosphorus': '11mg (1% DV)'
        },
        'health_benefits': [
            'Rich in antioxidants and polyphenols',
            'Supports heart health and lowers cholesterol',
            'High fiber promotes digestive health',
            'May help regulate blood sugar levels',
            'Contains quercetin which supports brain health'
        ],
        'glycemic_index': 36,
        'glycemic_load': 5,
        'gi_category': 'low',
        'season': {
            'peak_months': ['September', 'October', 'November'],
            'available': 'Year-round (stored)',
            'best_quality': 'Fall'
        },
        'storage': {
            'room_temp': '1-2 weeks',
            'refrigerated': '4-6 weeks',
            'tips': 'Store in crisper drawer. Keep away from strong-smelling foods as apples absorb odors.',
            'ripening': 'Store at room temperature to ripen faster'
        },
        'recipes': [
            {'name': 'Apple Cinnamon Smoothie', 'ingredients': ['1 apple', '1 banana', 'cinnamon', 'almond milk', 'honey'], 'type': 'smoothie'},
            {'name': 'Waldorf Salad', 'ingredients': ['apples', 'celery', 'walnuts', 'grapes', 'yogurt'], 'type': 'salad'},
            {'name': 'Baked Apple Chips', 'ingredients': ['apples', 'cinnamon', 'sugar (optional)'], 'type': 'snack'}
        ]
    },
    'Banana': {
        'calories': 89,
        'carbohydrates': 23,
        'fiber': 2.6,
        'sugar': 12,
        'protein': 1.1,
        'fat': 0.3,
        'vitamins': {
            'Vitamin B6': '0.37mg (22% DV)',
            'Vitamin C': '8.7mg (15% DV)',
            'Riboflavin': '0.07mg (4% DV)',
            'Folate': '20μg (5% DV)'
        },
        'minerals': {
            'Potassium': '358mg (10% DV)',
            'Magnesium': '27mg (7% DV)',
            'Manganese': '0.27mg (13% DV)'
        },
        'health_benefits': [
            'Excellent source of potassium for heart health',
            'Natural energy booster for athletes',
            'Contains resistant starch for gut health',
            'May improve insulin sensitivity',
            'Supports muscle recovery after exercise'
        ],
        'glycemic_index': 51,
        'glycemic_load': 13,
        'gi_category': 'low',
        'season': {
            'peak_months': ['Year-round'],
            'available': 'Year-round',
            'best_quality': 'All seasons'
        },
        'storage': {
            'room_temp': '2-7 days (depending on ripeness)',
            'refrigerated': '1-2 weeks (skin darkens but fruit stays fresh)',
            'tips': 'Separate from other fruits to prevent over-ripening. Freeze overripe bananas for smoothies.',
            'ripening': 'Place in paper bag with apple to speed ripening'
        },
        'recipes': [
            {'name': 'Banana Peanut Butter Smoothie', 'ingredients': ['2 bananas', 'peanut butter', 'milk', 'honey', 'ice'], 'type': 'smoothie'},
            {'name': 'Banana Oat Pancakes', 'ingredients': ['bananas', 'oats', 'eggs', 'cinnamon'], 'type': 'breakfast'},
            {'name': 'Frozen Banana Bites', 'ingredients': ['bananas', 'dark chocolate', 'nuts'], 'type': 'snack'}
        ]
    },
    'Orange': {
        'calories': 47,
        'carbohydrates': 12,
        'fiber': 2.4,
        'sugar': 9,
        'protein': 0.9,
        'fat': 0.1,
        'vitamins': {
            'Vitamin C': '53.2mg (89% DV)',
            'Thiamin': '0.09mg (6% DV)',
            'Folate': '30μg (8% DV)',
            'Vitamin A': '11μg (1% DV)'
        },
        'minerals': {
            'Potassium': '181mg (5% DV)',
            'Calcium': '40mg (4% DV)',
            'Magnesium': '10mg (3% DV)'
        },
        'health_benefits': [
            'Exceptional vitamin C for immune support',
            'Contains flavonoids that reduce inflammation',
            'Supports skin health and collagen production',
            'May help prevent kidney stones',
            'High in antioxidants for cell protection'
        ],
        'glycemic_index': 43,
        'glycemic_load': 5,
        'gi_category': 'low',
        'season': {
            'peak_months': ['December', 'January', 'February', 'March'],
            'available': 'Year-round',
            'best_quality': 'Winter'
        },
        'storage': {
            'room_temp': '1 week',
            'refrigerated': '2-3 weeks',
            'tips': 'Store in mesh bag for air circulation. Bring to room temperature before eating for best flavor.',
            'ripening': 'Oranges do not ripen after picking'
        },
        'recipes': [
            {'name': 'Orange Creamsicle Smoothie', 'ingredients': ['2 oranges', 'vanilla yogurt', 'honey', 'ice'], 'type': 'smoothie'},
            {'name': 'Citrus Salad', 'ingredients': ['oranges', 'grapefruit', 'mint', 'honey', 'almonds'], 'type': 'salad'},
            {'name': 'Orange Glazed Chicken', 'ingredients': ['orange juice', 'chicken', 'garlic', 'soy sauce'], 'type': 'main'}
        ]
    },
    'Mango': {
        'calories': 60,
        'carbohydrates': 15,
        'fiber': 1.6,
        'sugar': 14,
        'protein': 0.8,
        'fat': 0.4,
        'vitamins': {
            'Vitamin C': '36.4mg (61% DV)',
            'Vitamin A': '54μg (6% DV)',
            'Vitamin E': '0.9mg (5% DV)',
            'Folate': '43μg (11% DV)'
        },
        'minerals': {
            'Potassium': '168mg (5% DV)',
            'Copper': '0.11mg (5% DV)',
            'Magnesium': '10mg (3% DV)'
        },
        'health_benefits': [
            'Rich in beta-carotene for eye health',
            'Contains enzymes that aid digestion',
            'High in antioxidants like mangiferin',
            'Supports immune system function',
            'May improve skin and hair health'
        ],
        'glycemic_index': 51,
        'glycemic_load': 8,
        'gi_category': 'low',
        'season': {
            'peak_months': ['May', 'June', 'July', 'August'],
            'available': 'Spring to Fall',
            'best_quality': 'Summer'
        },
        'storage': {
            'room_temp': '2-5 days until ripe',
            'refrigerated': '5-7 days (once ripe)',
            'tips': 'Store unripe mangos at room temperature. Refrigerate only after fully ripe.',
            'ripening': 'Place in paper bag at room temperature'
        },
        'recipes': [
            {'name': 'Tropical Mango Smoothie', 'ingredients': ['1 mango', 'pineapple', 'coconut milk', 'lime'], 'type': 'smoothie'},
            {'name': 'Mango Salsa', 'ingredients': ['mango', 'red onion', 'cilantro', 'jalapeño', 'lime'], 'type': 'sauce'},
            {'name': 'Mango Sticky Rice', 'ingredients': ['mango', 'sticky rice', 'coconut milk', 'sugar'], 'type': 'dessert'}
        ]
    },
    'Strawberry': {
        'calories': 32,
        'carbohydrates': 8,
        'fiber': 2,
        'sugar': 5,
        'protein': 0.7,
        'fat': 0.3,
        'vitamins': {
            'Vitamin C': '58.8mg (98% DV)',
            'Folate': '24μg (6% DV)',
            'Vitamin K': '2.2μg (3% DV)',
            'Vitamin B6': '0.05mg (3% DV)'
        },
        'minerals': {
            'Manganese': '0.39mg (19% DV)',
            'Potassium': '153mg (4% DV)',
            'Magnesium': '13mg (3% DV)'
        },
        'health_benefits': [
            'Very high in vitamin C and antioxidants',
            'Low glycemic index, suitable for diabetics',
            'Contains anthocyanins for heart health',
            'May help reduce inflammation',
            'Supports brain health and memory'
        ],
        'glycemic_index': 41,
        'glycemic_load': 3,
        'gi_category': 'low',
        'season': {
            'peak_months': ['April', 'May', 'June'],
            'available': 'Spring to Summer',
            'best_quality': 'Late Spring'
        },
        'storage': {
            'room_temp': '1-2 days',
            'refrigerated': '3-7 days',
            'tips': 'Do not wash until ready to eat. Store in single layer with paper towel to absorb moisture.',
            'ripening': 'Strawberries do not ripen after picking'
        },
        'recipes': [
            {'name': 'Strawberry Banana Smoothie', 'ingredients': ['strawberries', 'banana', 'yogurt', 'honey'], 'type': 'smoothie'},
            {'name': 'Strawberry Spinach Salad', 'ingredients': ['strawberries', 'spinach', 'feta', 'pecans', 'balsamic'], 'type': 'salad'},
            {'name': 'Chocolate Dipped Strawberries', 'ingredients': ['strawberries', 'dark chocolate', 'coconut oil'], 'type': 'dessert'}
        ]
    },
    'Grape': {
        'calories': 69,
        'carbohydrates': 18,
        'fiber': 0.9,
        'sugar': 16,
        'protein': 0.7,
        'fat': 0.2,
        'vitamins': {
            'Vitamin K': '14.6μg (18% DV)',
            'Vitamin C': '3.2mg (5% DV)',
            'Vitamin B6': '0.09mg (5% DV)',
            'Thiamin': '0.07mg (5% DV)'
        },
        'minerals': {
            'Potassium': '191mg (5% DV)',
            'Copper': '0.13mg (6% DV)',
            'Manganese': '0.07mg (4% DV)'
        },
        'health_benefits': [
            'Contains resveratrol for heart health',
            'Rich in polyphenols and antioxidants',
            'May support healthy blood pressure',
            'Contains compounds that protect eye health',
            'Supports healthy aging'
        ],
        'glycemic_index': 59,
        'glycemic_load': 11,
        'gi_category': 'medium',
        'season': {
            'peak_months': ['August', 'September', 'October'],
            'available': 'Summer to Fall',
            'best_quality': 'Early Fall'
        },
        'storage': {
            'room_temp': '1-2 days',
            'refrigerated': '1-2 weeks',
            'tips': 'Store unwashed in perforated bag. Wash just before eating.',
            'ripening': 'Grapes do not ripen after picking'
        },
        'recipes': [
            {'name': 'Green Grape Smoothie', 'ingredients': ['green grapes', 'spinach', 'banana', 'almond milk'], 'type': 'smoothie'},
            {'name': 'Chicken Salad with Grapes', 'ingredients': ['chicken', 'grapes', 'celery', 'mayo', 'walnuts'], 'type': 'salad'},
            {'name': 'Frozen Grape Popsicles', 'ingredients': ['grapes', 'yogurt', 'honey'], 'type': 'snack'}
        ]
    },
    'Watermelon': {
        'calories': 30,
        'carbohydrates': 8,
        'fiber': 0.4,
        'sugar': 6,
        'protein': 0.6,
        'fat': 0.2,
        'vitamins': {
            'Vitamin C': '8.1mg (14% DV)',
            'Vitamin A': '28μg (3% DV)',
            'Vitamin B6': '0.05mg (3% DV)',
            'Vitamin B5': '0.22mg (2% DV)'
        },
        'minerals': {
            'Potassium': '112mg (3% DV)',
            'Magnesium': '10mg (3% DV)',
            'Phosphorus': '11mg (1% DV)'
        },
        'health_benefits': [
            'Excellent hydration (92% water content)',
            'Contains lycopene for heart and prostate health',
            'May reduce muscle soreness after exercise',
            'Low calorie option for weight management',
            'Contains citrulline for blood flow'
        ],
        'glycemic_index': 76,
        'glycemic_load': 4,
        'gi_category': 'high',
        'season': {
            'peak_months': ['June', 'July', 'August'],
            'available': 'Summer',
            'best_quality': 'Mid-Summer'
        },
        'storage': {
            'room_temp': '7-10 days (whole)',
            'refrigerated': '3-5 days (cut)',
            'tips': 'Store whole watermelon at room temperature. Once cut, wrap tightly and refrigerate.',
            'ripening': 'Watermelons do not ripen after picking'
        },
        'recipes': [
            {'name': 'Watermelon Mint Cooler', 'ingredients': ['watermelon', 'mint', 'lime', 'sparkling water'], 'type': 'drink'},
            {'name': 'Watermelon Feta Salad', 'ingredients': ['watermelon', 'feta cheese', 'mint', 'olive oil', 'balsamic'], 'type': 'salad'},
            {'name': 'Frozen Watermelon Pops', 'ingredients': ['watermelon', 'lime juice', 'honey'], 'type': 'snack'}
        ]
    },
    'Pineapple': {
        'calories': 50,
        'carbohydrates': 13,
        'fiber': 1.4,
        'sugar': 10,
        'protein': 0.5,
        'fat': 0.1,
        'vitamins': {
            'Vitamin C': '47.8mg (80% DV)',
            'Vitamin B6': '0.11mg (6% DV)',
            'Thiamin': '0.08mg (5% DV)',
            'Folate': '18μg (5% DV)'
        },
        'minerals': {
            'Manganese': '0.93mg (46% DV)',
            'Copper': '0.11mg (5% DV)',
            'Potassium': '109mg (3% DV)'
        },
        'health_benefits': [
            'Contains bromelain enzyme for digestion',
            'Anti-inflammatory properties',
            'Very high in manganese for bone health',
            'Supports post-surgery healing',
            'May boost immune system'
        ],
        'glycemic_index': 59,
        'glycemic_load': 7,
        'gi_category': 'medium',
        'season': {
            'peak_months': ['March', 'April', 'May', 'June', 'July'],
            'available': 'Year-round',
            'best_quality': 'Spring to Summer'
        },
        'storage': {
            'room_temp': '1-2 days (whole, ripe)',
            'refrigerated': '3-5 days (cut)',
            'tips': 'A ripe pineapple should smell sweet at the base. Store upside down to distribute sugars.',
            'ripening': 'Let sit at room temperature to soften (sugars won\'t increase)'
        },
        'recipes': [
            {'name': 'Piña Colada Smoothie', 'ingredients': ['pineapple', 'coconut milk', 'banana', 'ice'], 'type': 'smoothie'},
            {'name': 'Grilled Pineapple', 'ingredients': ['pineapple', 'brown sugar', 'cinnamon', 'butter'], 'type': 'dessert'},
            {'name': 'Hawaiian Poke Bowl', 'ingredients': ['pineapple', 'rice', 'fish', 'avocado', 'soy sauce'], 'type': 'main'}
        ]
    },
    'Cherry': {
        'calories': 63,
        'carbohydrates': 16,
        'fiber': 2.1,
        'sugar': 13,
        'protein': 1.1,
        'fat': 0.2,
        'vitamins': {
            'Vitamin C': '7mg (12% DV)',
            'Vitamin A': '3μg (0% DV)',
            'Vitamin K': '2.1μg (3% DV)',
            'Potassium': '222mg (6% DV)'
        },
        'minerals': {
            'Potassium': '222mg (6% DV)',
            'Copper': '0.06mg (3% DV)',
            'Manganese': '0.07mg (4% DV)'
        },
        'health_benefits': [
            'Rich in anthocyanins for inflammation',
            'May improve sleep quality (natural melatonin)',
            'Contains compounds that reduce gout attacks',
            'Supports post-workout muscle recovery',
            'May help reduce arthritis symptoms'
        ],
        'glycemic_index': 22,
        'glycemic_load': 4,
        'gi_category': 'low',
        'season': {
            'peak_months': ['May', 'June', 'July', 'August'],
            'available': 'Late Spring to Summer',
            'best_quality': 'Early Summer'
        },
        'storage': {
            'room_temp': '1-2 days',
            'refrigerated': '5-10 days',
            'tips': 'Store unwashed with stems attached. Keep in shallow container to prevent crushing.',
            'ripening': 'Cherries do not ripen after picking'
        },
        'recipes': [
            {'name': 'Cherry Almond Smoothie', 'ingredients': ['cherries', 'almond milk', 'vanilla', 'honey'], 'type': 'smoothie'},
            {'name': 'Cherry Compote', 'ingredients': ['cherries', 'sugar', 'lemon zest', 'vanilla'], 'type': 'sauce'},
            {'name': 'Black Forest Parfait', 'ingredients': ['cherries', 'chocolate', 'whipped cream', 'cake'], 'type': 'dessert'}
        ]
    },
    'Kiwi': {
        'calories': 61,
        'carbohydrates': 15,
        'fiber': 3,
        'sugar': 9,
        'protein': 1.1,
        'fat': 0.5,
        'vitamins': {
            'Vitamin C': '92.7mg (155% DV)',
            'Vitamin K': '40.3μg (50% DV)',
            'Vitamin E': '1.5mg (7% DV)',
            'Folate': '25μg (6% DV)'
        },
        'minerals': {
            'Potassium': '312mg (9% DV)',
            'Copper': '0.13mg (6% DV)',
            'Magnesium': '17mg (4% DV)'
        },
        'health_benefits': [
            'Exceptionally high in Vitamin C',
            'Contains actinidin enzyme for protein digestion',
            'Supports respiratory health',
            'May improve sleep quality',
            'High fiber for digestive health'
        ],
        'glycemic_index': 50,
        'glycemic_load': 7,
        'gi_category': 'low',
        'season': {
            'peak_months': ['November', 'December', 'January', 'February', 'March'],
            'available': 'Year-round',
            'best_quality': 'Winter'
        },
        'storage': {
            'room_temp': '3-5 days (until ripe)',
            'refrigerated': '1-2 weeks (once ripe)',
            'tips': 'Firm kiwis can be ripened at room temperature. Ripe kiwis yield to gentle pressure.',
            'ripening': 'Place in paper bag with banana or apple'
        },
        'recipes': [
            {'name': 'Kiwi Green Smoothie', 'ingredients': ['2 kiwis', 'spinach', 'banana', 'coconut water'], 'type': 'smoothie'},
            {'name': 'Tropical Fruit Salad', 'ingredients': ['kiwi', 'mango', 'pineapple', 'coconut', 'lime'], 'type': 'salad'},
            {'name': 'Kiwi Pavlova', 'ingredients': ['kiwi', 'meringue', 'whipped cream', 'passion fruit'], 'type': 'dessert'}
        ]
    }
}


def get_nutrition_info(fruit_class):
    """
    Get nutritional information for a fruit
    
    Args:
        fruit_class: Name of the fruit
        
    Returns:
        Dictionary with nutritional information or None if not found
    """
    return NUTRITION_DATABASE.get(fruit_class, None)


def get_all_fruits():
    """Get list of all fruits in the database"""
    return list(NUTRITION_DATABASE.keys())


def get_nutrition_summary(fruit_class):
    """
    Get a simplified nutrition summary for display
    
    Args:
        fruit_class: Name of the fruit
        
    Returns:
        Dictionary with key nutrition highlights
    """
    info = NUTRITION_DATABASE.get(fruit_class)
    if not info:
        return None
    
    return {
        'calories': info['calories'],
        'carbs': info['carbohydrates'],
        'fiber': info['fiber'],
        'sugar': info['sugar'],
        'protein': info['protein'],
        'key_vitamins': list(info['vitamins'].keys())[:3],
        'top_benefit': info['health_benefits'][0] if info['health_benefits'] else None
    }


def compare_fruits(fruit_list):
    """
    Compare multiple fruits side by side
    
    Args:
        fruit_list: List of fruit names to compare
        
    Returns:
        Dictionary with comparison data
    """
    comparison = {}
    for fruit in fruit_list:
        info = NUTRITION_DATABASE.get(fruit)
        if info:
            comparison[fruit] = {
                'calories': info['calories'],
                'carbohydrates': info['carbohydrates'],
                'fiber': info['fiber'],
                'sugar': info['sugar'],
                'protein': info['protein'],
                'fat': info['fat'],
                'glycemic_index': info.get('glycemic_index', 'N/A'),
                'gi_category': info.get('gi_category', 'N/A'),
                'vitamin_c': info['vitamins'].get('Vitamin C', 'N/A'),
                'potassium': info['minerals'].get('Potassium', 'N/A')
            }
    return comparison


def search_by_nutrient(nutrient, criteria='high', limit=5):
    """
    Search fruits by nutrient content
    
    Args:
        nutrient: Nutrient to search for (calories, fiber, sugar, protein, vitamin_c)
        criteria: 'high' or 'low'
        limit: Number of results to return
        
    Returns:
        List of fruits sorted by nutrient content
    """
    nutrient_map = {
        'calories': 'calories',
        'fiber': 'fiber',
        'sugar': 'sugar',
        'protein': 'protein',
        'carbs': 'carbohydrates',
        'fat': 'fat'
    }
    
    if nutrient not in nutrient_map:
        return []
    
    results = []
    for fruit, info in NUTRITION_DATABASE.items():
        value = info.get(nutrient_map[nutrient], 0)
        results.append({
            'fruit': fruit,
            'value': value,
            'unit': 'g' if nutrient != 'calories' else 'kcal'
        })
    
    reverse = criteria == 'high'
    results.sort(key=lambda x: x['value'], reverse=reverse)
    return results[:limit]


def get_low_gi_fruits():
    """Get all fruits with low glycemic index"""
    return [
        {'fruit': fruit, 'gi': info.get('glycemic_index', 'N/A'), 'category': info.get('gi_category', 'N/A')}
        for fruit, info in NUTRITION_DATABASE.items()
        if info.get('gi_category') == 'low'
    ]


def get_seasonal_fruits(month=None):
    """
    Get fruits by season/month
    
    Args:
        month: Month name (e.g., 'January') or None for all
        
    Returns:
        List of fruits in season
    """
    results = []
    for fruit, info in NUTRITION_DATABASE.items():
        season = info.get('season', {})
        peak_months = season.get('peak_months', [])
        
        if month:
            if month in peak_months or 'Year-round' in peak_months:
                results.append({
                    'fruit': fruit,
                    'peak_months': peak_months,
                    'best_quality': season.get('best_quality', 'N/A')
                })
        else:
            results.append({
                'fruit': fruit,
                'peak_months': peak_months,
                'available': season.get('available', 'N/A'),
                'best_quality': season.get('best_quality', 'N/A')
            })
    
    return results


def calculate_serving(fruit_class, grams=100):
    """
    Calculate nutrition for custom serving size
    
    Args:
        fruit_class: Name of fruit
        grams: Serving size in grams
        
    Returns:
        Adjusted nutrition values
    """
    info = NUTRITION_DATABASE.get(fruit_class)
    if not info:
        return None
    
    multiplier = grams / 100
    
    return {
        'serving_size': f'{grams}g',
        'calories': round(info['calories'] * multiplier, 1),
        'carbohydrates': round(info['carbohydrates'] * multiplier, 1),
        'fiber': round(info['fiber'] * multiplier, 1),
        'sugar': round(info['sugar'] * multiplier, 1),
        'protein': round(info['protein'] * multiplier, 1),
        'fat': round(info['fat'] * multiplier, 1),
        'daily_values': {
            'calories': round((info['calories'] * multiplier / DAILY_VALUES['calories']) * 100, 1),
            'carbohydrates': round((info['carbohydrates'] * multiplier / DAILY_VALUES['carbohydrates']) * 100, 1),
            'fiber': round((info['fiber'] * multiplier / DAILY_VALUES['fiber']) * 100, 1),
            'sugar': round((info['sugar'] * multiplier / DAILY_VALUES['sugar']) * 100, 1),
            'protein': round((info['protein'] * multiplier / DAILY_VALUES['protein']) * 100, 1)
        }
    }


def get_recipes(fruit_class, recipe_type=None):
    """
    Get recipes for a fruit
    
    Args:
        fruit_class: Name of fruit
        recipe_type: Optional filter (smoothie, salad, snack, dessert, main)
        
    Returns:
        List of recipes
    """
    info = NUTRITION_DATABASE.get(fruit_class)
    if not info:
        return []
    
    recipes = info.get('recipes', [])
    
    if recipe_type:
        recipes = [r for r in recipes if r.get('type') == recipe_type]
    
    return recipes


def get_storage_info(fruit_class):
    """Get storage information for a fruit"""
    info = NUTRITION_DATABASE.get(fruit_class)
    if not info:
        return None
    return info.get('storage', {})


def get_glycemic_info(fruit_class):
    """Get glycemic index information for a fruit"""
    info = NUTRITION_DATABASE.get(fruit_class)
    if not info:
        return None
    return {
        'glycemic_index': info.get('glycemic_index', 'N/A'),
        'glycemic_load': info.get('glycemic_load', 'N/A'),
        'category': info.get('gi_category', 'N/A')
    }
