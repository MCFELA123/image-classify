"""
Analytics Dashboard Module
Provides comprehensive analytics, charts data, and business intelligence
for the Fruit Classification System.
"""
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Any, Optional
import json


class AnalyticsDashboard:
    """
    Analytics engine for fruit classification insights.
    Generates data for charts, KPIs, and trend analysis.
    """
    
    def __init__(self, db_handler=None):
        """Initialize with optional database handler"""
        self.db = db_handler
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes cache
    
    def get_dashboard_summary(self, days: int = 30) -> Dict[str, Any]:
        """
        Get complete dashboard summary with all KPIs.
        
        Returns:
            Comprehensive dashboard data including:
            - Total classifications
            - Quality distribution
            - Defect rates
            - Most common fruits
            - Trend data
        """
        classifications = self._get_classifications(days)
        
        if not classifications:
            return self._get_empty_dashboard()
        
        return {
            'period': {
                'days': days,
                'start_date': (datetime.now() - timedelta(days=days)).isoformat(),
                'end_date': datetime.now().isoformat()
            },
            'kpis': self._calculate_kpis(classifications),
            'quality_distribution': self._get_quality_distribution(classifications),
            'fruit_distribution': self._get_fruit_distribution(classifications),
            'defect_analysis': self._get_defect_analysis(classifications),
            'ripeness_distribution': self._get_ripeness_distribution(classifications),
            'daily_trends': self._get_daily_trends(classifications, days),
            'grade_distribution': self._get_grade_distribution(classifications),
            'processing_stats': self._get_processing_stats(classifications),
            'generated_at': datetime.now().isoformat()
        }
    
    def _get_classifications(self, days: int) -> List[Dict]:
        """Retrieve classifications from database - returns empty list if no data"""
        if self.db:
            try:
                return self.db.get_classifications_in_range(days=days)
            except Exception as e:
                print(f"Database error: {e}")
                return []
        return []
    
    def _calculate_kpis(self, classifications: List[Dict]) -> Dict[str, Any]:
        """Calculate Key Performance Indicators"""
        total = len(classifications)
        if total == 0:
            return self._empty_kpis()
        
        # Quality metrics
        healthy_count = sum(1 for c in classifications 
                          if c.get('quality_status') in ['excellent', 'good', 'fresh'])
        defective_count = sum(1 for c in classifications 
                             if c.get('defects_detected'))
        
        # Average confidence
        confidences = [c.get('confidence', 0) for c in classifications if c.get('confidence')]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Calculate averages
        quality_scores = [c.get('quality_score', 0) for c in classifications if c.get('quality_score')]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        return {
            'total_processed': total,
            'healthy_percentage': round((healthy_count / total) * 100, 1),
            'defective_percentage': round((defective_count / total) * 100, 1),
            'average_confidence': round(avg_confidence * 100, 1),
            'average_quality_score': round(avg_quality, 1),
            'classifications_today': self._count_today(classifications),
            'classifications_this_week': self._count_this_week(classifications)
        }
    
    def _get_quality_distribution(self, classifications: List[Dict]) -> Dict[str, int]:
        """Get distribution of quality statuses for pie chart"""
        distribution = defaultdict(int)
        
        for c in classifications:
            status = c.get('quality_status', 'unknown').lower()
            if status in ['excellent', 'premium']:
                distribution['Premium'] += 1
            elif status in ['good', 'fresh', 'standard']:
                distribution['Standard'] += 1
            elif status in ['fair', 'acceptable']:
                distribution['Fair'] += 1
            elif status in ['poor', 'damaged', 'defective']:
                distribution['Reject'] += 1
            else:
                distribution['Unknown'] += 1
        
        return dict(distribution)
    
    def _get_fruit_distribution(self, classifications: List[Dict]) -> List[Dict]:
        """Get fruit type distribution for bar chart"""
        fruit_counts = defaultdict(int)
        
        for c in classifications:
            fruit = c.get('predicted_class', 'Unknown')
            fruit_counts[fruit] += 1
        
        # Sort by count and return top 10
        sorted_fruits = sorted(fruit_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return [
            {'fruit': fruit, 'count': count, 'percentage': round((count / len(classifications)) * 100, 1)}
            for fruit, count in sorted_fruits
        ]
    
    def _get_defect_analysis(self, classifications: List[Dict]) -> Dict[str, Any]:
        """Analyze defects detected"""
        defect_types = defaultdict(int)
        defective_count = 0
        
        for c in classifications:
            defects = c.get('defects_detected', [])
            if defects:
                defective_count += 1
                for defect in defects:
                    if isinstance(defect, dict):
                        defect_types[defect.get('type', 'unknown')] += 1
                    else:
                        defect_types[str(defect)] += 1
        
        return {
            'total_defective': defective_count,
            'defect_rate': round((defective_count / len(classifications)) * 100, 1) if classifications else 0,
            'defect_types': dict(defect_types),
            'most_common_defect': max(defect_types.items(), key=lambda x: x[1])[0] if defect_types else None
        }
    
    def _get_ripeness_distribution(self, classifications: List[Dict]) -> Dict[str, int]:
        """Get ripeness distribution for pie chart"""
        distribution = defaultdict(int)
        
        for c in classifications:
            ripeness = c.get('ripeness', 'unknown').lower()
            distribution[ripeness.capitalize()] += 1
        
        return dict(distribution)
    
    def _get_daily_trends(self, classifications: List[Dict], days: int) -> List[Dict]:
        """Get daily classification trends for line chart"""
        daily_counts = defaultdict(lambda: {'total': 0, 'healthy': 0, 'defective': 0})
        
        for c in classifications:
            date = c.get('timestamp', c.get('created_at', ''))
            if isinstance(date, str):
                try:
                    date = datetime.fromisoformat(date.replace('Z', '+00:00'))
                except:
                    continue
            
            day_key = date.strftime('%Y-%m-%d') if date else 'unknown'
            daily_counts[day_key]['total'] += 1
            
            if c.get('quality_status') in ['excellent', 'good', 'fresh']:
                daily_counts[day_key]['healthy'] += 1
            if c.get('defects_detected'):
                daily_counts[day_key]['defective'] += 1
        
        # Fill in missing days
        result = []
        for i in range(days):
            date = datetime.now() - timedelta(days=days-1-i)
            day_key = date.strftime('%Y-%m-%d')
            data = daily_counts.get(day_key, {'total': 0, 'healthy': 0, 'defective': 0})
            result.append({
                'date': day_key,
                'label': date.strftime('%b %d'),
                **data
            })
        
        return result
    
    def _get_grade_distribution(self, classifications: List[Dict]) -> Dict[str, int]:
        """Get quality grade distribution"""
        distribution = {'A': 0, 'B': 0, 'C': 0, 'Reject': 0}
        
        for c in classifications:
            grade = c.get('quality_grade', 'C')
            if grade in distribution:
                distribution[grade] += 1
            else:
                distribution['C'] += 1
        
        return distribution
    
    def _get_processing_stats(self, classifications: List[Dict]) -> Dict[str, Any]:
        """Get processing statistics"""
        return {
            'busiest_hour': self._get_busiest_hour(classifications),
            'avg_per_day': round(len(classifications) / max(1, self._get_unique_days(classifications)), 1),
            'peak_day': self._get_peak_day(classifications)
        }
    
    def _count_today(self, classifications: List[Dict]) -> int:
        """Count today's classifications"""
        today = datetime.now().date()
        count = 0
        for c in classifications:
            date = c.get('timestamp', c.get('created_at', ''))
            if isinstance(date, str):
                try:
                    date = datetime.fromisoformat(date.replace('Z', '+00:00')).date()
                    if date == today:
                        count += 1
                except:
                    pass
        return count
    
    def _count_this_week(self, classifications: List[Dict]) -> int:
        """Count this week's classifications"""
        week_start = datetime.now().date() - timedelta(days=datetime.now().weekday())
        count = 0
        for c in classifications:
            date = c.get('timestamp', c.get('created_at', ''))
            if isinstance(date, str):
                try:
                    date = datetime.fromisoformat(date.replace('Z', '+00:00')).date()
                    if date >= week_start:
                        count += 1
                except:
                    pass
        return count
    
    def _get_busiest_hour(self, classifications: List[Dict]) -> int:
        """Get the busiest hour of the day"""
        hour_counts = defaultdict(int)
        for c in classifications:
            date = c.get('timestamp', c.get('created_at', ''))
            if isinstance(date, str):
                try:
                    dt = datetime.fromisoformat(date.replace('Z', '+00:00'))
                    hour_counts[dt.hour] += 1
                except:
                    pass
        return max(hour_counts.items(), key=lambda x: x[1])[0] if hour_counts else 12
    
    def _get_unique_days(self, classifications: List[Dict]) -> int:
        """Count unique days with classifications"""
        days = set()
        for c in classifications:
            date = c.get('timestamp', c.get('created_at', ''))
            if isinstance(date, str):
                try:
                    days.add(datetime.fromisoformat(date.replace('Z', '+00:00')).date())
                except:
                    pass
        return len(days) or 1
    
    def _get_peak_day(self, classifications: List[Dict]) -> str:
        """Get the peak day with most classifications"""
        day_counts = defaultdict(int)
        for c in classifications:
            date = c.get('timestamp', c.get('created_at', ''))
            if isinstance(date, str):
                try:
                    dt = datetime.fromisoformat(date.replace('Z', '+00:00'))
                    day_counts[dt.strftime('%A')] += 1
                except:
                    pass
        return max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else 'N/A'
    
    def _generate_sample_data(self, days: int) -> List[Dict]:
        """Generate sample data for demo purposes"""
        import random
        
        fruits = ['Apple', 'Banana', 'Orange', 'Mango', 'Strawberry', 'Grape', 'Watermelon', 'Pineapple']
        ripeness_states = ['unripe', 'ripe', 'overripe']
        quality_statuses = ['excellent', 'good', 'fair', 'poor']
        grades = ['A', 'B', 'C']
        
        sample = []
        for i in range(random.randint(50, 200)):
            date = datetime.now() - timedelta(
                days=random.randint(0, days-1),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            has_defects = random.random() < 0.15
            
            sample.append({
                'predicted_class': random.choice(fruits),
                'confidence': random.uniform(0.7, 0.99),
                'ripeness': random.choice(ripeness_states),
                'quality_status': random.choice(quality_statuses),
                'quality_score': random.uniform(60, 100),
                'quality_grade': random.choice(grades),
                'defects_detected': [{'type': 'bruise'}] if has_defects else [],
                'timestamp': date.isoformat()
            })
        
        return sample
    
    def _get_empty_dashboard(self) -> Dict[str, Any]:
        """Return empty dashboard structure"""
        return {
            'period': {'days': 0, 'start_date': None, 'end_date': None},
            'kpis': self._empty_kpis(),
            'quality_distribution': {},
            'fruit_distribution': [],
            'defect_analysis': {'total_defective': 0, 'defect_rate': 0, 'defect_types': {}},
            'ripeness_distribution': {},
            'daily_trends': [],
            'grade_distribution': {'A': 0, 'B': 0, 'C': 0, 'Reject': 0},
            'processing_stats': {},
            'generated_at': datetime.now().isoformat()
        }
    
    def _empty_kpis(self) -> Dict[str, Any]:
        """Return empty KPIs structure"""
        return {
            'total_processed': 0,
            'healthy_percentage': 0,
            'defective_percentage': 0,
            'average_confidence': 0,
            'average_quality_score': 0,
            'classifications_today': 0,
            'classifications_this_week': 0
        }
    
    def get_inventory_report(self, days: int = 7) -> Dict[str, Any]:
        """Generate inventory and stock level report"""
        classifications = self._get_classifications(days)
        
        inventory = defaultdict(lambda: {'count': 0, 'avg_quality': [], 'grades': defaultdict(int)})
        
        for c in classifications:
            fruit = c.get('predicted_class', 'Unknown')
            inventory[fruit]['count'] += 1
            if c.get('quality_score'):
                inventory[fruit]['avg_quality'].append(c['quality_score'])
            grade = c.get('quality_grade', 'C')
            inventory[fruit]['grades'][grade] += 1
        
        report = {}
        for fruit, data in inventory.items():
            avg_qual = sum(data['avg_quality']) / len(data['avg_quality']) if data['avg_quality'] else 0
            report[fruit] = {
                'total_count': data['count'],
                'average_quality': round(avg_qual, 1),
                'grade_breakdown': dict(data['grades']),
                'stock_status': 'high' if data['count'] > 20 else 'medium' if data['count'] > 5 else 'low'
            }
        
        return {
            'period_days': days,
            'inventory': report,
            'total_items': sum(d['count'] for d in inventory.values()),
            'generated_at': datetime.now().isoformat()
        }
    
    def get_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly summary report"""
        return self.get_dashboard_summary(days=7)
    
    def get_monthly_report(self) -> Dict[str, Any]:
        """Generate monthly summary report"""
        return self.get_dashboard_summary(days=30)
    
    def export_report(self, format: str = 'json') -> str:
        """Export dashboard data in specified format"""
        data = self.get_dashboard_summary()
        
        if format == 'json':
            return json.dumps(data, indent=2)
        elif format == 'csv':
            # Simple CSV export of KPIs
            kpis = data['kpis']
            lines = ['Metric,Value']
            for key, value in kpis.items():
                lines.append(f'{key},{value}')
            return '\n'.join(lines)
        
        return json.dumps(data)
