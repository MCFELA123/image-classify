"""
Fruit Grading System Module
Weight estimation, size classification, quality grading, and pricing
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class FruitGradingSystem:
    """
    Comprehensive fruit grading system:
    - Size estimation and classification
    - Weight estimation based on visual analysis
    - Quality grading (A, B, C grades)
    - Pricing tier calculation
    - Packaging recommendations
    """
    
    # Standard fruit sizes (in approximate dimensions and weights)
    FRUIT_SIZE_STANDARDS = {
        'Apple': {
            'small': {'diameter_mm': (55, 65), 'weight_g': (100, 140), 'count_per_box': 175},
            'medium': {'diameter_mm': (65, 75), 'weight_g': (140, 180), 'count_per_box': 125},
            'large': {'diameter_mm': (75, 85), 'weight_g': (180, 220), 'count_per_box': 100},
            'extra_large': {'diameter_mm': (85, 100), 'weight_g': (220, 280), 'count_per_box': 80}
        },
        'Banana': {
            'small': {'length_mm': (120, 150), 'weight_g': (80, 100), 'fingers_per_hand': 12},
            'medium': {'length_mm': (150, 180), 'weight_g': (100, 130), 'fingers_per_hand': 10},
            'large': {'length_mm': (180, 220), 'weight_g': (130, 170), 'fingers_per_hand': 8},
            'extra_large': {'length_mm': (220, 250), 'weight_g': (170, 200), 'fingers_per_hand': 6}
        },
        'Orange': {
            'small': {'diameter_mm': (55, 65), 'weight_g': (100, 140), 'count_per_box': 138},
            'medium': {'diameter_mm': (65, 75), 'weight_g': (140, 180), 'count_per_box': 113},
            'large': {'diameter_mm': (75, 90), 'weight_g': (180, 250), 'count_per_box': 88},
            'extra_large': {'diameter_mm': (90, 110), 'weight_g': (250, 350), 'count_per_box': 56}
        },
        'Mango': {
            'small': {'length_mm': (80, 100), 'weight_g': (180, 250), 'count_per_box': 18},
            'medium': {'length_mm': (100, 130), 'weight_g': (250, 350), 'count_per_box': 14},
            'large': {'length_mm': (130, 160), 'weight_g': (350, 500), 'count_per_box': 10},
            'extra_large': {'length_mm': (160, 200), 'weight_g': (500, 700), 'count_per_box': 8}
        },
        'Strawberry': {
            'small': {'length_mm': (20, 30), 'weight_g': (8, 15), 'count_per_punnet': 25},
            'medium': {'length_mm': (30, 40), 'weight_g': (15, 25), 'count_per_punnet': 18},
            'large': {'length_mm': (40, 55), 'weight_g': (25, 40), 'count_per_punnet': 12},
            'extra_large': {'length_mm': (55, 70), 'weight_g': (40, 60), 'count_per_punnet': 8}
        },
        'Grape': {
            'small': {'diameter_mm': (12, 16), 'weight_g': (3, 5), 'grapes_per_bunch': 80},
            'medium': {'diameter_mm': (16, 20), 'weight_g': (5, 8), 'grapes_per_bunch': 60},
            'large': {'diameter_mm': (20, 25), 'weight_g': (8, 12), 'grapes_per_bunch': 45},
            'extra_large': {'diameter_mm': (25, 32), 'weight_g': (12, 18), 'grapes_per_bunch': 35}
        },
        'Watermelon': {
            'small': {'weight_kg': (2, 4), 'weight_g': (2000, 4000)},
            'medium': {'weight_kg': (4, 6), 'weight_g': (4000, 6000)},
            'large': {'weight_kg': (6, 10), 'weight_g': (6000, 10000)},
            'extra_large': {'weight_kg': (10, 15), 'weight_g': (10000, 15000)}
        },
        'Pineapple': {
            'small': {'height_mm': (150, 180), 'weight_g': (700, 1000)},
            'medium': {'height_mm': (180, 220), 'weight_g': (1000, 1400)},
            'large': {'height_mm': (220, 280), 'weight_g': (1400, 2000)},
            'extra_large': {'height_mm': (280, 350), 'weight_g': (2000, 2800)}
        },
        'Cherry': {
            'small': {'diameter_mm': (15, 20), 'weight_g': (4, 6)},
            'medium': {'diameter_mm': (20, 24), 'weight_g': (6, 9)},
            'large': {'diameter_mm': (24, 28), 'weight_g': (9, 12)},
            'extra_large': {'diameter_mm': (28, 35), 'weight_g': (12, 16)}
        },
        'Kiwi': {
            'small': {'weight_g': (50, 70), 'diameter_mm': (35, 42)},
            'medium': {'weight_g': (70, 100), 'diameter_mm': (42, 50)},
            'large': {'weight_g': (100, 130), 'diameter_mm': (50, 58)},
            'extra_large': {'weight_g': (130, 170), 'diameter_mm': (58, 70)}
        }
    }
    
    # Quality grade criteria
    GRADE_CRITERIA = {
        'A': {
            'quality_score_min': 85,
            'max_defects': 0,
            'ripeness': ['ripe'],
            'description': 'Premium grade - Export quality',
            'price_multiplier': 1.0
        },
        'B': {
            'quality_score_min': 65,
            'max_defects': 1,
            'ripeness': ['ripe', 'unripe'],
            'description': 'Standard grade - Retail quality',
            'price_multiplier': 0.80
        },
        'C': {
            'quality_score_min': 40,
            'max_defects': 3,
            'ripeness': ['ripe', 'unripe', 'overripe'],
            'description': 'Economy grade - Processing/discount',
            'price_multiplier': 0.55
        }
    }
    
    def __init__(self):
        """Initialize the grading system"""
        self.grading_history = []
    
    # ==================== Size Estimation ====================
    
    def estimate_size(self, fruit_type: str, relative_scale: float = 0.5) -> Dict:
        """
        Estimate fruit size based on visual analysis
        
        Args:
            fruit_type: Type of fruit
            relative_scale: Visual scale estimate (0-1, where 0.5 is medium)
            
        Returns:
            Size estimation details
        """
        # Determine size category from relative scale
        if relative_scale < 0.3:
            size_category = 'small'
        elif relative_scale < 0.55:
            size_category = 'medium'
        elif relative_scale < 0.8:
            size_category = 'large'
        else:
            size_category = 'extra_large'
        
        # Get fruit-specific size standards
        standards = self.FRUIT_SIZE_STANDARDS.get(fruit_type, self.FRUIT_SIZE_STANDARDS['Apple'])
        size_standard = standards.get(size_category, standards['medium'])
        
        # Estimate weight
        weight_range = size_standard.get('weight_g', (100, 200))
        estimated_weight = (weight_range[0] + weight_range[1]) / 2
        
        return {
            'size_category': size_category,
            'relative_scale': relative_scale,
            'estimated_weight_g': round(estimated_weight),
            'weight_range_g': weight_range,
            'size_specifications': size_standard,
            'confidence': self._calculate_size_confidence(relative_scale),
            'measurement_note': 'Visual estimation - actual weight may vary'
        }
    
    def _calculate_size_confidence(self, scale: float) -> float:
        """Calculate confidence in size estimation"""
        # Confidence is higher when scale is clearly in a category
        category_centers = [0.15, 0.42, 0.67, 0.9]
        distances = [abs(scale - c) for c in category_centers]
        min_distance = min(distances)
        
        # Convert distance to confidence (closer to center = higher confidence)
        confidence = 1 - (min_distance * 2)
        return round(max(0.6, min(0.95, confidence)), 2)
    
    # ==================== Weight Estimation ====================
    
    def estimate_weight(self, fruit_type: str, size_category: str, 
                        visual_density: Optional[str] = None) -> Dict:
        """
        Estimate fruit weight based on size and visual density
        
        Args:
            fruit_type: Type of fruit
            size_category: Size category (small, medium, large, extra_large)
            visual_density: Optional density indicator (light, normal, dense)
            
        Returns:
            Weight estimation with confidence intervals
        """
        standards = self.FRUIT_SIZE_STANDARDS.get(fruit_type, self.FRUIT_SIZE_STANDARDS['Apple'])
        size_data = standards.get(size_category, standards['medium'])
        
        weight_range = size_data.get('weight_g', (100, 200))
        base_weight = (weight_range[0] + weight_range[1]) / 2
        
        # Adjust based on visual density
        density_multipliers = {
            'light': 0.85,
            'normal': 1.0,
            'dense': 1.15
        }
        density_mult = density_multipliers.get(visual_density, 1.0)
        estimated_weight = base_weight * density_mult
        
        # Calculate confidence interval
        margin = (weight_range[1] - weight_range[0]) / 4
        
        return {
            'fruit_type': fruit_type,
            'size_category': size_category,
            'estimated_weight_g': round(estimated_weight),
            'weight_range': {
                'min_g': weight_range[0],
                'max_g': weight_range[1],
                'confidence_interval': f"±{round(margin)}g"
            },
            'visual_density': visual_density or 'normal',
            'estimation_method': 'visual_analysis',
            'accuracy_note': 'Estimation based on typical fruit characteristics. Actual weight may vary by ±15-20%.'
        }
    
    # ==================== Quality Grading ====================
    
    def calculate_grade(self, quality_score: int, defects: List[str], 
                       ripeness: str, size_category: str) -> Dict:
        """
        Calculate quality grade based on multiple factors
        
        Args:
            quality_score: Quality score (0-100)
            defects: List of detected defects
            ripeness: Ripeness status
            size_category: Size category
            
        Returns:
            Comprehensive grading result
        """
        num_defects = len(defects)
        
        # Determine grade
        grade = 'C'  # Default to lowest
        
        if (quality_score >= self.GRADE_CRITERIA['A']['quality_score_min'] and
            num_defects <= self.GRADE_CRITERIA['A']['max_defects'] and
            ripeness in self.GRADE_CRITERIA['A']['ripeness']):
            grade = 'A'
        elif (quality_score >= self.GRADE_CRITERIA['B']['quality_score_min'] and
              num_defects <= self.GRADE_CRITERIA['B']['max_defects'] and
              ripeness in self.GRADE_CRITERIA['B']['ripeness']):
            grade = 'B'
        
        grade_info = self.GRADE_CRITERIA[grade]
        
        # Calculate composite score
        composite_score = self._calculate_composite_score(
            quality_score, num_defects, ripeness, size_category
        )
        
        return {
            'grade': grade,
            'grade_description': grade_info['description'],
            'quality_score': quality_score,
            'composite_score': composite_score,
            'factors': {
                'quality_score': quality_score,
                'defect_count': num_defects,
                'defects': defects,
                'ripeness': ripeness,
                'size': size_category
            },
            'price_multiplier': grade_info['price_multiplier'],
            'suitable_for': self._get_suitable_uses(grade, ripeness),
            'grading_standard': 'USDA-equivalent visual grading'
        }
    
    def _calculate_composite_score(self, quality: int, defects: int, 
                                   ripeness: str, size: str) -> int:
        """Calculate composite score combining all factors"""
        # Base score from quality
        score = quality * 0.5
        
        # Defect penalty
        score -= defects * 10
        
        # Ripeness adjustment
        ripeness_scores = {'ripe': 25, 'unripe': 15, 'overripe': 5}
        score += ripeness_scores.get(ripeness, 15)
        
        # Size bonus
        size_scores = {'extra_large': 25, 'large': 20, 'medium': 15, 'small': 10}
        score += size_scores.get(size, 15)
        
        return max(0, min(100, int(score)))
    
    def _get_suitable_uses(self, grade: str, ripeness: str) -> List[str]:
        """Get suitable uses based on grade and ripeness"""
        uses = {
            'A': {
                'ripe': ['premium_export', 'gift_baskets', 'specialty_retail', 'direct_sale'],
                'unripe': ['future_retail', 'export_green'],
                'overripe': []
            },
            'B': {
                'ripe': ['standard_retail', 'supermarkets', 'local_markets'],
                'unripe': ['ripening_rooms', 'standard_retail'],
                'overripe': ['quick_sale', 'discount_retail']
            },
            'C': {
                'ripe': ['discount_stores', 'processing', 'juice_production'],
                'unripe': ['animal_feed', 'composting'],
                'overripe': ['juice_production', 'jam_making', 'food_processing']
            }
        }
        return uses.get(grade, uses['B']).get(ripeness, ['general_use'])
    
    # ==================== Pricing Calculation ====================
    
    def calculate_pricing(self, fruit_type: str, grade: str, size: str,
                         quantity: int = 1, base_price_per_kg: float = 5.0) -> Dict:
        """
        Calculate pricing based on grading
        
        Args:
            fruit_type: Type of fruit
            grade: Quality grade (A, B, C)
            size: Size category
            quantity: Number of fruits
            base_price_per_kg: Base market price per kg
            
        Returns:
            Pricing breakdown
        """
        # Get average weight for this size
        standards = self.FRUIT_SIZE_STANDARDS.get(fruit_type, self.FRUIT_SIZE_STANDARDS['Apple'])
        size_data = standards.get(size, standards['medium'])
        weight_range = size_data.get('weight_g', (100, 200))
        avg_weight_g = (weight_range[0] + weight_range[1]) / 2
        
        # Grade multiplier
        grade_mult = self.GRADE_CRITERIA.get(grade, self.GRADE_CRITERIA['B'])['price_multiplier']
        
        # Size multiplier
        size_multipliers = {
            'extra_large': 1.25,
            'large': 1.10,
            'medium': 1.00,
            'small': 0.85
        }
        size_mult = size_multipliers.get(size, 1.0)
        
        # Calculate per-unit and total pricing
        weight_kg = avg_weight_g / 1000
        base_per_unit = base_price_per_kg * weight_kg
        adjusted_per_unit = base_per_unit * grade_mult * size_mult
        total_price = adjusted_per_unit * quantity
        
        return {
            'fruit_type': fruit_type,
            'grade': grade,
            'size': size,
            'quantity': quantity,
            'pricing': {
                'base_price_per_kg': base_price_per_kg,
                'estimated_weight_per_unit_g': round(avg_weight_g),
                'price_per_unit': round(adjusted_per_unit, 2),
                'total_price': round(total_price, 2),
                'currency': 'USD'
            },
            'multipliers_applied': {
                'grade_multiplier': grade_mult,
                'size_multiplier': size_mult,
                'combined_multiplier': round(grade_mult * size_mult, 2)
            },
            'market_category': self._get_market_category(grade, size),
            'note': 'Prices are estimates based on standard market rates'
        }
    
    def _get_market_category(self, grade: str, size: str) -> str:
        """Determine market category"""
        if grade == 'A' and size in ['large', 'extra_large']:
            return 'premium'
        elif grade in ['A', 'B'] and size in ['medium', 'large']:
            return 'standard'
        else:
            return 'economy'
    
    # ==================== Packaging Recommendations ====================
    
    def get_packaging_recommendation(self, fruit_type: str, grade: str, 
                                      size: str, quantity: int) -> Dict:
        """
        Get packaging recommendations based on grading
        
        Args:
            fruit_type: Type of fruit
            grade: Quality grade
            size: Size category
            quantity: Number of fruits
            
        Returns:
            Packaging recommendations
        """
        # Get count per box from standards
        standards = self.FRUIT_SIZE_STANDARDS.get(fruit_type, {})
        size_data = standards.get(size, {})
        
        # Estimate fruits per box
        fruits_per_box = size_data.get('count_per_box', 
                         size_data.get('count_per_punnet', 
                         size_data.get('grapes_per_bunch', 50)))
        
        boxes_needed = -(-quantity // fruits_per_box)  # Ceiling division
        
        # Packaging type based on grade
        packaging_types = {
            'A': {
                'type': 'premium_individual',
                'material': 'Recycled cardboard with foam inserts',
                'labeling': 'Premium grade label with origin',
                'cushioning': 'Individual fruit cushioning'
            },
            'B': {
                'type': 'standard_bulk',
                'material': 'Standard cardboard boxes',
                'labeling': 'Standard grade markings',
                'cushioning': 'Layer dividers'
            },
            'C': {
                'type': 'economy_bulk',
                'material': 'Basic cardboard or crates',
                'labeling': 'Basic identification',
                'cushioning': 'Minimal'
            }
        }
        
        packaging = packaging_types.get(grade, packaging_types['B'])
        
        return {
            'fruit_type': fruit_type,
            'grade': grade,
            'size': size,
            'quantity': quantity,
            'packaging': {
                **packaging,
                'units_per_package': fruits_per_box,
                'packages_needed': boxes_needed,
                'estimated_total_weight_kg': round(quantity * size_data.get('weight_g', (150, 150))[0] / 1000, 2)
            },
            'storage_requirements': self._get_storage_requirements(fruit_type),
            'handling_instructions': self._get_handling_instructions(grade)
        }
    
    def _get_storage_requirements(self, fruit_type: str) -> Dict:
        """Get storage requirements by fruit type"""
        storage = {
            'Apple': {'temperature_c': '0-4', 'humidity': '90-95%', 'ethylene': 'producer'},
            'Banana': {'temperature_c': '13-15', 'humidity': '90-95%', 'ethylene': 'producer'},
            'Orange': {'temperature_c': '3-9', 'humidity': '85-90%', 'ethylene': 'low'},
            'Mango': {'temperature_c': '10-13', 'humidity': '85-90%', 'ethylene': 'producer'},
            'Strawberry': {'temperature_c': '0-1', 'humidity': '90-95%', 'ethylene': 'sensitive'},
            'Grape': {'temperature_c': '-1-0', 'humidity': '90-95%', 'ethylene': 'low'},
            'Watermelon': {'temperature_c': '10-15', 'humidity': '85-90%', 'ethylene': 'sensitive'},
            'Pineapple': {'temperature_c': '7-10', 'humidity': '85-90%', 'ethylene': 'low'},
            'Cherry': {'temperature_c': '-1-0', 'humidity': '90-95%', 'ethylene': 'low'},
            'Kiwi': {'temperature_c': '-0.5-0', 'humidity': '95-98%', 'ethylene': 'sensitive'}
        }
        return storage.get(fruit_type, {'temperature_c': '2-8', 'humidity': '85-95%', 'ethylene': 'moderate'})
    
    def _get_handling_instructions(self, grade: str) -> List[str]:
        """Get handling instructions by grade"""
        instructions = {
            'A': [
                'Handle with extreme care - premium product',
                'Avoid stacking heavy loads',
                'Keep away from ethylene producers if sensitive',
                'Maintain cold chain',
                'Inspect for damage before display'
            ],
            'B': [
                'Standard careful handling',
                'Use proper stacking techniques',
                'Monitor storage conditions',
                'Rotate stock - first in, first out'
            ],
            'C': [
                'Handle carefully despite grade',
                'Process quickly to reduce waste',
                'Check for deterioration regularly'
            ]
        }
        return instructions.get(grade, instructions['B'])
    
    # ==================== Batch Grading ====================
    
    def grade_batch(self, fruits: List[Dict]) -> Dict:
        """
        Grade a batch of fruits and provide summary
        
        Args:
            fruits: List of fruit analysis results
            
        Returns:
            Batch grading summary
        """
        results = {
            'batch_size': len(fruits),
            'timestamp': datetime.utcnow().isoformat(),
            'graded_items': [],
            'summary': {
                'by_grade': {'A': 0, 'B': 0, 'C': 0},
                'by_size': {'small': 0, 'medium': 0, 'large': 0, 'extra_large': 0},
                'total_estimated_weight_g': 0,
                'average_quality_score': 0,
                'defective_percentage': 0
            }
        }
        
        total_quality = 0
        defective_count = 0
        
        for fruit in fruits:
            # Grade individual fruit
            grade_result = self.calculate_grade(
                quality_score=fruit.get('quality_score', 80),
                defects=fruit.get('defects_detected', []),
                ripeness=fruit.get('ripeness', 'ripe'),
                size_category=fruit.get('size_grade', 'medium')
            )
            
            # Size estimation
            size_result = self.estimate_size(
                fruit.get('predicted_class', 'Apple'),
                fruit.get('size_scale', 0.5)
            )
            
            results['graded_items'].append({
                'fruit_type': fruit.get('predicted_class'),
                'grade': grade_result['grade'],
                'size': size_result['size_category'],
                'estimated_weight_g': size_result['estimated_weight_g']
            })
            
            # Update summary
            results['summary']['by_grade'][grade_result['grade']] += 1
            results['summary']['by_size'][size_result['size_category']] += 1
            results['summary']['total_estimated_weight_g'] += size_result['estimated_weight_g']
            total_quality += fruit.get('quality_score', 80)
            
            if fruit.get('defects_detected'):
                defective_count += 1
        
        # Calculate averages
        if fruits:
            results['summary']['average_quality_score'] = round(total_quality / len(fruits), 1)
            results['summary']['defective_percentage'] = round(defective_count / len(fruits) * 100, 1)
        
        return results


# Factory function
def create_grading_system() -> FruitGradingSystem:
    """Create a fruit grading system instance"""
    return FruitGradingSystem()
