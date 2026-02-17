"""
Performance Evaluation Module
Comprehensive model evaluation with metrics, confusion matrix, and limitations
"""
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from collections import defaultdict
import json


class PerformanceEvaluator:
    """
    Evaluates model performance using standard ML metrics:
    - Accuracy, Precision, Recall, F1-Score
    - Confusion Matrix
    - Per-class performance
    - System limitations analysis
    """
    
    def __init__(self, class_names: List[str]):
        """
        Initialize the performance evaluator
        
        Args:
            class_names: List of class names in the classification system
        """
        self.class_names = class_names
        self.num_classes = len(class_names)
        self.predictions = []
        self.ground_truths = []
        self.confidences = []
        self.evaluation_history = []
    
    # ==================== Data Collection ====================
    
    def add_prediction(self, predicted: str, actual: str, confidence: float):
        """
        Add a prediction for evaluation
        
        Args:
            predicted: Predicted class name
            actual: Actual (ground truth) class name
            confidence: Prediction confidence score
        """
        self.predictions.append(predicted)
        self.ground_truths.append(actual)
        self.confidences.append(confidence)
    
    def add_batch_predictions(self, predictions: List[Dict]):
        """
        Add multiple predictions at once
        
        Args:
            predictions: List of dicts with 'predicted', 'actual', 'confidence'
        """
        for pred in predictions:
            self.add_prediction(
                pred['predicted'],
                pred['actual'],
                pred.get('confidence', 1.0)
            )
    
    def clear_predictions(self):
        """Clear all stored predictions"""
        self.predictions = []
        self.ground_truths = []
        self.confidences = []
    
    # ==================== Core Metrics ====================
    
    def calculate_accuracy(self) -> float:
        """
        Calculate overall accuracy
        
        Returns:
            Accuracy score (0-1)
        """
        if not self.predictions:
            return 0.0
        
        correct = sum(1 for p, a in zip(self.predictions, self.ground_truths) if p == a)
        return correct / len(self.predictions)
    
    def calculate_confusion_matrix(self) -> Dict:
        """
        Calculate confusion matrix
        
        Returns:
            Confusion matrix as dict with 'matrix' and 'labels'
        """
        # Initialize matrix
        matrix = [[0] * self.num_classes for _ in range(self.num_classes)]
        
        # Create class to index mapping
        class_to_idx = {name: idx for idx, name in enumerate(self.class_names)}
        
        # Fill matrix
        for pred, actual in zip(self.predictions, self.ground_truths):
            if pred in class_to_idx and actual in class_to_idx:
                pred_idx = class_to_idx[pred]
                actual_idx = class_to_idx[actual]
                matrix[actual_idx][pred_idx] += 1
        
        return {
            'matrix': matrix,
            'labels': self.class_names,
            'description': 'Rows are actual classes, columns are predicted classes'
        }
    
    def calculate_precision_recall_f1(self) -> Dict:
        """
        Calculate precision, recall, and F1 score per class
        
        Returns:
            Dict with per-class and overall metrics
        """
        # Count predictions per class
        class_stats = {name: {'tp': 0, 'fp': 0, 'fn': 0} for name in self.class_names}
        
        for pred, actual in zip(self.predictions, self.ground_truths):
            if pred == actual:
                if pred in class_stats:
                    class_stats[pred]['tp'] += 1
            else:
                if pred in class_stats:
                    class_stats[pred]['fp'] += 1
                if actual in class_stats:
                    class_stats[actual]['fn'] += 1
        
        # Calculate metrics per class
        class_metrics = {}
        total_precision = 0
        total_recall = 0
        total_f1 = 0
        valid_classes = 0
        
        for name, stats in class_stats.items():
            tp = stats['tp']
            fp = stats['fp']
            fn = stats['fn']
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            class_metrics[name] = {
                'precision': round(precision, 4),
                'recall': round(recall, 4),
                'f1_score': round(f1, 4),
                'support': tp + fn  # Total actual instances
            }
            
            if tp + fn > 0:  # Only count classes with actual instances
                total_precision += precision
                total_recall += recall
                total_f1 += f1
                valid_classes += 1
        
        # Calculate macro averages
        macro_precision = total_precision / valid_classes if valid_classes > 0 else 0
        macro_recall = total_recall / valid_classes if valid_classes > 0 else 0
        macro_f1 = total_f1 / valid_classes if valid_classes > 0 else 0
        
        return {
            'per_class': class_metrics,
            'macro_average': {
                'precision': round(macro_precision, 4),
                'recall': round(macro_recall, 4),
                'f1_score': round(macro_f1, 4)
            },
            'weighted_average': self._calculate_weighted_average(class_metrics),
            'total_samples': len(self.predictions)
        }
    
    def _calculate_weighted_average(self, class_metrics: Dict) -> Dict:
        """Calculate weighted average based on support"""
        total_support = sum(m['support'] for m in class_metrics.values())
        if total_support == 0:
            return {'precision': 0, 'recall': 0, 'f1_score': 0}
        
        weighted_precision = sum(
            m['precision'] * m['support'] for m in class_metrics.values()
        ) / total_support
        weighted_recall = sum(
            m['recall'] * m['support'] for m in class_metrics.values()
        ) / total_support
        weighted_f1 = sum(
            m['f1_score'] * m['support'] for m in class_metrics.values()
        ) / total_support
        
        return {
            'precision': round(weighted_precision, 4),
            'recall': round(weighted_recall, 4),
            'f1_score': round(weighted_f1, 4)
        }
    
    # ==================== Full Evaluation ====================
    
    def evaluate(self) -> Dict:
        """
        Perform comprehensive evaluation
        
        Returns:
            Complete evaluation report
        """
        accuracy = self.calculate_accuracy()
        confusion = self.calculate_confusion_matrix()
        precision_recall = self.calculate_precision_recall_f1()
        confidence_analysis = self.analyze_confidence()
        
        report = {
            'evaluation_timestamp': datetime.utcnow().isoformat(),
            'total_samples': len(self.predictions),
            'accuracy': round(accuracy, 4),
            'precision_recall_f1': precision_recall,
            'confusion_matrix': confusion,
            'confidence_analysis': confidence_analysis,
            'class_distribution': self._get_class_distribution(),
            'performance_summary': self._generate_summary(accuracy, precision_recall)
        }
        
        # Store in history
        self.evaluation_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'samples': len(self.predictions),
            'accuracy': accuracy,
            'macro_f1': precision_recall['macro_average']['f1_score']
        })
        
        return report
    
    def _get_class_distribution(self) -> Dict:
        """Get distribution of classes in ground truth"""
        distribution = defaultdict(int)
        for gt in self.ground_truths:
            distribution[gt] += 1
        
        total = len(self.ground_truths)
        return {
            'counts': dict(distribution),
            'percentages': {k: round(v / total * 100, 2) for k, v in distribution.items()} if total > 0 else {}
        }
    
    def _generate_summary(self, accuracy: float, precision_recall: Dict) -> Dict:
        """Generate human-readable summary"""
        macro = precision_recall['macro_average']
        
        if accuracy >= 0.95:
            performance_level = 'Excellent'
        elif accuracy >= 0.85:
            performance_level = 'Good'
        elif accuracy >= 0.70:
            performance_level = 'Acceptable'
        else:
            performance_level = 'Needs Improvement'
        
        # Find best and worst performing classes
        per_class = precision_recall['per_class']
        sorted_classes = sorted(per_class.items(), key=lambda x: x[1]['f1_score'], reverse=True)
        
        best_classes = [c[0] for c in sorted_classes[:3] if c[1]['support'] > 0]
        worst_classes = [c[0] for c in sorted_classes[-3:] if c[1]['support'] > 0]
        
        return {
            'performance_level': performance_level,
            'accuracy_percentage': f"{accuracy * 100:.1f}%",
            'macro_f1_percentage': f"{macro['f1_score'] * 100:.1f}%",
            'best_performing_classes': best_classes,
            'worst_performing_classes': worst_classes,
            'recommendations': self._generate_recommendations(accuracy, per_class)
        }
    
    def _generate_recommendations(self, accuracy: float, per_class: Dict) -> List[str]:
        """Generate recommendations for improvement"""
        recommendations = []
        
        if accuracy < 0.85:
            recommendations.append("Consider collecting more training data")
        
        for class_name, metrics in per_class.items():
            if metrics['support'] > 0:
                if metrics['precision'] < 0.7:
                    recommendations.append(f"Improve precision for {class_name} - too many false positives")
                if metrics['recall'] < 0.7:
                    recommendations.append(f"Improve recall for {class_name} - too many missed detections")
        
        if not recommendations:
            recommendations.append("Model performance is satisfactory")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    # ==================== Confidence Analysis ====================
    
    def analyze_confidence(self) -> Dict:
        """
        Analyze prediction confidence patterns
        
        Returns:
            Confidence analysis report
        """
        if not self.confidences:
            return {'message': 'No confidence data available'}
        
        correct_confidences = []
        incorrect_confidences = []
        
        for pred, actual, conf in zip(self.predictions, self.ground_truths, self.confidences):
            if pred == actual:
                correct_confidences.append(conf)
            else:
                incorrect_confidences.append(conf)
        
        return {
            'average_confidence': round(np.mean(self.confidences), 4) if self.confidences else 0,
            'confidence_std': round(np.std(self.confidences), 4) if self.confidences else 0,
            'min_confidence': round(min(self.confidences), 4) if self.confidences else 0,
            'max_confidence': round(max(self.confidences), 4) if self.confidences else 0,
            'correct_predictions': {
                'count': len(correct_confidences),
                'avg_confidence': round(np.mean(correct_confidences), 4) if correct_confidences else 0
            },
            'incorrect_predictions': {
                'count': len(incorrect_confidences),
                'avg_confidence': round(np.mean(incorrect_confidences), 4) if incorrect_confidences else 0
            },
            'confidence_brackets': self._confidence_brackets()
        }
    
    def _confidence_brackets(self) -> Dict:
        """Analyze accuracy by confidence bracket"""
        brackets = {
            '0.0-0.5': {'correct': 0, 'total': 0},
            '0.5-0.7': {'correct': 0, 'total': 0},
            '0.7-0.9': {'correct': 0, 'total': 0},
            '0.9-1.0': {'correct': 0, 'total': 0}
        }
        
        for pred, actual, conf in zip(self.predictions, self.ground_truths, self.confidences):
            if conf < 0.5:
                bracket = '0.0-0.5'
            elif conf < 0.7:
                bracket = '0.5-0.7'
            elif conf < 0.9:
                bracket = '0.7-0.9'
            else:
                bracket = '0.9-1.0'
            
            brackets[bracket]['total'] += 1
            if pred == actual:
                brackets[bracket]['correct'] += 1
        
        # Calculate accuracy per bracket
        for bracket in brackets:
            total = brackets[bracket]['total']
            brackets[bracket]['accuracy'] = round(
                brackets[bracket]['correct'] / total, 4
            ) if total > 0 else 0
        
        return brackets
    
    # ==================== Limitations Documentation ====================
    
    def get_system_limitations(self) -> Dict:
        """
        Document system limitations
        
        Returns:
            Comprehensive limitations document
        """
        return {
            'document_version': '2.0',
            'last_updated': datetime.utcnow().isoformat(),
            'categories': {
                'image_quality': {
                    'title': 'Image Quality Requirements',
                    'limitations': [
                        {
                            'issue': 'Low Resolution Images',
                            'impact': 'Reduced classification accuracy',
                            'minimum_requirement': '224x224 pixels recommended',
                            'severity': 'medium'
                        },
                        {
                            'issue': 'Blurry or Out-of-Focus Images',
                            'impact': 'Difficulty detecting fine details like texture and defects',
                            'recommendation': 'Ensure camera focus before capture',
                            'severity': 'high'
                        },
                        {
                            'issue': 'Poor Lighting Conditions',
                            'impact': 'Color distortion affecting ripeness assessment',
                            'recommendation': 'Use even, natural lighting',
                            'severity': 'high'
                        },
                        {
                            'issue': 'Shadows and Harsh Light',
                            'impact': 'False defect detection, color inaccuracy',
                            'recommendation': 'Diffuse lighting recommended',
                            'severity': 'medium'
                        }
                    ]
                },
                'fruit_characteristics': {
                    'title': 'Fruit and Object Limitations',
                    'limitations': [
                        {
                            'issue': 'Similar-Looking Fruits',
                            'examples': ['Green apple vs unripe pear', 'Orange vs tangerine', 'Grape varieties'],
                            'impact': 'Potential misclassification',
                            'severity': 'medium'
                        },
                        {
                            'issue': 'Unusual or Rare Varieties',
                            'impact': 'Lower accuracy for uncommon fruit varieties',
                            'note': 'System optimized for common commercial varieties',
                            'severity': 'low'
                        },
                        {
                            'issue': 'Partial Fruit Visibility',
                            'impact': 'Incomplete analysis, missed defects',
                            'recommendation': 'Capture full fruit in frame',
                            'severity': 'medium'
                        },
                        {
                            'issue': 'Multiple Fruits in Image',
                            'impact': 'May analyze only primary fruit',
                            'recommendation': 'Single fruit per image for best results',
                            'severity': 'low'
                        }
                    ]
                },
                'detection_limitations': {
                    'title': 'Detection Capabilities',
                    'limitations': [
                        {
                            'issue': 'Internal Defects',
                            'description': 'Cannot detect issues inside the fruit',
                            'examples': ['Core rot', 'Internal browning', 'Worm damage'],
                            'recommendation': 'Supplement with physical inspection',
                            'severity': 'high'
                        },
                        {
                            'issue': 'Microscopic Contamination',
                            'description': 'Cannot detect bacteria, pesticide residue, or mold spores',
                            'recommendation': 'Lab testing required for food safety',
                            'severity': 'high'
                        },
                        {
                            'issue': 'Early-Stage Diseases',
                            'description': 'May not detect diseases before visible symptoms',
                            'note': 'Limited to visible spectrum analysis',
                            'severity': 'medium'
                        },
                        {
                            'issue': 'Weight Estimation',
                            'description': 'Size grade is visual estimate only',
                            'note': 'Actual weight requires physical measurement',
                            'severity': 'low'
                        }
                    ]
                },
                'environmental_factors': {
                    'title': 'Environmental Limitations',
                    'limitations': [
                        {
                            'issue': 'Background Interference',
                            'impact': 'Complex backgrounds may affect accuracy',
                            'recommendation': 'Use plain, contrasting background',
                            'severity': 'low'
                        },
                        {
                            'issue': 'Wet or Reflective Surfaces',
                            'impact': 'Reflections may affect color analysis',
                            'recommendation': 'Dry fruit surface before photographing',
                            'severity': 'low'
                        },
                        {
                            'issue': 'Color Temperature Variation',
                            'description': 'Different light sources affect color perception',
                            'recommendation': 'Consistent lighting conditions',
                            'severity': 'medium'
                        }
                    ]
                },
                'system_constraints': {
                    'title': 'Technical Constraints',
                    'limitations': [
                        {
                            'issue': 'API Dependency',
                            'description': 'Requires OpenAI API availability',
                            'impact': 'Service unavailable if API is down',
                            'severity': 'medium'
                        },
                        {
                            'issue': 'Processing Time',
                            'description': 'API calls introduce latency',
                            'typical_time': '1-3 seconds per image',
                            'severity': 'low'
                        },
                        {
                            'issue': 'Supported Fruit Types',
                            'description': 'Optimized for specific fruit categories',
                            'current_support': self.class_names,
                            'severity': 'low'
                        }
                    ]
                }
            },
            'accuracy_expectations': {
                'overall_accuracy': '90-95% under ideal conditions',
                'ripeness_accuracy': '85-90% for clear ripeness stages',
                'defect_accuracy': '80-90% for visible surface defects',
                'size_accuracy': '75-85% for relative size estimation',
                'factors_affecting_accuracy': [
                    'Image quality',
                    'Lighting conditions',
                    'Fruit variety familiarity',
                    'Defect visibility',
                    'Ripeness stage clarity'
                ]
            },
            'recommendations_for_use': [
                'Use as decision support tool, not sole decision maker',
                'Verify critical classifications with human experts',
                'Maintain consistent imaging conditions',
                'Report inaccuracies for system improvement',
                'Combine with physical inspection for food safety'
            ]
        }
    
    # ==================== Reporting ====================
    
    def generate_evaluation_report(self, output_format: str = 'json') -> Any:
        """
        Generate complete evaluation report
        
        Args:
            output_format: 'json' or 'text'
            
        Returns:
            Evaluation report in specified format
        """
        evaluation = self.evaluate()
        limitations = self.get_system_limitations()
        
        report = {
            'report_title': 'Fruit Classification System - Performance Evaluation Report',
            'generated_at': datetime.utcnow().isoformat(),
            'evaluation_results': evaluation,
            'system_limitations': limitations,
            'evaluation_history': self.evaluation_history[-10:]  # Last 10 evaluations
        }
        
        if output_format == 'text':
            return self._format_text_report(report)
        return report
    
    def _format_text_report(self, report: Dict) -> str:
        """Format report as text"""
        lines = [
            "=" * 60,
            "FRUIT CLASSIFICATION SYSTEM - PERFORMANCE REPORT",
            "=" * 60,
            f"\nGenerated: {report['generated_at']}",
            f"Total Samples Evaluated: {report['evaluation_results']['total_samples']}",
            f"\nOverall Accuracy: {report['evaluation_results']['accuracy'] * 100:.1f}%",
            f"\nMacro Averages:",
            f"  Precision: {report['evaluation_results']['precision_recall_f1']['macro_average']['precision'] * 100:.1f}%",
            f"  Recall: {report['evaluation_results']['precision_recall_f1']['macro_average']['recall'] * 100:.1f}%",
            f"  F1-Score: {report['evaluation_results']['precision_recall_f1']['macro_average']['f1_score'] * 100:.1f}%",
            "\n" + "=" * 60,
            "PER-CLASS PERFORMANCE",
            "=" * 60,
        ]
        
        for class_name, metrics in report['evaluation_results']['precision_recall_f1']['per_class'].items():
            lines.append(f"\n{class_name}:")
            lines.append(f"  Precision: {metrics['precision'] * 100:.1f}%")
            lines.append(f"  Recall: {metrics['recall'] * 100:.1f}%")
            lines.append(f"  F1-Score: {metrics['f1_score'] * 100:.1f}%")
            lines.append(f"  Support: {metrics['support']} samples")
        
        return "\n".join(lines)


# Factory function
def create_evaluator(class_names: List[str] = None) -> PerformanceEvaluator:
    """Create a performance evaluator instance"""
    if class_names is None:
        from backend.config import Config
        class_names = Config.FRUIT_CLASSES
    return PerformanceEvaluator(class_names)
