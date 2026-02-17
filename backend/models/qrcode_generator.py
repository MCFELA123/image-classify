"""
QR Code & Barcode Generation Module
Generates QR codes containing fruit classification data, grades, pricing, and quality status.
"""
from typing import Dict, Any, Optional
from datetime import datetime
import base64
import io
import json


class QRCodeGenerator:
    """
    Generates QR codes and barcodes for fruit classification data.
    Supports multiple output formats and data encoding options.
    """
    
    def __init__(self):
        """Initialize QR code generator"""
        self._qr_available = self._check_qr_library()
        self._barcode_available = self._check_barcode_library()
    
    def _check_qr_library(self) -> bool:
        """Check if qrcode library is available"""
        try:
            import qrcode
            return True
        except ImportError:
            return False
    
    def _check_barcode_library(self) -> bool:
        """Check if barcode library is available"""
        try:
            import barcode
            return True
        except ImportError:
            return False
    
    def generate_fruit_qr(
        self,
        fruit_type: str,
        grade: str,
        quality_score: float,
        price: Optional[float] = None,
        ripeness: Optional[str] = None,
        classification_id: Optional[str] = None,
        batch_id: Optional[str] = None,
        farm_source: Optional[str] = None,
        harvest_date: Optional[str] = None,
        output_format: str = 'base64'
    ) -> Dict[str, Any]:
        """
        Generate QR code with fruit classification data.
        
        Args:
            fruit_type: Type of fruit (e.g., 'Apple', 'Banana')
            grade: Quality grade (e.g., 'A', 'B', 'C')
            quality_score: Quality score (0-100)
            price: Optional price per unit
            ripeness: Ripeness status
            classification_id: Unique classification ID
            batch_id: Batch identifier
            farm_source: Source farm name
            harvest_date: Harvest date
            output_format: 'base64', 'bytes', or 'svg'
        
        Returns:
            QR code data with image in requested format
        """
        # Build QR data payload
        qr_data = {
            'type': 'fruit_classification',
            'version': '1.0',
            'fruit': fruit_type,
            'grade': grade,
            'quality_score': round(quality_score, 1),
            'generated_at': datetime.now().isoformat()
        }
        
        # Add optional fields
        if price is not None:
            qr_data['price'] = round(price, 2)
        if ripeness:
            qr_data['ripeness'] = ripeness
        if classification_id:
            qr_data['id'] = classification_id
        if batch_id:
            qr_data['batch'] = batch_id
        if farm_source:
            qr_data['source'] = farm_source
        if harvest_date:
            qr_data['harvest_date'] = harvest_date
        
        # Create compact JSON for QR
        qr_content = json.dumps(qr_data, separators=(',', ':'))
        
        # Generate QR code
        if self._qr_available:
            result = self._generate_qr_image(qr_content, output_format)
        else:
            result = self._generate_text_fallback(qr_data)
        
        return {
            'success': True,
            'data': qr_data,
            'qr_content': qr_content,
            'image': result['image'],
            'format': result['format'],
            'size': result.get('size', 'unknown')
        }
    
    def _generate_qr_image(self, content: str, output_format: str) -> Dict[str, Any]:
        """Generate actual QR code image"""
        try:
            import qrcode
            from PIL import Image
            
            # Create QR code
            qr = qrcode.QRCode(
                version=None,  # Auto-size
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(content)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to requested format
            if output_format == 'base64':
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)
                base64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')
                return {
                    'image': f'data:image/png;base64,{base64_img}',
                    'format': 'base64_png',
                    'size': f'{img.size[0]}x{img.size[1]}'
                }
            elif output_format == 'bytes':
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                return {
                    'image': buffer.getvalue(),
                    'format': 'bytes_png',
                    'size': f'{img.size[0]}x{img.size[1]}'
                }
            else:
                # SVG fallback - return base64
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)
                base64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')
                return {
                    'image': f'data:image/png;base64,{base64_img}',
                    'format': 'base64_png',
                    'size': f'{img.size[0]}x{img.size[1]}'
                }
                
        except Exception as e:
            return self._generate_text_fallback({'error': str(e)})
    
    def _generate_text_fallback(self, data: Dict) -> Dict[str, Any]:
        """Generate text-based fallback when QR library unavailable"""
        # Create a simple ASCII representation
        ascii_qr = self._create_ascii_qr(json.dumps(data))
        return {
            'image': ascii_qr,
            'format': 'ascii_text',
            'size': 'text_only',
            'note': 'Install qrcode package for actual QR: pip install qrcode[pil]'
        }
    
    def _create_ascii_qr(self, content: str) -> str:
        """Create ASCII art QR placeholder"""
        border = "█" * 30
        lines = [
            border,
            "█                            █",
            "█  ▄▄▄▄▄ ▄▄▄   ▄▄▄ ▄▄▄▄▄    █",
            "█  █   █ ▀█▀   ▀█▀ █   █    █",
            "█  █▄▄▄█ ▄▄▄ ▄ ▄▄▄ █▄▄▄█    █",
            "█  ▄▄▄ ▄ ▀█▀ █ ▀█▀ ▄ ▄▄▄    █",
            "█  ▀█▀█▀ ▄▄▄ █ ▄▄▄ ▀█▀█▀    █",
            "█  ▄▄▄▄▄ ▀█▀ █ ▀█▀ ▄▄▄▄▄    █",
            "█  █   █ ▄▄▄ █ ▄▄▄ █   █    █",
            "█  █▄▄▄█ ▀█▀   ▀█▀ █▄▄▄█    █",
            "█                            █",
            border,
            "",
            f"Content: {content[:50]}..."
        ]
        return "\n".join(lines)
    
    def generate_batch_label(
        self,
        batch_id: str,
        fruits: list,
        total_count: int,
        avg_quality: float,
        grade_distribution: Dict[str, int],
        total_price: float,
        farm_source: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate QR code for a batch of fruits.
        
        Args:
            batch_id: Unique batch identifier
            fruits: List of fruit types in batch
            total_count: Total number of items
            avg_quality: Average quality score
            grade_distribution: Count per grade (A, B, C)
            total_price: Total batch price
            farm_source: Source farm
        
        Returns:
            Batch label QR data
        """
        batch_data = {
            'type': 'batch_label',
            'batch_id': batch_id,
            'fruits': list(set(fruits)),
            'count': total_count,
            'avg_quality': round(avg_quality, 1),
            'grades': grade_distribution,
            'total_price': round(total_price, 2),
            'generated_at': datetime.now().isoformat()
        }
        
        if farm_source:
            batch_data['source'] = farm_source
        
        qr_content = json.dumps(batch_data, separators=(',', ':'))
        
        if self._qr_available:
            result = self._generate_qr_image(qr_content, 'base64')
        else:
            result = self._generate_text_fallback(batch_data)
        
        return {
            'success': True,
            'batch_id': batch_id,
            'data': batch_data,
            'image': result['image'],
            'format': result['format']
        }
    
    def generate_price_tag(
        self,
        fruit_type: str,
        price_per_unit: float,
        unit: str = 'piece',
        grade: str = 'A',
        currency: str = 'USD',
        discount_percentage: float = 0,
        expiry_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate QR code for price tag.
        
        Args:
            fruit_type: Type of fruit
            price_per_unit: Price per unit
            unit: Unit type (piece, kg, lb, etc.)
            grade: Quality grade
            currency: Currency code
            discount_percentage: Any applied discount
            expiry_date: Best before date
        
        Returns:
            Price tag QR data
        """
        final_price = price_per_unit * (1 - discount_percentage / 100)
        
        price_data = {
            'type': 'price_tag',
            'fruit': fruit_type,
            'price': round(price_per_unit, 2),
            'final_price': round(final_price, 2),
            'unit': unit,
            'grade': grade,
            'currency': currency
        }
        
        if discount_percentage > 0:
            price_data['discount'] = discount_percentage
        if expiry_date:
            price_data['expiry'] = expiry_date
        
        price_data['generated_at'] = datetime.now().isoformat()
        
        qr_content = json.dumps(price_data, separators=(',', ':'))
        
        if self._qr_available:
            result = self._generate_qr_image(qr_content, 'base64')
        else:
            result = self._generate_text_fallback(price_data)
        
        return {
            'success': True,
            'data': price_data,
            'display_price': f"{currency} {final_price:.2f}/{unit}",
            'image': result['image'],
            'format': result['format']
        }
    
    def generate_traceability_qr(
        self,
        fruit_type: str,
        farm_name: str,
        farm_location: str,
        harvest_date: str,
        classification_date: str,
        quality_grade: str,
        organic: bool = False,
        certifications: list = None
    ) -> Dict[str, Any]:
        """
        Generate traceability QR code for supply chain tracking.
        
        Args:
            fruit_type: Type of fruit
            farm_name: Source farm name
            farm_location: Farm location/region
            harvest_date: Date of harvest
            classification_date: Date of classification
            quality_grade: Quality grade assigned
            organic: Whether organic certified
            certifications: List of certifications
        
        Returns:
            Traceability QR data
        """
        trace_data = {
            'type': 'traceability',
            'fruit': fruit_type,
            'farm': farm_name,
            'location': farm_location,
            'harvested': harvest_date,
            'classified': classification_date,
            'grade': quality_grade,
            'organic': organic
        }
        
        if certifications:
            trace_data['certs'] = certifications
        
        qr_content = json.dumps(trace_data, separators=(',', ':'))
        
        if self._qr_available:
            result = self._generate_qr_image(qr_content, 'base64')
        else:
            result = self._generate_text_fallback(trace_data)
        
        return {
            'success': True,
            'data': trace_data,
            'image': result['image'],
            'format': result['format']
        }
    
    def generate_barcode(
        self,
        product_id: str,
        barcode_type: str = 'ean13'
    ) -> Dict[str, Any]:
        """
        Generate barcode for product identification.
        
        Args:
            product_id: Product identifier (numeric for EAN13)
            barcode_type: Barcode type (ean13, code128, code39, etc.)
        
        Returns:
            Barcode image data
        """
        if not self._barcode_available:
            return {
                'success': False,
                'error': 'Barcode library not available. Install with: pip install python-barcode',
                'product_id': product_id
            }
        
        try:
            import barcode
            from barcode.writer import ImageWriter
            
            # Get barcode class
            barcode_class = barcode.get_barcode_class(barcode_type)
            
            # For EAN13, we need exactly 12 digits (13th is checksum)
            if barcode_type == 'ean13':
                # Pad or truncate to 12 digits
                numeric_id = ''.join(filter(str.isdigit, product_id))
                numeric_id = numeric_id[:12].zfill(12)
                code = barcode_class(numeric_id, writer=ImageWriter())
            else:
                code = barcode_class(product_id, writer=ImageWriter())
            
            # Generate to buffer
            buffer = io.BytesIO()
            code.write(buffer)
            buffer.seek(0)
            
            base64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return {
                'success': True,
                'product_id': product_id,
                'barcode_type': barcode_type,
                'image': f'data:image/png;base64,{base64_img}',
                'format': 'base64_png'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'product_id': product_id
            }
    
    def scan_qr_data(self, qr_content: str) -> Dict[str, Any]:
        """
        Parse and validate QR code content.
        
        Args:
            qr_content: Raw QR code content (JSON string)
        
        Returns:
            Parsed and validated data
        """
        try:
            data = json.loads(qr_content)
            
            qr_type = data.get('type', 'unknown')
            
            return {
                'success': True,
                'valid': True,
                'type': qr_type,
                'data': data
            }
            
        except json.JSONDecodeError:
            return {
                'success': False,
                'valid': False,
                'error': 'Invalid QR content - not valid JSON',
                'raw_content': qr_content
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get QR generator status and capabilities"""
        return {
            'qr_code_available': self._qr_available,
            'barcode_available': self._barcode_available,
            'supported_formats': ['base64_png', 'bytes', 'ascii_text'],
            'supported_qr_types': ['fruit_classification', 'batch_label', 'price_tag', 'traceability'],
            'supported_barcode_types': ['ean13', 'code128', 'code39'] if self._barcode_available else [],
            'install_instructions': {
                'qrcode': 'pip install qrcode[pil]',
                'barcode': 'pip install python-barcode'
            }
        }
