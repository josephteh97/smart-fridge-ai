"""
Database Management for Smart Fridge AI System
"""
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd
from loguru import logger
import config


class FridgeDatabase:
    """Manages all database operations for the smart fridge system"""
    
    def __init__(self, db_path: str = config.DATABASE_PATH):
        self.db_path = db_path
        self.initialize_database()
    
    def get_connection(self):
        """Create and return a database connection"""
        return sqlite3.connect(self.db_path)
    
    def initialize_database(self):
        """Create tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Food Items Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS food_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER DEFAULT 1,
                unit TEXT,
                storage_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expiry_date DATE,
                location TEXT,
                barcode TEXT,
                image_path TEXT,
                confidence_score REAL,
                status TEXT DEFAULT 'fresh',
                notes TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Alerts Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_item_id INTEGER,
                alert_type TEXT,
                alert_level TEXT,
                message TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_read BOOLEAN DEFAULT 0,
                FOREIGN KEY (food_item_id) REFERENCES food_items (id)
            )
        ''')
        
        # Consumption History Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consumption_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_item_id INTEGER,
                food_name TEXT,
                category TEXT,
                consumed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                was_expired BOOLEAN DEFAULT 0,
                waste_amount REAL,
                FOREIGN KEY (food_item_id) REFERENCES food_items (id)
            )
        ''')
        
        # Recipes Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generated_recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_name TEXT,
                ingredients TEXT,
                instructions TEXT,
                cuisine_type TEXT,
                preparation_time INTEGER,
                servings INTEGER,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_items TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def add_food_item(self, item_data: Dict) -> int:
        """Add a new food item to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO food_items 
            (name, category, quantity, unit, expiry_date, location, barcode, 
             image_path, confidence_score, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item_data.get('name'),
            item_data.get('category'),
            item_data.get('quantity', 1),
            item_data.get('unit', 'piece'),
            item_data.get('expiry_date'),
            item_data.get('location', 'main_compartment'),
            item_data.get('barcode'),
            item_data.get('image_path'),
            item_data.get('confidence_score'),
            item_data.get('notes')
        ))
        
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Added food item: {item_data.get('name')} (ID: {item_id})")
        return item_id
    
    def get_all_items(self, include_consumed: bool = False) -> pd.DataFrame:
        """Retrieve all food items"""
        conn = self.get_connection()
        
        query = '''
            SELECT * FROM food_items 
            WHERE status != 'consumed' OR ? = 1
            ORDER BY expiry_date ASC
        '''
        
        df = pd.read_sql_query(query, conn, params=(include_consumed,))
        conn.close()
        
        return df
    
    def get_items_by_category(self, category: str) -> pd.DataFrame:
        """Get items filtered by category"""
        conn = self.get_connection()
        
        query = '''
            SELECT * FROM food_items 
            WHERE category = ? AND status != 'consumed'
            ORDER BY expiry_date ASC
        '''
        
        df = pd.read_sql_query(query, conn, params=(category,))
        conn.close()
        
        return df
    
    def get_expiring_items(self, days_threshold: int = 3) -> pd.DataFrame:
        """Get items expiring within specified days"""
        conn = self.get_connection()
        
        threshold_date = (datetime.now() + timedelta(days=days_threshold)).strftime('%Y-%m-%d')
        
        query = '''
            SELECT * FROM food_items 
            WHERE expiry_date <= ? AND status = 'fresh'
            ORDER BY expiry_date ASC
        '''
        
        df = pd.read_sql_query(query, conn, params=(threshold_date,))
        conn.close()
        
        return df
    
    def update_item_status(self, item_id: int, status: str):
        """Update the status of a food item"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE food_items 
            SET status = ?, last_updated = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, item_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Updated item {item_id} status to {status}")
    
    def create_alert(self, food_item_id: int, alert_type: str, 
                     alert_level: str, message: str):
        """Create a new alert"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts (food_item_id, alert_type, alert_level, message)
            VALUES (?, ?, ?, ?)
        ''', (food_item_id, alert_type, alert_level, message))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Created {alert_level} alert for item {food_item_id}")
    
    def get_unread_alerts(self) -> pd.DataFrame:
        """Get all unread alerts"""
        conn = self.get_connection()
        
        query = '''
            SELECT a.*, f.name as food_name 
            FROM alerts a
            JOIN food_items f ON a.food_item_id = f.id
            WHERE a.is_read = 0
            ORDER BY a.created_date DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def mark_alert_as_read(self, alert_id: int):
        """Mark an alert as read"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE alerts SET is_read = 1 WHERE id = ?', (alert_id,))
        
        conn.commit()
        conn.close()
    
    def save_recipe(self, recipe_data: Dict) -> int:
        """Save a generated recipe"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO generated_recipes 
            (recipe_name, ingredients, instructions, cuisine_type, 
             preparation_time, servings, used_items)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            recipe_data.get('name'),
            recipe_data.get('ingredients'),
            recipe_data.get('instructions'),
            recipe_data.get('cuisine_type'),
            recipe_data.get('prep_time'),
            recipe_data.get('servings'),
            recipe_data.get('used_items')
        ))
        
        recipe_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return recipe_id
    
    def get_statistics(self) -> Dict:
        """Get summary statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total items
        cursor.execute('SELECT COUNT(*) FROM food_items WHERE status = "fresh"')
        stats['total_items'] = cursor.fetchone()[0]
        
        # Items by category
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM food_items 
            WHERE status = "fresh"
            GROUP BY category
        ''')
        stats['by_category'] = dict(cursor.fetchall())
        
        # Expiring soon (within 3 days)
        threshold_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT COUNT(*) FROM food_items 
            WHERE expiry_date <= ? AND status = "fresh"
        ''', (threshold_date,))
        stats['expiring_soon'] = cursor.fetchone()[0]
        
        # Unread alerts
        cursor.execute('SELECT COUNT(*) FROM alerts WHERE is_read = 0')
        stats['unread_alerts'] = cursor.fetchone()[0]
        
        conn.close()
        
        return stats
    
    def delete_item(self, item_id: int):
        """Delete a food item"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM food_items WHERE id = ?', (item_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Deleted food item: {item_id}")
