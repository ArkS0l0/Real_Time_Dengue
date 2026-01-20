# ============== CONFIGURATION ==============

import telebot
from ultralytics import YOLO
from PIL import Image
import os
import csv
from datetime import datetime
import io

# ============== CONFIGURATION ==============
BOT_TOKEN = "8285850333:AAFkDNuKWIXbVe-cv1Self6kjNmF3_cRpWE"  # Replace with your BotFather token
MODEL_PATH = "best.pt"
CSV_FILE = "environment_scans.csv"

# Risk weights for each detection class
RISK_WEIGHTS = {
    "Bottle": 2.0,
    "Coconut-Exocarp": 1.5,
    "Drain-Inlet": 2.5,
    "Tire": 2.5,
    "Vase": 1.5
}

# ============== INITIALIZE ==============
bot = telebot.TeleBot(BOT_TOKEN)
model = YOLO(MODEL_PATH)

# Create CSV if not exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'user_id', 'username', 'detections', 'risk_score', 'risk_level'])

# ============== HELPER FUNCTIONS ==============
def calculate_risk(detections):
    """Calculate risk score based on detections"""
    score = 0
    for item, count in detections.items():
        weight = RISK_WEIGHTS.get(item, 1.0)
        score += weight * count
    
    if score >= 5:
        return score, "HIGH RISK"
    elif score >= 2:
        return score, "MEDIUM RISK"
    else:
        return score, "LOW RISK"

def save_to_csv(user_id, username, detections, risk_score, risk_level):
    """Save scan results to CSV for Streamlit dashboard"""
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id,
            username,
            str(detections),
            risk_score,
            risk_level
        ])

def format_results(detections, risk_score, risk_level):
    """Format detection results as message"""
    if not detections:
        return "*No breeding sites detected!*\n\nYour environment appears safe. Keep it clean!"
    
    message = f"*DENGUE RISK SCAN RESULTS*\n\n"
    message += f"*Risk Level:* {risk_level}\n"
    message += f"*Risk Score:* {risk_score:.1f}\n\n"
    message += "*Detected Items:*\n"
    
    for item, count in detections.items():
        message += f"  - {item}: {count}\n"
    
    message += "\n*Recommendations:*\n"
    
    if "Tire" in detections:
        message += "  - Remove or cover old tires\n"
    if "Bottle" in detections:
        message += "  - Dispose of bottles properly\n"
    if "Vase" in detections:
        message += "  - Change vase water regularly\n"
    if "Drain-Inlet" in detections:
        message += "  - Clear clogged drains\n"
    if "Coconut-Exocarp" in detections:
        message += "  - Remove coconut shells\n"
    
    return message

# ============== BOT HANDLERS ==============
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
*Welcome to Dengue Risk Scanner!*

I can analyze photos of your environment to detect potential mosquito breeding sites.

*How to use:*
1. Take a photo of your surroundings
2. Send it to me
3. Get instant risk assessment!

*What I detect:*
- Bottles
- Tires
- Vases/Flower pots
- Drain inlets
- Coconut shells

Send me a photo to get started!
    """
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
*Help Guide*

*Commands:*
/start - Welcome message
/help - This help guide
/about - About this bot

*How to scan:*
Simply send any photo and I'll analyze it for dengue breeding sites.

*Risk Levels:*
LOW - Score < 2
MEDIUM - Score 2-5
HIGH - Score > 5

*Tips for best results:*
- Good lighting
- Clear photos
- Include suspected areas
    """
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['about'])
def send_about(message):
    about_text = """
*About Dengue Risk Scanner*

This bot uses AI (YOLOv8) to detect potential mosquito breeding sites in your environment.

*Developed for:*
Final Year Project - Dengue Risk Assessment System

*Model trained to detect:*
- Bottles
- Coconut shells (Exocarp)
- Drain inlets
- Tires
- Vases

Stay safe from dengue!
    """
    bot.reply_to(message, about_text, parse_mode='Markdown')

def process_image(message, file_id):
    """Common function to process images from both photos and documents"""
    try:
        # Send processing message
        processing_msg = bot.reply_to(message, "Analyzing image...")
        
        # Get file
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Save temporarily
        temp_path = f"temp_{message.from_user.id}.jpg"
        with open(temp_path, 'wb') as f:
            f.write(downloaded_file)
        
        # Run YOLOv8 detection
        results = model.predict(temp_path, conf=0.5, save=True, project="detections", name="scan", exist_ok=True)
        
        # Count detections
        detections = {}
        for result in results:
            for box in result.boxes:
                class_name = model.names[int(box.cls)]
                detections[class_name] = detections.get(class_name, 0) + 1
        
        # Calculate risk
        risk_score, risk_level = calculate_risk(detections)
        
        # Save to CSV
        username = message.from_user.username or "unknown"
        save_to_csv(message.from_user.id, username, detections, risk_score, risk_level)
        
        # Format results message
        result_message = format_results(detections, risk_score, risk_level)
        
        # Send annotated image
        annotated_path = "detections/scan/temp_" + str(message.from_user.id) + ".jpg"
        if os.path.exists(annotated_path):
            with open(annotated_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=result_message, parse_mode='Markdown')
        else:
            bot.reply_to(message, result_message, parse_mode='Markdown')
        
        # Delete processing message
        bot.delete_message(message.chat.id, processing_msg.message_id)
        
        # Cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    except Exception as e:
        bot.reply_to(message, f"Error processing image: {str(e)}")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """Handle compressed photos"""
    file_id = message.photo[-1].file_id
    process_image(message, file_id)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    """Handle uncompressed images sent as documents"""
    # Check if document is an image
    if message.document.mime_type and message.document.mime_type.startswith('image/'):
        file_id = message.document.file_id
        process_image(message, file_id)
    else:
        bot.reply_to(message, "Please send an image file (JPG, PNG, etc.)")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.reply_to(message, "Please send me a *photo* to analyze for dengue breeding sites!", parse_mode='Markdown')

# ============== RUN BOT ==============
if __name__ == "__main__":
    print("Dengue Risk Scanner Bot is running...")
    print("Press Ctrl+C to stop")
    bot.infinity_polling()
