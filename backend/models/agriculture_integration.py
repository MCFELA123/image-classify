"""
Smart Agriculture Integration Module
Provides APIs and interfaces for farm management and inventory systems
"""
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from backend.config import Config


class SmartAgricultureIntegration:
    """
    Integration layer for connecting with smart agriculture systems:
    - Farm Management Systems (FMS)
    - Inventory Management Systems
    - Supply Chain Systems
    - IoT Sensors
    - ERP Systems
    """
    
    def __init__(self, db_handler=None):
        """
        Initialize the agriculture integration module
        
        Args:
            db_handler: Optional database handler for persistent storage
        """
        self.db_handler = db_handler
        self.registered_webhooks = []
        self.connected_systems = {}
    
    # ==================== API Export Formats ====================
    
    def export_for_farm_management(self, classifications: List[Dict], 
                                    format_type: str = 'standard') -> Dict:
        """
        Export classification data in farm management system compatible format
        
        Args:
            classifications: List of classification results
            format_type: 'standard', 'agri_erp', 'custom'
            
        Returns:
            Formatted data for FMS integration
        """
        if format_type == 'standard':
            return self._format_standard_fms(classifications)
        elif format_type == 'agri_erp':
            return self._format_agri_erp(classifications)
        else:
            return self._format_custom(classifications)
    
    def _format_standard_fms(self, classifications: List[Dict]) -> Dict:
        """Standard FMS format"""
        return {
            'system': 'FruitAI Classification System',
            'export_version': '2.0',
            'timestamp': datetime.utcnow().isoformat(),
            'data_type': 'fruit_classification',
            'records': [
                {
                    'id': c.get('_id', c.get('classification_id')),
                    'crop_type': c.get('predicted_class'),
                    'quality_grade': c.get('quality_grade', 'B'),
                    'ripeness_stage': c.get('ripeness', 'ripe'),
                    'size_category': c.get('size_grade', 'medium'),
                    'defects': c.get('defects_detected', []),
                    'quality_score': c.get('quality_score', 80),
                    'is_marketable': c.get('is_edible', True),
                    'timestamp': c.get('timestamp'),
                    'confidence': c.get('confidence', 0.8),
                    'recommendations': {
                        'storage': c.get('storage_recommendation', ''),
                        'handling': c.get('handling_tips', ''),
                        'shelf_life_days': c.get('days_until_overripe', 5)
                    }
                }
                for c in classifications
            ],
            'summary': self._generate_summary(classifications)
        }
    
    def _format_agri_erp(self, classifications: List[Dict]) -> Dict:
        """Agricultural ERP system format"""
        # Group by fruit type and grade
        grouped = {}
        for c in classifications:
            fruit = c.get('predicted_class', 'Unknown')
            grade = c.get('quality_grade', 'B')
            key = f"{fruit}_{grade}"
            if key not in grouped:
                grouped[key] = {
                    'product_code': f"FRT_{fruit.upper()[:3]}_{grade}",
                    'product_name': fruit,
                    'grade': grade,
                    'count': 0,
                    'avg_quality_score': 0,
                    'items': []
                }
            grouped[key]['count'] += 1
            grouped[key]['items'].append(c)
        
        # Calculate averages
        for key in grouped:
            items = grouped[key]['items']
            grouped[key]['avg_quality_score'] = sum(
                item.get('quality_score', 80) for item in items
            ) / len(items)
            del grouped[key]['items']  # Remove detailed items for summary
        
        return {
            'format': 'AGRI_ERP_V1',
            'timestamp': datetime.utcnow().isoformat(),
            'inventory_snapshot': list(grouped.values()),
            'total_items': len(classifications),
            'export_metadata': {
                'source_system': 'FruitAI',
                'export_type': 'quality_assessment',
                'data_completeness': 1.0
            }
        }
    
    def _format_custom(self, classifications: List[Dict]) -> Dict:
        """Custom format for flexible integration"""
        return {
            'raw_data': classifications,
            'format': 'custom',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _generate_summary(self, classifications: List[Dict]) -> Dict:
        """Generate summary statistics"""
        if not classifications:
            return {'total': 0}
        
        total = len(classifications)
        by_fruit = {}
        by_grade = {'A': 0, 'B': 0, 'C': 0}
        by_ripeness = {'unripe': 0, 'ripe': 0, 'overripe': 0}
        defective_count = 0
        
        for c in classifications:
            fruit = c.get('predicted_class', 'Unknown')
            by_fruit[fruit] = by_fruit.get(fruit, 0) + 1
            
            grade = c.get('quality_grade', 'B')
            if grade in by_grade:
                by_grade[grade] += 1
            
            ripeness = c.get('ripeness', 'ripe')
            if ripeness in by_ripeness:
                by_ripeness[ripeness] += 1
            
            if c.get('defects_detected'):
                defective_count += 1
        
        return {
            'total': total,
            'by_fruit_type': by_fruit,
            'by_quality_grade': by_grade,
            'by_ripeness': by_ripeness,
            'defective_percentage': (defective_count / total * 100) if total > 0 else 0,
            'marketable_percentage': ((total - defective_count) / total * 100) if total > 0 else 0
        }
    
    # ==================== Inventory Integration ====================
    
    def generate_inventory_report(self, classifications: List[Dict]) -> Dict:
        """
        Generate inventory report suitable for warehouse/inventory systems
        
        Args:
            classifications: List of classification results
            
        Returns:
            Inventory report data
        """
        inventory = {}
        
        for c in classifications:
            fruit = c.get('predicted_class', 'Unknown')
            grade = c.get('quality_grade', 'B')
            size = c.get('size_grade', 'medium')
            
            key = f"{fruit}_{grade}_{size}"
            
            if key not in inventory:
                inventory[key] = {
                    'sku': f"FRT-{fruit[:3].upper()}-{grade}-{size[0].upper()}",
                    'product_name': fruit,
                    'grade': grade,
                    'size': size,
                    'quantity': 0,
                    'quality_scores': [],
                    'shelf_life_estimate_days': [],
                    'suitable_for': set()
                }
            
            inventory[key]['quantity'] += 1
            inventory[key]['quality_scores'].append(c.get('quality_score', 80))
            inventory[key]['shelf_life_estimate_days'].append(c.get('days_until_overripe', 5))
            
            for use in c.get('suitable_for', []):
                inventory[key]['suitable_for'].add(use)
        
        # Calculate averages and convert sets
        for key in inventory:
            scores = inventory[key]['quality_scores']
            shelf_life = inventory[key]['shelf_life_estimate_days']
            
            inventory[key]['avg_quality_score'] = sum(scores) / len(scores)
            inventory[key]['avg_shelf_life_days'] = sum(shelf_life) / len(shelf_life)
            inventory[key]['suitable_for'] = list(inventory[key]['suitable_for'])
            
            del inventory[key]['quality_scores']
            del inventory[key]['shelf_life_estimate_days']
        
        return {
            'report_type': 'inventory_summary',
            'generated_at': datetime.utcnow().isoformat(),
            'items': list(inventory.values()),
            'total_unique_skus': len(inventory),
            'total_items': sum(item['quantity'] for item in inventory.values())
        }
    
    # ==================== Pricing & Grading ====================
    
    def calculate_pricing_grade(self, classification: Dict) -> Dict:
        """
        Calculate pricing tier based on quality assessment
        
        Args:
            classification: Single classification result
            
        Returns:
            Pricing information
        """
        quality_score = classification.get('quality_score', 80)
        grade = classification.get('quality_grade', 'B')
        ripeness = classification.get('ripeness', 'ripe')
        defects = classification.get('defects_detected', [])
        size = classification.get('size_grade', 'medium')
        
        # Base price multipliers
        grade_multipliers = {'A': 1.0, 'B': 0.85, 'C': 0.65}
        size_multipliers = {'extra_large': 1.15, 'large': 1.05, 'medium': 1.0, 'small': 0.90}
        ripeness_multipliers = {'ripe': 1.0, 'unripe': 0.80, 'overripe': 0.60}
        
        # Calculate price multiplier
        multiplier = (
            grade_multipliers.get(grade, 0.85) *
            size_multipliers.get(size, 1.0) *
            ripeness_multipliers.get(ripeness, 1.0)
        )
        
        # Defect penalty
        defect_penalty = len(defects) * 0.05
        multiplier = max(0.3, multiplier - defect_penalty)
        
        # Market category
        if multiplier >= 0.95:
            market_category = 'premium_export'
        elif multiplier >= 0.85:
            market_category = 'standard_retail'
        elif multiplier >= 0.70:
            market_category = 'discount_retail'
        else:
            market_category = 'processing_only'
        
        return {
            'pricing_tier': grade,
            'price_multiplier': round(multiplier, 2),
            'market_category': market_category,
            'quality_factors': {
                'grade_contribution': grade_multipliers.get(grade, 0.85),
                'size_contribution': size_multipliers.get(size, 1.0),
                'ripeness_contribution': ripeness_multipliers.get(ripeness, 1.0),
                'defect_penalty': defect_penalty
            },
            'recommendations': self._get_market_recommendations(market_category)
        }
    
    def _get_market_recommendations(self, category: str) -> Dict:
        """Get market recommendations based on category"""
        recommendations = {
            'premium_export': {
                'suggested_channels': ['export', 'premium_retail', 'specialty_stores'],
                'packaging': 'individual_premium',
                'priority': 'high',
                'shelf_placement': 'premium_section'
            },
            'standard_retail': {
                'suggested_channels': ['supermarkets', 'local_retail', 'wholesale'],
                'packaging': 'standard_bulk',
                'priority': 'normal',
                'shelf_placement': 'standard_section'
            },
            'discount_retail': {
                'suggested_channels': ['discount_stores', 'rapid_sale', 'local_markets'],
                'packaging': 'economy_bulk',
                'priority': 'urgent',
                'shelf_placement': 'discount_section'
            },
            'processing_only': {
                'suggested_channels': ['juice_production', 'canning', 'food_processing'],
                'packaging': 'industrial_bulk',
                'priority': 'immediate',
                'shelf_placement': 'not_for_fresh_sale'
            }
        }
        return recommendations.get(category, recommendations['standard_retail'])
    
    # ==================== Webhook Integration ====================
    
    def register_webhook(self, webhook_url: str, events: List[str], 
                        api_key: Optional[str] = None) -> Dict:
        """
        Register a webhook for real-time notifications
        
        Args:
            webhook_url: URL to send notifications
            events: List of event types to subscribe to
            api_key: Optional authentication key
            
        Returns:
            Registration confirmation
        """
        webhook_id = f"wh_{len(self.registered_webhooks) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        webhook = {
            'id': webhook_id,
            'url': webhook_url,
            'events': events,
            'api_key': api_key,
            'created_at': datetime.utcnow().isoformat(),
            'status': 'active'
        }
        
        self.registered_webhooks.append(webhook)
        
        return {
            'webhook_id': webhook_id,
            'status': 'registered',
            'subscribed_events': events,
            'available_events': [
                'classification.completed',
                'quality.alert',
                'defect.detected',
                'batch.processed',
                'inventory.update'
            ]
        }
    
    def trigger_webhook(self, event_type: str, data: Dict) -> List[Dict]:
        """
        Trigger webhooks for specific event
        
        Args:
            event_type: Type of event
            data: Event data to send
            
        Returns:
            List of webhook delivery results
        """
        results = []
        
        for webhook in self.registered_webhooks:
            if event_type in webhook['events'] and webhook['status'] == 'active':
                # In production, this would make actual HTTP requests
                results.append({
                    'webhook_id': webhook['id'],
                    'event': event_type,
                    'status': 'delivered',
                    'timestamp': datetime.utcnow().isoformat()
                })
        
        return results
    
    # ==================== API Schema ====================
    
    def get_api_schema(self) -> Dict:
        """
        Get API schema for integration documentation
        
        Returns:
            OpenAPI-compatible schema definition
        """
        return {
            'openapi': '3.0.0',
            'info': {
                'title': 'Fruit Classification API - Agriculture Integration',
                'version': '2.0.0',
                'description': 'API for integrating fruit classification with farm management systems'
            },
            'paths': {
                '/api/integration/export': {
                    'get': {
                        'summary': 'Export classification data',
                        'parameters': [
                            {'name': 'format', 'in': 'query', 'schema': {'type': 'string', 'enum': ['standard', 'agri_erp', 'custom']}},
                            {'name': 'limit', 'in': 'query', 'schema': {'type': 'integer', 'default': 100}}
                        ],
                        'responses': {'200': {'description': 'Exported data'}}
                    }
                },
                '/api/integration/inventory': {
                    'get': {
                        'summary': 'Get inventory report',
                        'responses': {'200': {'description': 'Inventory summary'}}
                    }
                },
                '/api/integration/pricing': {
                    'post': {
                        'summary': 'Calculate pricing grade',
                        'requestBody': {'content': {'application/json': {'schema': {'type': 'object'}}}},
                        'responses': {'200': {'description': 'Pricing information'}}
                    }
                },
                '/api/integration/webhook': {
                    'post': {
                        'summary': 'Register webhook',
                        'requestBody': {'content': {'application/json': {'schema': {'type': 'object'}}}},
                        'responses': {'200': {'description': 'Webhook registration confirmation'}}
                    }
                }
            },
            'components': {
                'schemas': {
                    'Classification': {
                        'type': 'object',
                        'properties': {
                            'predicted_class': {'type': 'string'},
                            'confidence': {'type': 'number'},
                            'ripeness': {'type': 'string', 'enum': ['unripe', 'ripe', 'overripe']},
                            'quality_grade': {'type': 'string', 'enum': ['A', 'B', 'C']},
                            'size_grade': {'type': 'string', 'enum': ['small', 'medium', 'large', 'extra_large']},
                            'quality_score': {'type': 'integer', 'minimum': 0, 'maximum': 100},
                            'defects_detected': {'type': 'array', 'items': {'type': 'string'}}
                        }
                    }
                }
            }
        }


# Singleton instance
_integration_instance = None


def get_agriculture_integration(db_handler=None) -> SmartAgricultureIntegration:
    """Get or create the agriculture integration instance"""
    global _integration_instance
    if _integration_instance is None:
        _integration_instance = SmartAgricultureIntegration(db_handler)
    return _integration_instance
