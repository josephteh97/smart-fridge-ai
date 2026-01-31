"""
Food Detection and Recognition using Computer Vision
"""
import cv2
import numpy as np
from PIL import Image
import easyocr
import pytesseract
from datetime import datetime, timedelta
import re
from typing import List, Dict, Tuple, Optional
from loguru import logger
from ultralytics import YOLO
import config


class FoodDetector:
    """Handles food detection, recognition, and expiry date extraction"""
    
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
        self.confidence_threshold = config.CONFIDENCE_THRESHOLD
        
        # Initialize YOLO model (you'll need to train or use a pretrained food detection model)
        try:
            self.model = YOLO(config.FOOD_DETECTION_MODEL)
            logger.info("YOLO model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load YOLO model: {e}. Using fallback detection.")
            self.model = None
    
    def capture_image(self, camera_id: int = config.CAMERA_ID) -> np.ndarray:
        """Capture image from camera"""
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            logger.error("Cannot open camera")
            return None
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            logger.error("Cannot capture frame")
            return None
        
        logger.info("Image captured successfully")
        return frame
    
    def detect_food_items(self, image: np.ndarray) -> List[Dict]:
        """Detect food items in the image using YOLO"""
        if self.model is None:
            logger.warning("No model available, using mock detection")
            return self._mock_detection(image)
        
        try:
            results = self.model(image)
            detected_items = []
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    confidence = float(box.conf[0])
                    
                    if confidence >= self.confidence_threshold:
                        class_id = int(box.cls[0])
                        class_name = result.names[class_id]
                        bbox = box.xyxy[0].tolist()
                        
                        detected_items.append({
                            'name': class_name,
                            'confidence': confidence,
                            'bbox': bbox,
                            'category': self._categorize_food(class_name)
                        })
            
            logger.info(f"Detected {len(detected_items)} food items")
            return detected_items
            
        except Exception as e:
            logger.error(f"Error in food detection: {e}")
            return []
    
    def _mock_detection(self, image: np.ndarray) -> List[Dict]:
        """Mock detection for demo purposes"""
        # This is a placeholder - in production, use trained YOLO model
        mock_items = [
            {'name': 'Apple', 'confidence': 0.95, 'bbox': [100, 100, 200, 200], 'category': 'Fruits'},
            {'name': 'Milk', 'confidence': 0.92, 'bbox': [300, 100, 400, 250], 'category': 'Dairy'},
        ]
        return mock_items
    
    def _categorize_food(self, food_name: str) -> str:
        """Categorize food item"""
        food_name_lower = food_name.lower()
        
        vegetables = ['carrot', 'broccoli', 'lettuce', 'tomato', 'cucumber', 'spinach', 'potato']
        fruits = ['apple', 'banana', 'orange', 'strawberry', 'grape', 'mango', 'watermelon']
        dairy = ['milk', 'cheese', 'yogurt', 'butter', 'cream']
        meat = ['chicken', 'beef', 'pork', 'lamb', 'turkey']
        seafood = ['fish', 'salmon', 'tuna', 'shrimp', 'crab']
        
        for veg in vegetables:
            if veg in food_name_lower:
                return 'Vegetables'
        
        for fruit in fruits:
            if fruit in food_name_lower:
                return 'Fruits'
        
        for d in dairy:
            if d in food_name_lower:
                return 'Dairy'
        
        for m in meat:
            if m in food_name_lower:
                return 'Meat'
        
        for s in seafood:
            if s in food_name_lower:
                return 'Seafood'
        
        return 'Others'
    
    def extract_text_from_image(self, image: np.ndarray, bbox: List[int] = None) -> str:
        """Extract text from image using OCR"""
        try:
            if bbox:
                x1, y1, x2, y2 = [int(coord) for coord in bbox]
                image_crop = image[y1:y2, x1:x2]
            else:
                image_crop = image
            
            # Use EasyOCR
            result = self.reader.readtext(image_crop)
            text = ' '.join([item[1] for item in result])
            
            logger.info(f"Extracted text: {text}")
            return text
            
        except Exception as e:
            logger.error(f"Error in OCR: {e}")
            return ""
    
    def extract_expiry_date(self, text: str) -> Optional[datetime]:
        """Extract expiry date from OCR text"""
        # Common date patterns
        patterns = [
            r'(?:exp|expiry|best before|use by)[\s:]*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
            r'(\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{2,4})',
        ]
        
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                date_str = matches[0]
                parsed_date = self._parse_date(date_str)
                if parsed_date:
                    logger.info(f"Extracted expiry date: {parsed_date}")
                    return parsed_date
        
        return None
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime object"""
        formats = [
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%Y/%m/%d',
            '%d-%m-%Y',
            '%m-%d-%Y',
            '%Y-%m-%d',
            '%d %b %Y',
            '%d %B %Y',
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None
    
    def estimate_expiry_date(self, category: str, storage_date: datetime = None) -> datetime:
        """Estimate expiry date based on category default shelf life"""
        if storage_date is None:
            storage_date = datetime.now()
        
        shelf_life_days = config.DEFAULT_SHELF_LIFE.get(category, 7)
        expiry_date = storage_date + timedelta(days=shelf_life_days)
        
        logger.info(f"Estimated expiry date for {category}: {expiry_date}")
        return expiry_date
    
    def scan_barcode(self, image: np.ndarray) -> Optional[str]:
        """Scan barcode from image"""
        try:
            from pyzbar import pyzbar
            
            barcodes = pyzbar.decode(image)
            
            if barcodes:
                barcode_data = barcodes[0].data.decode('utf-8')
                logger.info(f"Barcode detected: {barcode_data}")
                return barcode_data
            
        except Exception as e:
            logger.warning(f"Barcode scanning failed: {e}")
        
        return None
    
    def process_fridge_scan(self, image_path: str = None) -> List[Dict]:
        """Complete scan process for fridge contents"""
        # Capture or load image
        if image_path:
            image = cv2.imread(image_path)
        else:
            image = self.capture_image()
        
        if image is None:
            logger.error("No image available for scanning")
            return []
        
        # Detect food items
        detected_items = self.detect_food_items(image)
        
        # Process each detected item
        processed_items = []
        for item in detected_items:
            # Extract text from bounding box
            text = self.extract_text_from_image(image, item['bbox'])
            
            # Try to extract expiry date
            expiry_date = self.extract_expiry_date(text)
            
            # If no expiry date found, estimate based on category
            if expiry_date is None:
                expiry_date = self.estimate_expiry_date(item['category'])
            
            # Try to scan barcode
            barcode = self.scan_barcode(image)
            
            processed_item = {
                'name': item['name'],
                'category': item['category'],
                'confidence_score': item['confidence'],
                'expiry_date': expiry_date.strftime('%Y-%m-%d') if expiry_date else None,
                'barcode': barcode,
                'quantity': 1,
                'unit': 'piece',
                'location': 'main_compartment',
                'notes': f"Auto-detected with {item['confidence']*100:.1f}% confidence"
            }
            
            processed_items.append(processed_item)
        
        logger.info(f"Processed {len(processed_items)} items from scan")
        return processed_items
    
    def save_scan_image(self, image: np.ndarray, filename: str) -> str:
        """Save scanned image for record keeping"""
        import os
        
        save_dir = os.path.join(config.BASE_DIR, 'data', 'scans')
        os.makedirs(save_dir, exist_ok=True)
        
        filepath = os.path.join(save_dir, filename)
        cv2.imwrite(filepath, image)
        
        logger.info(f"Saved scan image: {filepath}")
        return filepath
