"""
Expiry Tracking and Alert System
"""
from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd
from loguru import logger
from plyer import notification
import config
from database import FridgeDatabase


class ExpiryTracker:
    """Tracks food expiry and generates alerts"""
    
    def __init__(self, db: FridgeDatabase):
        self.db = db
        self.alert_thresholds = config.ALERT_THRESHOLDS
    
    def check_expiry_status(self) -> Dict:
        """Check expiry status of all items"""
        items = self.db.get_all_items()
        
        if items.empty:
            logger.info("No items to check")
            return {'critical': [], 'warning': [], 'normal': [], 'fresh': []}
        
        now = datetime.now()
        status_groups = {
            'critical': [],
            'warning': [],
            'normal': [],
            'fresh': []
        }
        
        for _, item in items.iterrows():
            if pd.isna(item['expiry_date']):
                continue
            
            expiry_date = pd.to_datetime(item['expiry_date'])
            days_until_expiry = (expiry_date - now).days
            
            item_info = {
                'id': item['id'],
                'name': item['name'],
                'category': item['category'],
                'expiry_date': item['expiry_date'],
                'days_remaining': days_until_expiry
            }
            
            if days_until_expiry < 0:
                # Already expired
                status_groups['critical'].append(item_info)
                self.db.update_item_status(item['id'], 'expired')
                
            elif days_until_expiry <= self.alert_thresholds['critical']:
                status_groups['critical'].append(item_info)
                
            elif days_until_expiry <= self.alert_thresholds['warning']:
                status_groups['warning'].append(item_info)
                
            elif days_until_expiry <= self.alert_thresholds['normal']:
                status_groups['normal'].append(item_info)
                
            else:
                status_groups['fresh'].append(item_info)
        
        logger.info(f"Expiry check complete: {len(status_groups['critical'])} critical, "
                   f"{len(status_groups['warning'])} warning, {len(status_groups['normal'])} normal")
        
        return status_groups
    
    def generate_alerts(self):
        """Generate alerts for expiring items"""
        status = self.check_expiry_status()
        
        # Critical alerts (expiring within 1 day or expired)
        for item in status['critical']:
            days = item['days_remaining']
            
            if days < 0:
                message = f"{item['name']} has EXPIRED {abs(days)} day(s) ago!"
            elif days == 0:
                message = f"{item['name']} expires TODAY!"
            else:
                message = f"{item['name']} expires in {days} day(s)!"
            
            self.db.create_alert(
                food_item_id=item['id'],
                alert_type='expiry',
                alert_level='critical',
                message=message
            )
            
            if config.ENABLE_DESKTOP_NOTIFICATIONS:
                self._send_desktop_notification('Critical Alert', message)
        
        # Warning alerts (expiring within 3 days)
        for item in status['warning']:
            message = f"{item['name']} expires in {item['days_remaining']} day(s)"
            
            self.db.create_alert(
                food_item_id=item['id'],
                alert_type='expiry',
                alert_level='warning',
                message=message
            )
        
        # Normal alerts (expiring within 7 days)
        for item in status['normal']:
            message = f"{item['name']} expires in {item['days_remaining']} day(s)"
            
            self.db.create_alert(
                food_item_id=item['id'],
                alert_type='expiry',
                alert_level='normal',
                message=message
            )
        
        logger.info("Alerts generated successfully")
    
    def _send_desktop_notification(self, title: str, message: str):
        """Send desktop notification"""
        try:
            notification.notify(
                title=title,
                message=message,
                app_name='Smart Fridge AI',
                timeout=10
            )
        except Exception as e:
            logger.warning(f"Desktop notification failed: {e}")
    
    def get_items_for_recipe(self, max_items: int = None) -> List[Dict]:
        """Get expiring items that can be used for recipe generation"""
        if max_items is None:
            max_items = config.MAX_INGREDIENTS_FOR_RECIPE
        
        # Get items expiring in next 3 days
        expiring_items = self.db.get_expiring_items(days_threshold=3)
        
        if expiring_items.empty:
            return []
        
        items_list = []
        for _, item in expiring_items.head(max_items).iterrows():
            items_list.append({
                'id': item['id'],
                'name': item['name'],
                'category': item['category'],
                'quantity': item['quantity'],
                'days_remaining': (pd.to_datetime(item['expiry_date']) - datetime.now()).days
            })
        
        return items_list
    
    def calculate_waste_statistics(self) -> Dict:
        """Calculate food waste statistics"""
        conn = self.db.get_connection()
        
        # Get expired items in last 30 days
        query = '''
            SELECT category, COUNT(*) as count, 
                   SUM(CASE WHEN status = 'expired' THEN 1 ELSE 0 END) as expired_count
            FROM food_items
            WHERE storage_date >= date('now', '-30 days')
            GROUP BY category
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        total_items = df['count'].sum()
        total_expired = df['expired_count'].sum()
        waste_rate = (total_expired / total_items * 100) if total_items > 0 else 0
        
        statistics = {
            'total_items_last_30_days': int(total_items),
            'expired_items': int(total_expired),
            'waste_rate_percentage': round(waste_rate, 2),
            'by_category': df.to_dict('records')
        }
        
        return statistics
    
    def get_consumption_insights(self) -> Dict:
        """Get insights on consumption patterns"""
        conn = self.db.get_connection()
        
        # Most consumed categories
        query = '''
            SELECT category, COUNT(*) as consumption_count
            FROM consumption_history
            WHERE consumed_date >= date('now', '-30 days')
            GROUP BY category
            ORDER BY consumption_count DESC
            LIMIT 5
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        insights = {
            'top_consumed_categories': df.to_dict('records'),
            'waste_stats': self.calculate_waste_statistics()
        }
        
        return insights


class AlertManager:
    """Manages alert notifications across different channels"""
    
    def __init__(self, db: FridgeDatabase):
        self.db = db
    
    def send_email_alert(self, recipient: str, subject: str, body: str):
        """Send email alert"""
        if not config.ENABLE_EMAIL_NOTIFICATIONS:
            return
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            message = MIMEMultipart()
            message['From'] = config.SENDER_EMAIL
            message['To'] = recipient
            message['Subject'] = subject
            
            message.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
            server.starttls()
            server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
            server.send_message(message)
            server.quit()
            
            logger.info(f"Email alert sent to {recipient}")
            
        except Exception as e:
            logger.error(f"Email alert failed: {e}")
    
    def send_sms_alert(self, phone_number: str, message: str):
        """Send SMS alert using Twilio"""
        if not config.ENABLE_SMS_NOTIFICATIONS:
            return
        
        try:
            from twilio.rest import Client
            
            client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
            
            message = client.messages.create(
                body=message,
                from_=config.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            
            logger.info(f"SMS alert sent to {phone_number}")
            
        except Exception as e:
            logger.error(f"SMS alert failed: {e}")
    
    def get_alert_summary(self) -> str:
        """Generate HTML summary of alerts"""
        alerts = self.db.get_unread_alerts()
        
        if alerts.empty:
            return "<p>No active alerts</p>"
        
        html = "<h3>Active Alerts</h3><ul>"
        
        for _, alert in alerts.iterrows():
            color = {
                'critical': 'red',
                'warning': 'orange',
                'normal': 'blue'
            }.get(alert['alert_level'], 'gray')
            
            html += f"<li style='color: {color}'><strong>{alert['food_name']}</strong>: {alert['message']}</li>"
        
        html += "</ul>"
        
        return html
