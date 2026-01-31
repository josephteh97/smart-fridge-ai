"""
Smart Fridge AI Dashboard - Interactive Web Interface
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.database import FridgeDatabase
from src.expiry_tracker import ExpiryTracker, AlertManager
from src.recipe_generator import RecipeGenerator
from src.food_detector import FoodDetector
import src.config as config


# Page configuration
st.set_page_config(
    page_title="Smart Fridge AI",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .alert-critical {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .alert-warning {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .alert-normal {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize components
@st.cache_resource
def initialize_system():
    """Initialize all system components"""
    db = FridgeDatabase()
    tracker = ExpiryTracker(db)
    alert_manager = AlertManager(db)
    recipe_gen = RecipeGenerator()
    food_detector = FoodDetector()
    
    return db, tracker, alert_manager, recipe_gen, food_detector


def main():
    """Main dashboard function"""
    
    # Initialize system
    db, tracker, alert_manager, recipe_gen, food_detector = initialize_system()
    
    # Header
    st.markdown('<h1 class="main-header">🧊 Smart Fridge AI System</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Food Inventory", "Scan Items", "Alerts", "Recipes", "Statistics"]
    )
    
    # Dashboard Page
    if page == "Dashboard":
        show_dashboard(db, tracker)
    
    # Food Inventory Page
    elif page == "Food Inventory":
        show_inventory(db)
    
    # Scan Items Page
    elif page == "Scan Items":
        show_scan_page(db, food_detector)
    
    # Alerts Page
    elif page == "Alerts":
        show_alerts(db, tracker, alert_manager)
    
    # Recipes Page
    elif page == "Recipes":
        show_recipes(db, tracker, recipe_gen)
    
    # Statistics Page
    elif page == "Statistics":
        show_statistics(db, tracker)


def show_dashboard(db: FridgeDatabase, tracker: ExpiryTracker):
    """Show main dashboard overview"""
    
    st.header("📊 Dashboard Overview")
    
    # Get statistics
    stats = db.get_statistics()
    expiry_status = tracker.check_expiry_status()
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Items", stats['total_items'], delta=None)
    
    with col2:
        critical_count = len(expiry_status['critical'])
        st.metric("Critical Alerts", critical_count, delta=None, delta_color="inverse")
    
    with col3:
        warning_count = len(expiry_status['warning'])
        st.metric("Expiring Soon", warning_count, delta=None)
    
    with col4:
        st.metric("Unread Alerts", stats['unread_alerts'], delta=None)
    
    st.markdown("---")
    
    # Two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Category Distribution
        st.subheader("📦 Items by Category")
        if stats['by_category']:
            category_df = pd.DataFrame(list(stats['by_category'].items()), 
                                      columns=['Category', 'Count'])
            fig = px.pie(category_df, values='Count', names='Category', 
                        color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No items in inventory")
    
    with col2:
        # Expiry Timeline
        st.subheader("⏰ Expiry Timeline")
        timeline_data = []
        for status, items in expiry_status.items():
            for item in items:
                timeline_data.append({
                    'Food': item['name'],
                    'Days Remaining': item['days_remaining'],
                    'Status': status.capitalize()
                })
        
        if timeline_data:
            timeline_df = pd.DataFrame(timeline_data)
            fig = px.bar(timeline_df, x='Food', y='Days Remaining', color='Status',
                        color_discrete_map={
                            'Critical': '#f44336',
                            'Warning': '#ff9800',
                            'Normal': '#2196f3',
                            'Fresh': '#4caf50'
                        })
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No items to display")
    
    # Recent Items
    st.subheader("🆕 Recently Added Items")
    all_items = db.get_all_items()
    if not all_items.empty:
        recent_items = all_items.head(5)[['name', 'category', 'storage_date', 'expiry_date', 'status']]
        st.dataframe(recent_items, use_container_width=True)
    else:
        st.info("No items in inventory")


def show_inventory(db: FridgeDatabase):
    """Show food inventory management"""
    
    st.header("📦 Food Inventory")
    
    # Add new item manually
    with st.expander("➕ Add New Item Manually"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input("Food Name")
            category = st.selectbox("Category", config.FOOD_CATEGORIES)
        
        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1)
            unit = st.selectbox("Unit", ["piece", "kg", "g", "L", "ml", "pack"])
        
        with col3:
            expiry_date = st.date_input("Expiry Date")
            location = st.text_input("Location", value="main_compartment")
        
        if st.button("Add Item"):
            if name:
                item_data = {
                    'name': name,
                    'category': category,
                    'quantity': quantity,
                    'unit': unit,
                    'expiry_date': expiry_date.strftime('%Y-%m-%d'),
                    'location': location
                }
                db.add_food_item(item_data)
                st.success(f"Added {name} to inventory!")
                st.rerun()
            else:
                st.error("Please enter a food name")
    
    st.markdown("---")
    
    # Display inventory
    st.subheader("Current Inventory")
    
    # Filter options
    col1, col2 = st.columns([1, 3])
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + config.FOOD_CATEGORIES)
    
    # Get items
    if filter_category == "All":
        items = db.get_all_items()
    else:
        items = db.get_items_by_category(filter_category)
    
    if not items.empty:
        # Display as table with actions
        for idx, item in items.iterrows():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                st.write(f"**{item['name']}** ({item['category']})")
            
            with col2:
                days_left = (pd.to_datetime(item['expiry_date']) - datetime.now()).days
                if days_left < 0:
                    st.error(f"Expired {abs(days_left)} days ago")
                elif days_left <= 1:
                    st.error(f"Expires in {days_left} day(s)")
                elif days_left <= 3:
                    st.warning(f"Expires in {days_left} days")
                else:
                    st.info(f"Expires in {days_left} days")
            
            with col3:
                st.write(f"Qty: {item['quantity']} {item['unit']}")
            
            with col4:
                if st.button("🗑️", key=f"delete_{item['id']}"):
                    db.delete_item(item['id'])
                    st.rerun()
            
            st.markdown("---")
    else:
        st.info("No items in inventory")


def show_scan_page(db: FridgeDatabase, detector: FoodDetector):
    """Show scanning interface"""
    
    st.header("📷 Scan Food Items")
    
    st.info("Upload an image of your fridge contents to automatically detect and add items")
    
    uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        # Display image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        if st.button("🔍 Scan and Detect Items"):
            with st.spinner("Scanning image..."):
                # Save uploaded file temporarily
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Process scan
                detected_items = detector.process_fridge_scan(tmp_path)
                
                if detected_items:
                    st.success(f"Detected {len(detected_items)} items!")
                    
                    # Display detected items
                    st.subheader("Detected Items:")
                    for i, item in enumerate(detected_items):
                        col1, col2, col3 = st.columns([2, 2, 1])
                        
                        with col1:
                            st.write(f"**{item['name']}** ({item['category']})")
                        
                        with col2:
                            st.write(f"Confidence: {item['confidence_score']*100:.1f}%")
                        
                        with col3:
                            if st.button("Add", key=f"add_{i}"):
                                db.add_food_item(item)
                                st.success(f"Added {item['name']}!")
                else:
                    st.warning("No items detected. Please try a clearer image or add items manually.")


def show_alerts(db: FridgeDatabase, tracker: ExpiryTracker, alert_manager: AlertManager):
    """Show alerts page"""
    
    st.header("🔔 Alerts & Notifications")
    
    # Generate fresh alerts
    if st.button("🔄 Refresh Alerts"):
        tracker.generate_alerts()
        st.rerun()
    
    # Get unread alerts
    alerts = db.get_unread_alerts()
    
    if not alerts.empty:
        st.subheader(f"You have {len(alerts)} unread alerts")
        
        # Group by level
        critical_alerts = alerts[alerts['alert_level'] == 'critical']
        warning_alerts = alerts[alerts['alert_level'] == 'warning']
        normal_alerts = alerts[alerts['alert_level'] == 'normal']
        
        # Critical alerts
        if not critical_alerts.empty:
            st.markdown("### 🚨 Critical Alerts")
            for _, alert in critical_alerts.iterrows():
                st.markdown(f'<div class="alert-critical">'
                          f'<strong>{alert["food_name"]}</strong>: {alert["message"]}'
                          f'</div>', unsafe_allow_html=True)
        
        # Warning alerts
        if not warning_alerts.empty:
            st.markdown("### ⚠️ Warning Alerts")
            for _, alert in warning_alerts.iterrows():
                st.markdown(f'<div class="alert-warning">'
                          f'<strong>{alert["food_name"]}</strong>: {alert["message"]}'
                          f'</div>', unsafe_allow_html=True)
        
        # Normal alerts
        if not normal_alerts.empty:
            st.markdown("### ℹ️ Information")
            for _, alert in normal_alerts.iterrows():
                st.markdown(f'<div class="alert-normal">'
                          f'<strong>{alert["food_name"]}</strong>: {alert["message"]}'
                          f'</div>', unsafe_allow_html=True)
        
        if st.button("Mark All as Read"):
            for alert_id in alerts['id']:
                db.mark_alert_as_read(alert_id)
            st.success("All alerts marked as read!")
            st.rerun()
    else:
        st.success("✅ No pending alerts!")


def show_recipes(db: FridgeDatabase, tracker: ExpiryTracker, recipe_gen: RecipeGenerator):
    """Show recipe generation page"""
    
    st.header("🍳 Recipe Suggestions")
    
    st.info("Generate recipes using ingredients that are about to expire!")
    
    # Get expiring items
    expiring_items = tracker.get_items_for_recipe(max_items=10)
    
    if expiring_items:
        st.subheader("Ingredients Available for Recipes:")
        
        ingredients_list = [item['name'] for item in expiring_items]
        
        for item in expiring_items:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"• {item['name']} ({item['category']})")
            with col2:
                st.write(f"{item['days_remaining']} days left")
        
        st.markdown("---")
        
        # Recipe generation options
        col1, col2 = st.columns(2)
        
        with col1:
            cuisine_type = st.selectbox("Cuisine Type (Optional)", 
                                       ["Any", "Asian", "Italian", "Mexican", "Mediterranean", "American"])
        
        with col2:
            dietary = st.multiselect("Dietary Restrictions", 
                                    ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free"])
        
        if st.button("🎲 Generate Recipe"):
            with st.spinner("Generating recipe..."):
                cuisine = None if cuisine_type == "Any" else cuisine_type
                recipe = recipe_gen.generate_recipe(
                    ingredients_list,
                    cuisine_type=cuisine,
                    dietary_restrictions=dietary if dietary else None
                )
                
                # Display recipe
                st.success("Recipe Generated!")
                
                st.markdown(f"## {recipe['name']}")
                st.write(f"**Description:** {recipe.get('description', 'N/A')}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Prep Time", f"{recipe.get('prep_time', 'N/A')} mins")
                with col2:
                    st.metric("Cook Time", f"{recipe.get('cook_time', 'N/A')} mins")
                with col3:
                    st.metric("Servings", recipe.get('servings', 'N/A'))
                
                st.markdown("### 📦 Ingredients")
                for ing in recipe.get('ingredients', []):
                    if isinstance(ing, dict):
                        st.write(f"• {ing.get('amount', '')} {ing.get('unit', '')} {ing.get('item', '')}")
                    else:
                        st.write(f"• {ing}")
                
                st.markdown("### 📋 Instructions")
                for i, step in enumerate(recipe.get('instructions', []), 1):
                    st.write(f"{i}. {step}")
                
                if recipe.get('tips'):
                    st.markdown("### 💡 Tips")
                    for tip in recipe['tips']:
                        st.write(f"• {tip}")
                
                # Save recipe option
                if st.button("💾 Save Recipe"):
                    recipe_data = {
                        'name': recipe['name'],
                        'ingredients': str(recipe.get('ingredients', [])),
                        'instructions': str(recipe.get('instructions', [])),
                        'cuisine_type': recipe.get('cuisine_type'),
                        'prep_time': recipe.get('prep_time'),
                        'servings': recipe.get('servings'),
                        'used_items': ','.join(ingredients_list)
                    }
                    db.save_recipe(recipe_data)
                    st.success("Recipe saved to database!")
    else:
        st.info("No expiring items available for recipe generation. Your fridge is well-stocked!")


def show_statistics(db: FridgeDatabase, tracker: ExpiryTracker):
    """Show statistics and analytics"""
    
    st.header("📈 Statistics & Analytics")
    
    # Time period selection
    period = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "Last 90 Days"])
    
    # Waste statistics
    waste_stats = tracker.calculate_waste_statistics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Items (30 days)", waste_stats['total_items_last_30_days'])
    
    with col2:
        st.metric("Expired Items", waste_stats['expired_items'])
    
    with col3:
        st.metric("Waste Rate", f"{waste_stats['waste_rate_percentage']}%")
    
    st.markdown("---")
    
    # Consumption insights
    insights = tracker.get_consumption_insights()
    
    # Waste by category
    st.subheader("Waste by Category")
    if waste_stats['by_category']:
        waste_df = pd.DataFrame(waste_stats['by_category'])
        fig = px.bar(waste_df, x='category', y='expired_count', 
                    title="Expired Items by Category",
                    labels={'expired_count': 'Expired Items', 'category': 'Category'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("💡 Recommendations")
    if waste_stats['waste_rate_percentage'] > 20:
        st.warning("⚠️ Your waste rate is high. Consider:")
        st.write("• Setting earlier alert thresholds")
        st.write("• Using the recipe generator more often")
        st.write("• Buying smaller quantities")
    else:
        st.success("✅ Your waste rate is good! Keep it up!")


if __name__ == "__main__":
    main()
