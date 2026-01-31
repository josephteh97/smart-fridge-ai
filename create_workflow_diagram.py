"""
Generate System Workflow Schematic Diagram
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np


def create_workflow_diagram():
    """Create a comprehensive workflow diagram for the Smart Fridge AI System"""
    
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Title
    ax.text(5, 13.5, 'Smart Fridge AI System - Workflow Architecture',
            fontsize=20, fontweight='bold', ha='center')
    
    # Color scheme
    colors = {
        'input': '#E3F2FD',      # Light Blue
        'process': '#FFF3E0',    # Light Orange
        'database': '#E8F5E9',   # Light Green
        'output': '#F3E5F5',     # Light Purple
        'alert': '#FFEBEE'       # Light Red
    }
    
    # Define box style
    def draw_box(x, y, width, height, text, color, fontsize=10):
        box = FancyBboxPatch((x, y), width, height,
                            boxstyle="round,pad=0.1",
                            edgecolor='black',
                            facecolor=color,
                            linewidth=2)
        ax.add_patch(box)
        ax.text(x + width/2, y + height/2, text,
               fontsize=fontsize, ha='center', va='center',
               weight='bold', wrap=True)
    
    # Define arrow style
    def draw_arrow(x1, y1, x2, y2, label='', style='->'):
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                               arrowstyle=style,
                               color='black',
                               linewidth=2,
                               mutation_scale=20)
        ax.add_patch(arrow)
        if label:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x + 0.2, mid_y + 0.1, label,
                   fontsize=8, style='italic', bbox=dict(boxstyle='round', 
                   facecolor='white', alpha=0.8))
    
    # Layer 1: Input Sources
    draw_box(0.5, 11.5, 2, 1, 'Fridge Camera\n(Image Capture)', colors['input'], 9)
    draw_box(3, 11.5, 2, 1, 'Manual Input\n(User Entry)', colors['input'], 9)
    draw_box(5.5, 11.5, 2, 1, 'Barcode Scanner\n(Product ID)', colors['input'], 9)
    
    # Layer 2: Image Processing
    draw_box(1.5, 9.5, 3, 1.2, 'Computer Vision Module\n• YOLOv8 Food Detection\n• OCR (EasyOCR/Tesseract)\n• Barcode Recognition',
            colors['process'], 8)
    
    # Arrows from inputs to processing
    draw_arrow(1.5, 11.5, 2.5, 10.7, 'Images')
    draw_arrow(4, 11.5, 3.5, 10.7, 'Data')
    draw_arrow(6.5, 11.5, 4.5, 10.7, 'Codes')
    
    # Layer 3: Data Extraction
    draw_box(0.5, 7.8, 1.8, 1, 'Food Item\nIdentification', colors['process'], 8)
    draw_box(2.5, 7.8, 1.8, 1, 'Expiry Date\nExtraction', colors['process'], 8)
    draw_box(4.5, 7.8, 1.8, 1, 'Category\nClassification', colors['process'], 8)
    
    # Arrows from CV to extraction
    draw_arrow(2.5, 9.5, 1.4, 8.8)
    draw_arrow(3, 9.5, 3.4, 8.8)
    draw_arrow(3.5, 9.5, 5.4, 8.8)
    
    # Layer 4: Database
    draw_box(2, 6, 3, 1.2, 'SQLite Database\n• Food Items Table\n• Alerts Table\n• Consumption History\n• Recipes',
            colors['database'], 8)
    
    # Arrows to database
    draw_arrow(1.4, 7.8, 3, 7.2, 'Store')
    draw_arrow(3.4, 7.8, 3.5, 7.2, 'Store')
    draw_arrow(5.4, 7.8, 4, 7.2, 'Store')
    
    # Layer 5: Core Processing Modules
    draw_box(6.5, 9, 3, 1.2, 'Expiry Tracker\n• Monitor Shelf Life\n• Calculate Days Remaining\n• Status Classification',
            colors['process'], 8)
    
    draw_box(6.5, 7, 3, 1.2, 'Alert System\n• Generate Alerts\n• Set Priority Levels\n• Send Notifications',
            colors['alert'], 8)
    
    draw_box(6.5, 5, 3, 1.2, 'Recipe Generator\n• AI-Powered (GPT)\n• Use Expiring Items\n• Dietary Preferences',
            colors['process'], 8)
    
    # Arrows from database to modules
    draw_arrow(5, 6.6, 6.5, 9.5, 'Query')
    draw_arrow(5, 6.4, 6.5, 7.5, 'Query')
    draw_arrow(5, 6.2, 6.5, 5.5, 'Query')
    
    # Bidirectional arrows
    draw_arrow(6.5, 9.5, 5, 6.8, 'Update', '<-')
    draw_arrow(6.5, 7.5, 5, 6.6, 'Update', '<-')
    draw_arrow(6.5, 5.5, 5, 6.4, 'Update', '<-')
    
    # Layer 6: User Interface
    draw_box(1, 3.5, 3.5, 1.5, 'Web Dashboard (Streamlit)\n• Real-time Monitoring\n• Food Inventory View\n• Category Distribution\n• Expiry Timeline',
            colors['output'], 9)
    
    draw_box(5.5, 3.5, 3.5, 1.5, 'Alert Notifications\n• Desktop Notifications\n• Email Alerts\n• SMS Alerts\n• Priority Indicators',
            colors['alert'], 9)
    
    # Arrows to outputs
    draw_arrow(3.5, 6, 2.75, 5, 'Display')
    draw_arrow(8, 7, 7.25, 5, 'Notify')
    
    # Layer 7: User Actions
    draw_box(1.5, 1.5, 2, 0.8, 'User Actions\n• View Status\n• Add/Remove Items',
            colors['input'], 8)
    
    draw_box(4, 1.5, 2, 0.8, 'Recipe Actions\n• Generate Recipe\n• Save Recipe',
            colors['input'], 8)
    
    draw_box(6.5, 1.5, 2, 0.8, 'System Actions\n• Mark Consumed\n• Acknowledge Alerts',
            colors['input'], 8)
    
    # Feedback arrows
    draw_arrow(2.5, 3.5, 2.5, 2.3, 'Interact', '<->')
    draw_arrow(5, 3.5, 5, 2.3, 'Interact', '<->')
    draw_arrow(7.5, 3.5, 7.5, 2.3, 'Interact', '<->')
    
    # Data flow loop
    draw_arrow(7.5, 1.5, 4, 6, 'Feedback Loop', '->')
    
    # Legend
    legend_y = 0.3
    ax.text(0.5, legend_y + 0.5, 'Legend:', fontsize=10, weight='bold')
    
    legend_items = [
        (colors['input'], 'Input/User Interface'),
        (colors['process'], 'Processing Module'),
        (colors['database'], 'Data Storage'),
        (colors['output'], 'Output/Display'),
        (colors['alert'], 'Alert System')
    ]
    
    for i, (color, label) in enumerate(legend_items):
        x_pos = 0.5 + (i * 1.8)
        legend_box = FancyBboxPatch((x_pos, legend_y), 0.3, 0.3,
                                   boxstyle="round,pad=0.05",
                                   edgecolor='black',
                                   facecolor=color,
                                   linewidth=1)
        ax.add_patch(legend_box)
        ax.text(x_pos + 0.4, legend_y + 0.15, label, fontsize=7, va='center')
    
    # Add system features box
    features_text = """Key System Features:
    • Automated Food Detection using Computer Vision
    • Real-time Expiry Tracking & Monitoring
    • Multi-level Alert System (Critical/Warning/Normal)
    • AI-Powered Recipe Generation
    • Comprehensive Analytics & Reporting
    • Multiple Notification Channels
    • Historical Data & Waste Analysis"""
    
    ax.text(0.2, 12.8, features_text, fontsize=8,
           bbox=dict(boxstyle='round', facecolor='lightyellow', 
           edgecolor='black', linewidth=2),
           verticalalignment='top', family='monospace')
    
    plt.tight_layout()
    plt.savefig('/home/claude/smart_fridge_ai/docs/system_workflow_diagram.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    print("Workflow diagram saved to: docs/system_workflow_diagram.png")
    
    return fig


if __name__ == "__main__":
    import os
    os.makedirs('/home/claude/smart_fridge_ai/docs', exist_ok=True)
    create_workflow_diagram()
    print("Workflow schematic generated successfully!")
