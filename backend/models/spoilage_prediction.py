"""
Spoilage Prediction Module
Predicts shelf life, alerts for overripe fruits, and suggests discount recommendations.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import math


class SpoilagePrediction:
    """
    Predicts fruit spoilage timeline and provides waste reduction recommendations.
    """
    
    # Base shelf life data (days) at optimal storage conditions
    SHELF_LIFE_DATA = {
        'apple': {'unripe': 14, 'ripe': 7, 'overripe': 2},
        'banana': {'unripe': 7, 'ripe': 3, 'overripe': 1},
        'orange': {'unripe': 21, 'ripe': 14, 'overripe': 5},
        'mango': {'unripe': 10, 'ripe': 4, 'overripe': 2},
        'strawberry': {'unripe': 5, 'ripe': 3, 'overripe': 1},
        'grape': {'unripe': 10, 'ripe': 5, 'overripe': 2},
        'watermelon': {'unripe': 14, 'ripe': 7, 'overripe': 3},
        'pineapple': {'unripe': 7, 'ripe': 4, 'overripe': 2},
        'cherry': {'unripe': 7, 'ripe': 4, 'overripe': 1},
        'kiwi': {'unripe': 14, 'ripe': 7, 'overripe': 3}
    }
    
    # Storage temperature impact factors
    TEMPERATURE_FACTORS = {
        'refrigerated': 1.5,    # Extends shelf life by 50%
        'room_temp': 1.0,       # Baseline
        'warm': 0.5,            # Halves shelf life
        'cold_chain_broken': 0.3  # Severely reduces shelf life
    }
    
    # Defect impact on shelf life
    DEFECT_PENALTIES = {
        'bruise': 0.7,
        'soft_spot': 0.6,
        'discoloration': 0.8,
        'mold': 0.1,
        'rot': 0.0,
        'cuts': 0.5,
        'insect_damage': 0.4
    }
    
    def __init__(self):
        self.alerts = []
    
    def predict_spoilage(
        self,
        fruit_type: str,
        ripeness: str,
        quality_score: float,
        defects: List[str] = None,
        storage_condition: str = 'room_temp',
        current_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Predict spoilage timeline for a fruit.
        
        Args:
            fruit_type: Type of fruit (e.g., 'apple', 'banana')
            ripeness: Current ripeness state ('unripe', 'ripe', 'overripe')
            quality_score: Quality score (0-100)
            defects: List of detected defects
            storage_condition: Storage type
            current_date: Analysis date (defaults to now)
        
        Returns:
            Spoilage prediction with timeline and recommendations
        """
        fruit_lower = fruit_type.lower()
        ripeness_lower = ripeness.lower() if ripeness else 'ripe'
        defects = defects or []
        current_date = current_date or datetime.now()
        
        # Get base shelf life
        base_life = self.SHELF_LIFE_DATA.get(fruit_lower, {'unripe': 7, 'ripe': 4, 'overripe': 2})
        days_remaining = base_life.get(ripeness_lower, base_life.get('ripe', 4))
        
        # Apply storage factor
        storage_factor = self.TEMPERATURE_FACTORS.get(storage_condition, 1.0)
        days_remaining *= storage_factor
        
        # Apply defect penalties
        defect_factor = 1.0
        for defect in defects:
            defect_lower = defect.lower() if isinstance(defect, str) else defect.get('type', '').lower()
            penalty = self.DEFECT_PENALTIES.get(defect_lower, 0.9)
            defect_factor *= penalty
        days_remaining *= defect_factor
        
        # Apply quality score factor
        quality_factor = max(0.5, quality_score / 100) if quality_score else 1.0
        days_remaining *= quality_factor
        
        days_remaining = max(0, math.ceil(days_remaining))
        
        # Calculate dates
        spoilage_date = current_date + timedelta(days=days_remaining)
        overripe_date = current_date + timedelta(days=max(0, days_remaining - 1))
        critical_date = current_date + timedelta(days=max(0, days_remaining - 2))
        
        # Determine urgency and recommendations
        prediction = {
            'fruit_type': fruit_type,
            'current_ripeness': ripeness,
            'predicted_spoilage_date': spoilage_date.isoformat(),
            'days_until_spoilage': days_remaining,
            'overripe_date': overripe_date.isoformat(),
            'critical_alert_date': critical_date.isoformat(),
            'confidence': self._calculate_confidence(quality_score, len(defects)),
            'urgency': self._get_urgency(days_remaining),
            'risk_level': self._get_risk_level(days_remaining, ripeness_lower),
            'factors_considered': {
                'base_shelf_life': base_life.get(ripeness_lower, 4),
                'storage_impact': storage_factor,
                'defect_impact': round(defect_factor, 2),
                'quality_impact': round(quality_factor, 2)
            },
            'recommendations': self._get_recommendations(fruit_lower, ripeness_lower, days_remaining, defects),
            'discount_suggestion': self._get_discount_suggestion(days_remaining, ripeness_lower, quality_score),
            'storage_tips': self._get_storage_tips(fruit_lower, ripeness_lower),
            'alert': self._generate_alert(fruit_type, days_remaining, ripeness_lower)
        }
        
        return prediction
    
    def _calculate_confidence(self, quality_score: float, defect_count: int) -> float:
        """Calculate prediction confidence based on input quality"""
        base_confidence = 85
        # More defects = more certainty about faster spoilage
        if defect_count > 0:
            base_confidence += min(10, defect_count * 2)
        # Quality score adds precision
        if quality_score:
            base_confidence += (quality_score / 100) * 5
        return min(95, base_confidence)
    
    def _get_urgency(self, days: int) -> str:
        """Get urgency level based on days remaining"""
        if days <= 0:
            return 'expired'
        elif days <= 1:
            return 'critical'
        elif days <= 3:
            return 'high'
        elif days <= 5:
            return 'medium'
        else:
            return 'low'
    
    def _get_risk_level(self, days: int, ripeness: str) -> str:
        """Calculate overall risk level"""
        if days <= 0 or ripeness == 'overripe':
            return 'very_high'
        elif days <= 2:
            return 'high'
        elif days <= 4:
            return 'medium'
        else:
            return 'low'
    
    def _get_recommendations(self, fruit: str, ripeness: str, days: int, defects: List) -> List[str]:
        """Generate action recommendations"""
        recommendations = []
        
        if days <= 0:
            recommendations.append("🚨 EXPIRED: Remove from inventory immediately")
            recommendations.append("Consider composting or disposal")
        elif days <= 1:
            recommendations.append("⚠️ CRITICAL: Use within 24 hours")
            recommendations.append("Apply maximum discount for quick sale")
            recommendations.append("Consider juice/smoothie processing")
        elif days <= 3:
            recommendations.append("🔔 Priority sale item - use quick sale strategies")
            recommendations.append("Move to front of display for visibility")
            recommendations.append("Consider bundled deals")
        elif ripeness == 'unripe':
            recommendations.append("Can be stored longer if kept cool")
            recommendations.append("Monitor daily for ripening progress")
        else:
            recommendations.append("Standard shelf life - regular monitoring")
        
        if defects:
            recommendations.append("Separate from healthy fruits to prevent spread")
        
        # Fruit-specific tips
        if fruit == 'banana' and ripeness == 'overripe':
            recommendations.append("Ideal for baking (banana bread, smoothies)")
        elif fruit == 'apple' and days <= 3:
            recommendations.append("Consider for apple sauce or pie filling")
        
        return recommendations
    
    def _get_discount_suggestion(self, days: int, ripeness: str, quality_score: float) -> Dict[str, Any]:
        """Calculate discount recommendation"""
        if days <= 0:
            return {'discount_percentage': 100, 'action': 'remove', 'reason': 'Expired'}
        
        base_discount = 0
        
        # Days-based discount
        if days <= 1:
            base_discount = 50
        elif days <= 2:
            base_discount = 40
        elif days <= 3:
            base_discount = 30
        elif days <= 5:
            base_discount = 20
        
        # Ripeness adjustment
        if ripeness == 'overripe':
            base_discount += 15
        elif ripeness == 'unripe':
            base_discount = max(0, base_discount - 10)
        
        # Quality adjustment
        if quality_score and quality_score < 70:
            base_discount += 10
        
        base_discount = min(70, base_discount)
        
        return {
            'discount_percentage': base_discount,
            'suggested_action': 'quick_sale' if base_discount >= 30 else 'standard',
            'pricing_tier': 'clearance' if base_discount >= 40 else 'reduced' if base_discount >= 20 else 'standard',
            'reason': self._get_discount_reason(days, ripeness)
        }
    
    def _get_discount_reason(self, days: int, ripeness: str) -> str:
        """Get human-readable discount reason"""
        if days <= 1:
            return "Approaching expiration - same-day sale recommended"
        elif days <= 3:
            return "Short shelf life remaining"
        elif ripeness == 'overripe':
            return "Peak ripeness - best consumed immediately"
        return "Standard pricing applies"
    
    def _get_storage_tips(self, fruit: str, ripeness: str) -> List[str]:
        """Get fruit-specific storage tips"""
        tips = {
            'apple': [
                "Store in refrigerator crisper drawer",
                "Keep away from strong-smelling foods",
                "Store separately from ethylene-sensitive produce"
            ],
            'banana': [
                "Store at room temperature until ripe",
                "Refrigerate once ripe to slow ripening",
                "Separate from other fruits to slow ripening"
            ],
            'orange': [
                "Store at room temperature for up to a week",
                "Refrigerate for longer storage",
                "Keep in mesh bag for air circulation"
            ],
            'mango': [
                "Ripen at room temperature",
                "Refrigerate once ripe",
                "Store in paper bag to speed ripening"
            ],
            'strawberry': [
                "Refrigerate immediately",
                "Don't wash until ready to use",
                "Store in single layer if possible"
            ],
            'grape': [
                "Refrigerate unwashed in perforated bag",
                "Wash just before eating",
                "Keep stem attached until eating"
            ]
        }
        
        default_tips = [
            "Store in cool, dry place",
            "Check daily for signs of spoilage",
            "Separate from ethylene producers if sensitive"
        ]
        
        return tips.get(fruit, default_tips)
    
    def _generate_alert(self, fruit: str, days: int, ripeness: str) -> Optional[Dict]:
        """Generate alert if fruit needs attention"""
        if days > 3 and ripeness != 'overripe':
            return None
        
        alert_level = 'critical' if days <= 1 else 'warning'
        
        return {
            'level': alert_level,
            'message': f"{fruit}: {days} day(s) until spoilage" if days > 0 else f"{fruit}: Already spoiled",
            'action_required': days <= 1,
            'timestamp': datetime.now().isoformat()
        }
    
    def batch_predict(self, items: List[Dict]) -> Dict[str, Any]:
        """
        Predict spoilage for multiple items at once.
        
        Args:
            items: List of dicts with fruit_type, ripeness, quality_score, defects
        
        Returns:
            Batch prediction results with summary
        """
        predictions = []
        critical_count = 0
        warning_count = 0
        
        for item in items:
            prediction = self.predict_spoilage(
                fruit_type=item.get('fruit_type', 'unknown'),
                ripeness=item.get('ripeness', 'ripe'),
                quality_score=item.get('quality_score', 80),
                defects=item.get('defects', []),
                storage_condition=item.get('storage', 'room_temp')
            )
            predictions.append(prediction)
            
            if prediction['urgency'] == 'critical':
                critical_count += 1
            elif prediction['urgency'] in ['high', 'medium']:
                warning_count += 1
        
        return {
            'total_items': len(items),
            'critical_items': critical_count,
            'warning_items': warning_count,
            'predictions': predictions,
            'summary': {
                'immediate_action_needed': critical_count,
                'attention_required': warning_count,
                'total_discount_recommended': sum(
                    1 for p in predictions if p['discount_suggestion']['discount_percentage'] > 0
                )
            },
            'generated_at': datetime.now().isoformat()
        }
    
    def get_waste_reduction_report(self, classifications: List[Dict]) -> Dict[str, Any]:
        """Generate waste reduction analysis report"""
        items_analyzed = len(classifications)
        predicted_waste = 0
        potential_savings = 0
        
        for c in classifications:
            prediction = self.predict_spoilage(
                fruit_type=c.get('predicted_class', 'unknown'),
                ripeness=c.get('ripeness', 'ripe'),
                quality_score=c.get('quality_score', 80),
                defects=c.get('defects_detected', [])
            )
            
            if prediction['days_until_spoilage'] <= 1:
                predicted_waste += 1
                # Assume $2 average value per fruit
                base_price = 2.0
                discount = prediction['discount_suggestion']['discount_percentage']
                potential_savings += base_price * (1 - discount/100)
        
        return {
            'items_analyzed': items_analyzed,
            'items_at_risk': predicted_waste,
            'waste_percentage': round((predicted_waste / max(1, items_analyzed)) * 100, 1),
            'potential_savings_usd': round(potential_savings, 2),
            'recommendations': [
                "Implement daily spoilage checks",
                "Apply dynamic pricing based on freshness",
                "Partner with food banks for near-expiry items",
                "Consider processing (juice, preserves) for overripe items"
            ],
            'generated_at': datetime.now().isoformat()
        }
