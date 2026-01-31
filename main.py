"""
Smart Fridge AI System - Main Application
Orchestrates all components of the system
"""
import schedule
import time
from datetime import datetime
from loguru import logger
import sys
import os

# Setup logging
os.makedirs('logs', exist_ok=True)
logger.add(
    "logs/smart_fridge_{time}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO"
)

from src.database import FridgeDatabase
from src.food_detector import FoodDetector
from src.expiry_tracker import ExpiryTracker, AlertManager
from src.recipe_generator import RecipeGenerator
import src.config as config


class SmartFridgeAI:
    """Main application class for Smart Fridge AI System"""
    
    def __init__(self):
        logger.info("Initializing Smart Fridge AI System...")
        
        # Initialize components
        self.db = FridgeDatabase()
        self.detector = FoodDetector()
        self.tracker = ExpiryTracker(self.db)
        self.alert_manager = AlertManager(self.db)
        self.recipe_gen = RecipeGenerator()
        
        logger.info("All components initialized successfully")
    
    def scan_fridge(self, image_path: str = None):
        """Perform a complete fridge scan"""
        logger.info("Starting fridge scan...")
        
        try:
            # Detect food items
            detected_items = self.detector.process_fridge_scan(image_path)
            
            if not detected_items:
                logger.warning("No items detected in scan")
                return
            
            # Add items to database
            added_count = 0
            for item in detected_items:
                try:
                    self.db.add_food_item(item)
                    added_count += 1
                except Exception as e:
                    logger.error(f"Failed to add item {item.get('name')}: {e}")
            
            logger.info(f"Scan complete: {added_count} items added to database")
            
            # Generate alerts for new items
            self.check_and_alert()
            
            return detected_items
            
        except Exception as e:
            logger.error(f"Fridge scan failed: {e}")
            return None
    
    def check_and_alert(self):
        """Check expiry status and generate alerts"""
        logger.info("Checking expiry status...")
        
        try:
            # Generate alerts
            self.tracker.generate_alerts()
            
            # Get critical alerts
            alerts = self.db.get_unread_alerts()
            critical_alerts = alerts[alerts['alert_level'] == 'critical']
            
            if not critical_alerts.empty:
                logger.warning(f"Found {len(critical_alerts)} critical alerts")
                
                # Send notifications if enabled
                if config.ENABLE_DESKTOP_NOTIFICATIONS:
                    for _, alert in critical_alerts.iterrows():
                        self.alert_manager._send_desktop_notification(
                            "Critical Food Alert",
                            alert['message']
                        )
            
            logger.info("Alert check complete")
            
        except Exception as e:
            logger.error(f"Alert check failed: {e}")
    
    def generate_recipe_from_expiring_items(self):
        """Generate recipe using expiring ingredients"""
        logger.info("Generating recipe from expiring items...")
        
        try:
            # Get expiring items
            expiring_items = self.tracker.get_items_for_recipe()
            
            if not expiring_items:
                logger.info("No expiring items for recipe generation")
                return None
            
            # Extract ingredient names
            ingredients = [item['name'] for item in expiring_items]
            
            # Generate recipe
            recipe = self.recipe_gen.generate_recipe(ingredients)
            
            # Save to database
            recipe_data = {
                'name': recipe['name'],
                'ingredients': str(recipe.get('ingredients', [])),
                'instructions': str(recipe.get('instructions', [])),
                'cuisine_type': recipe.get('cuisine_type'),
                'prep_time': recipe.get('prep_time'),
                'servings': recipe.get('servings'),
                'used_items': ','.join(ingredients)
            }
            
            self.db.save_recipe(recipe_data)
            
            logger.info(f"Recipe generated: {recipe['name']}")
            
            # Print recipe
            print("\n" + "="*50)
            print(self.recipe_gen.format_recipe_for_display(recipe))
            print("="*50 + "\n")
            
            return recipe
            
        except Exception as e:
            logger.error(f"Recipe generation failed: {e}")
            return None
    
    def get_system_status(self):
        """Get current system status"""
        try:
            stats = self.db.get_statistics()
            expiry_status = self.tracker.check_expiry_status()
            
            status = {
                'timestamp': datetime.now().isoformat(),
                'total_items': stats['total_items'],
                'critical_alerts': len(expiry_status['critical']),
                'warning_alerts': len(expiry_status['warning']),
                'unread_alerts': stats['unread_alerts'],
                'items_by_category': stats['by_category']
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return None
    
    def run_scheduled_tasks(self):
        """Setup and run scheduled tasks"""
        logger.info("Setting up scheduled tasks...")
        
        # Schedule automatic scans
        if config.AUTO_SCAN_ENABLED:
            schedule.every(config.SCAN_INTERVAL_HOURS).hours.do(
                self.scan_fridge
            )
            logger.info(f"Auto-scan scheduled every {config.SCAN_INTERVAL_HOURS} hours")
        
        # Schedule daily expiry checks
        schedule.every().day.at("08:00").do(self.check_and_alert)
        schedule.every().day.at("18:00").do(self.check_and_alert)
        
        logger.info("Scheduled tasks configured. Running scheduler...")
        
        # Run scheduler
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def print_status(self):
        """Print current system status"""
        status = self.get_system_status()
        
        if status:
            print("\n" + "="*50)
            print("SMART FRIDGE AI - SYSTEM STATUS")
            print("="*50)
            print(f"Timestamp: {status['timestamp']}")
            print(f"Total Items: {status['total_items']}")
            print(f"Critical Alerts: {status['critical_alerts']}")
            print(f"Warning Alerts: {status['warning_alerts']}")
            print(f"Unread Alerts: {status['unread_alerts']}")
            print("\nItems by Category:")
            for category, count in status['items_by_category'].items():
                print(f"  {category}: {count}")
            print("="*50 + "\n")


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════╗
    ║      SMART FRIDGE AI SYSTEM v1.0             ║
    ║      Food Preservation & Management           ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    # Initialize system
    system = SmartFridgeAI()
    
    # Print initial status
    system.print_status()
    
    # Menu
    while True:
        print("\nMain Menu:")
        print("1. Scan Fridge")
        print("2. Check Alerts")
        print("3. Generate Recipe")
        print("4. View Status")
        print("5. Start Scheduled Tasks")
        print("6. Launch Dashboard")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            image_path = input("Enter image path (or press Enter to use camera): ").strip()
            image_path = image_path if image_path else None
            system.scan_fridge(image_path)
        
        elif choice == '2':
            system.check_and_alert()
            alerts = system.db.get_unread_alerts()
            if not alerts.empty:
                print(f"\nYou have {len(alerts)} unread alerts:")
                for _, alert in alerts.iterrows():
                    print(f"  [{alert['alert_level'].upper()}] {alert['food_name']}: {alert['message']}")
            else:
                print("\n✅ No pending alerts!")
        
        elif choice == '3':
            system.generate_recipe_from_expiring_items()
        
        elif choice == '4':
            system.print_status()
        
        elif choice == '5':
            print("\nStarting scheduled tasks... (Press Ctrl+C to stop)")
            try:
                system.run_scheduled_tasks()
            except KeyboardInterrupt:
                print("\nScheduler stopped.")
        
        elif choice == '6':
            print("\nLaunching dashboard...")
            print("Run: streamlit run dashboard.py")
            print("Dashboard will open in your browser at http://localhost:8501")
            break
        
        elif choice == '7':
            print("\nThank you for using Smart Fridge AI!")
            logger.info("System shutdown")
            break
        
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
